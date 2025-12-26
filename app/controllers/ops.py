from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models import get_db
from app.middleware.dependencies import require_minecraft_cookie

router = APIRouter()


@router.get("/{world_id}")
async def get_ops(
    world_id: int,
    cookie: str = Depends(require_minecraft_cookie),
    db: Session = Depends(get_db)
):
    """Get operators for a world"""
    return {"ops": []}
