from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models import get_db
from app.models.entities import World
from app.middleware.dependencies import require_admin_key

router = APIRouter()


@router.get("")
async def get_all_servers(
    admin_key: str = Depends(require_admin_key),
    db: Session = Depends(get_db)
):
    """Get all servers (admin)"""
    worlds = db.query(World).all()
    return {
        "servers": [
            {
                "id": world.Id,
                "owner": world.Owner,
                "ownerUUID": world.OwnerUUID,
                "name": world.Name,
                "motd": world.Motd
            }
            for world in worlds
        ]
    }
