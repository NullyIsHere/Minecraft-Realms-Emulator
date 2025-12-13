from sqlalchemy.orm import Session
from app.models.enums import StateEnum
from app.helpers.docker_helper import DockerHelper


class WorldHelper:
    def __init__(self, db: Session, world_id: int):
        self.db = db
        self.world_id = world_id
    
    async def get_state(self) -> str:
        """Get the state of a world"""
        from app.models.entities import World
        
        world = self.db.query(World).filter(World.Id == self.world_id).first()
        
        if world.Name is None:
            return StateEnum.UNINITIALIZED.value
        
        docker_helper = DockerHelper(world.Id)
        if await docker_helper.is_running():
            return StateEnum.OPEN.value
        
        return StateEnum.CLOSED.value
