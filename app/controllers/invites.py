from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models import get_db
from app.middleware.dependencies import require_minecraft_cookie

router = APIRouter()


@router.get("/pending")
async def get_pending_invites(
    cookie: str = Depends(require_minecraft_cookie),
    db: Session = Depends(get_db)
):
    """Get pending invites"""
    return {"invites": []}


@router.get("/count/pending")
async def get_pending_invites_count(
    cookie: str = Depends(require_minecraft_cookie),
    db: Session = Depends(get_db)
):
    """Get count of pending invites"""
    return {"count": 0}
