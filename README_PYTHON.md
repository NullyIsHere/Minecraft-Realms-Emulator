# Minecraft Realms Emulator (Python)

This is a custom implementation of a Minecraft Realms server for Java Edition, written in **Python** using FastAPI.

## Requirements

- Python 3.11 or higher
- Minecraft Java Edition
- PostgreSQL (for database support)
- Docker (for `REALMS` mode to work)

## Installation

Clone the repository:

```sh
git clone https://github.com/NullyIsHere/Minecraft-Realms-Emulator.git 
cd Minecraft-Realms-Emulator
```

Install Python dependencies:

```sh
pip install -r requirements.txt
```

Configure the server:

Create a `.env` file based on `.env.example`:

```
CONNECTION_STRING=postgresql://postgres:password@db:5432/Minecraft-Realms-Emulator
ADMIN_KEY=[RANDOMLY GENERATED KEY]
```

## Running the Server

Run the server using uvicorn:

```sh
python -m uvicorn app.main:app --host 0.0.0.0 --port 5000
```

Or run directly:

```sh
python app/main.py
```

The server will start on `http://localhost:5000`.

## API Documentation

Once the server is running, you can access the auto-generated API documentation at:
- Swagger UI: `http://localhost:5000/docs`
- ReDoc: `http://localhost:5000/redoc`

## Docker Support

Make sure Docker is installed and running before starting the server. The application will check for Docker availability on startup.

## Project Structure

```
app/
├── main.py                  # FastAPI application entry point
├── models/
│   ├── __init__.py         # Database configuration
│   ├── entities.py         # SQLAlchemy models
│   └── enums.py            # Enum definitions
├── schemas/
│   ├── requests.py         # Pydantic request models
│   └── responses.py        # Pydantic response models
├── controllers/
│   ├── worlds.py           # World management endpoints
│   ├── activities.py       # Activity tracking
│   ├── invites.py          # Invite management
│   └── ...                 # Other controllers
├── middleware/
│   └── dependencies.py     # FastAPI dependencies for auth
├── helpers/
│   ├── docker_helper.py    # Docker operations
│   ├── world_helper.py     # World management helpers
│   ├── config_helper.py    # Configuration management
│   └── minecraft_version_parser.py  # Version comparison
└── resources/              # Static resources
```

## Development

To run in development mode with auto-reload:

```sh
uvicorn app.main:app --reload --host 0.0.0.0 --port 5000
```

## Original C# Version

This is a port of the original C# ASP.NET Core implementation. The original version can be found in the `Minecraft-Realms-Emulator/` directory.

## Migration from C#

The Python port maintains API compatibility with the original C# version. The main differences are:

1. **Web Framework**: ASP.NET Core → FastAPI
2. **ORM**: Entity Framework Core → SQLAlchemy
3. **Validation**: Data Annotations → Pydantic
4. **Dependency Injection**: Built-in DI → FastAPI Dependencies
5. **Docker Client**: Docker.DotNet → docker-py

All endpoints and functionality remain the same.
