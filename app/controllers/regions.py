from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models import get_db
from app.middleware.dependencies import require_minecraft_cookie

router = APIRouter()


@router.get("/ping/stat")
async def ping_regions(
    cookie: str = Depends(require_minecraft_cookie),
    db: Session = Depends(get_db)
):
    """Ping regions"""
    return {"regions": []}
