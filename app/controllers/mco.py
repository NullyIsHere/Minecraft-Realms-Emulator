from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models import get_db
from app.middleware.dependencies import require_minecraft_cookie

router = APIRouter()


@router.get("/available")
async def check_available(
    cookie: str = Depends(require_minecraft_cookie),
    db: Session = Depends(get_db)
):
    """Check if MCO is available"""
    return True


@router.get("/client/outdated")
async def check_client_outdated(
    cookie: str = Depends(require_minecraft_cookie),
    db: Session = Depends(get_db)
):
    """Check if client is outdated"""
    return False


@router.get("/tos/agreed")
async def check_tos_agreed(
    cookie: str = Depends(require_minecraft_cookie),
    db: Session = Depends(get_db)
):
    """Check if TOS is agreed"""
    return True


@router.get("/v1/news")
async def get_news(
    cookie: str = Depends(require_minecraft_cookie),
    db: Session = Depends(get_db)
):
    """Get news"""
    from app.helpers.config_helper import ConfigHelper
    return {"newsLink": ConfigHelper.get_setting("NewsLink") or ""}
