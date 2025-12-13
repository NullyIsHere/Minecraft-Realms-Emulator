import docker
import socket
from typing import Optional
from docker.models.containers import Container


class DockerHelper:
    def __init__(self, world_id: int):
        self.world_id = world_id
        self.docker_client = docker.from_env()
    
    async def create_volume(self) -> None:
        """Create a Docker volume for the world"""
        volume_name = f"realm-server-{self.world_id}"
        try:
            self.docker_client.volumes.create(name=volume_name)
        except docker.errors.APIError:
            pass  # Volume might already exist
    
    def _find_free_port(self) -> int:
        """Find a free port to bind the server to"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            s.listen(1)
            port = s.getsockname()[1]
        return port
    
    async def create_container(self, slot_id: int) -> Container:
        """Create a Docker container for the server"""
        free_port = self._find_free_port()
        container_name = f"realm-server-{self.world_id}"
        
        container = self.docker_client.containers.create(
            image="realm-server",
            name=container_name,
            detach=True,
            auto_remove=True,
            ports={'25565/tcp': ('0.0.0.0', free_port)},
            volumes={f"realm-server-{self.world_id}": {'bind': '/mc', 'mode': 'rw'}},
            environment={'SLOT_ID': str(slot_id)}
        )
        return container
    
    async def is_running(self) -> bool:
        """Check if the server container is running"""
        try:
            container = self.docker_client.containers.get(f"realm-server-{self.world_id}")
            return container.status == 'running'
        except docker.errors.NotFound:
            return False
    
    async def start_server(self, slot_id: int) -> None:
        """Start the server container"""
        container = await self.create_container(slot_id)
        container.start()
    
    async def get_server_port(self) -> int:
        """Get the port the server is bound to"""
        container = self.docker_client.containers.get(f"realm-server-{self.world_id}")
        ports = container.ports
        return int(ports['25565/tcp'][0]['HostPort'])
    
    async def stop_server(self, force: bool = False) -> None:
        """Stop the server container"""
        try:
            container = self.docker_client.containers.get(f"realm-server-{self.world_id}")
            if force:
                container.stop()
            else:
                await self.execute_command("stop")
        except docker.errors.NotFound:
            pass
    
    async def delete_server(self) -> None:
        """Delete the server container and volume"""
        try:
            container = self.docker_client.containers.get(f"realm-server-{self.world_id}")
            container.remove(force=True)
        except docker.errors.NotFound:
            print("Container offline, removing only server data")
        
        try:
            volume = self.docker_client.volumes.get(f"realm-server-{self.world_id}")
            volume.remove()
        except docker.errors.NotFound:
            pass
    
    async def execute_command(self, command: str) -> str:
        """Execute a command in the container"""
        container = self.docker_client.containers.get(f"realm-server-{self.world_id}")
        exec_result = container.exec_run(command)
        return exec_result.output.decode('utf-8')
    
    async def get_server_logs_stream(self, handler):
        """Stream server logs"""
        container = self.docker_client.containers.get(f"realm-server-{self.world_id}")
        for line in container.logs(stream=True, follow=True, tail=100):
            handler(line.decode('utf-8'))
