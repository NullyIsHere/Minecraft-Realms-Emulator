# Minecraft Realms Emulator

This is a custom implementation of a Minecraft Realms server for Java Edition, written in **Python** using FastAPI.

> **Note:** This project has been fully ported from C# to Python. The original C# implementation has been replaced with this modern Python version.

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

## Docker Support

You can also run the application using Docker:

```sh
docker-compose -f docker-compose.python.yml up
```

Or build manually:

```sh
docker build -f Dockerfile.python -t minecraft-realms-emulator .
docker run -p 5000:5000 --env-file .env minecraft-realms-emulator
```

## API Documentation

Once the server is running, you can access the auto-generated API documentation at:
- Swagger UI: `http://localhost:5000/docs`
- ReDoc: `http://localhost:5000/redoc`

## Documentation

For detailed information about the Python implementation:
- [README_PYTHON.md](README_PYTHON.md) - Detailed Python setup and usage
- [PORTING_GUIDE.md](PORTING_GUIDE.md) - Technical porting details from C# to Python
- [PYTHON_PORT_COMPLETION_SUMMARY.md](PYTHON_PORT_COMPLETION_SUMMARY.md) - Complete project summary

## Demo

[![Demo](https://img.youtube.com/vi/5pHPsKQhEjI/0.jpg)](https://www.youtu.be/5pHPsKQhEjI)
