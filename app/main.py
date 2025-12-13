import os
import sys
import subprocess
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.models import engine, get_db, SessionLocal
from app.models.entities import Base
from app.helpers.config_helper import ConfigHelper

# Load environment variables
load_dotenv()

# Check for CONNECTION_STRING
if not os.getenv("CONNECTION_STRING"):
    print("CONNECTION_STRING environment variable missing")
    sys.exit(1)

# Create FastAPI app
app = FastAPI(
    title="Minecraft Realms Emulator",
    description="Custom implementation of a Minecraft Realms server for Java Edition",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5192"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
@app.on_event("startup")
async def startup_event():
    """Initialize the application on startup"""
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Initialize configuration
    db = SessionLocal()
    try:
        ConfigHelper.initialize(db)
    finally:
        db.close()
    
    # Check if docker is running
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            check=False
        )
        if result.returncode != 0:
            print("Docker is required to run, but its daemon is not running.")
            sys.exit(1)
    except FileNotFoundError:
        print("Docker is required to run, but it is not installed")
        print("You can install it here: https://docs.docker.com/engine/install")
        sys.exit(1)
    
    print("Running Minecraft Realms Emulator")


# Import and include routers
from app.controllers import worlds, activities, invites, mco, notifications
from app.controllers import ops, regions, subscriptions, trial, upload, feature
from app.controllers.admin import configuration, servers

app.include_router(worlds.router, prefix="/worlds", tags=["worlds"])
app.include_router(activities.router, prefix="/activities", tags=["activities"])
app.include_router(invites.router, prefix="/invites", tags=["invites"])
app.include_router(mco.router, prefix="/mco", tags=["mco"])
app.include_router(notifications.router, prefix="/notifications", tags=["notifications"])
app.include_router(ops.router, prefix="/ops", tags=["ops"])
app.include_router(regions.router, prefix="/regions", tags=["regions"])
app.include_router(subscriptions.router, prefix="/subscriptions", tags=["subscriptions"])
app.include_router(trial.router, prefix="/trial", tags=["trial"])
app.include_router(upload.router, prefix="/upload", tags=["upload"])
app.include_router(feature.router, prefix="/feature", tags=["feature"])
app.include_router(configuration.router, prefix="/admin/configuration", tags=["admin"])
app.include_router(servers.router, prefix="/admin/servers", tags=["admin"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
