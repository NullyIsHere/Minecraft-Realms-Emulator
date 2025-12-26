from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models import get_db
from app.middleware.dependencies import require_minecraft_cookie

router = APIRouter()


@router.get("/liveplayerlist")
async def get_live_player_list(
    cookie: str = Depends(require_minecraft_cookie),
    db: Session = Depends(get_db)
):
    """Get live player list for all worlds"""
    return {"online": []}


@router.get("/{world_id}")
async def get_world_activity(
    world_id: int,
    cookie: str = Depends(require_minecraft_cookie),
    db: Session = Depends(get_db)
):
    """Get activity for a specific world"""
    return {"playerActivityDto": {"profileUuid": "", "joinTime": 0, "leaveTime": 0}}
