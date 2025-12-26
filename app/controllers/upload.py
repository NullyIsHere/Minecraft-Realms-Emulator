from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models import get_db
from app.middleware.dependencies import require_minecraft_cookie

router = APIRouter()


@router.put("/{world_id}/{slot_id}")
async def upload_world(
    world_id: int,
    slot_id: int,
    cookie: str = Depends(require_minecraft_cookie),
    db: Session = Depends(get_db)
):
    """Upload world"""
    return {"uploadUrl": ""}
