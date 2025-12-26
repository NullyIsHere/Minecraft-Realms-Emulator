from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models import get_db
from app.middleware.dependencies import require_admin_key
from app.helpers.config_helper import ConfigHelper

router = APIRouter()


@router.get("")
async def get_configuration(
    admin_key: str = Depends(require_admin_key),
    db: Session = Depends(get_db)
):
    """Get configuration"""
    return ConfigHelper.get_config()


@router.post("")
async def update_configuration(
    config: dict,
    admin_key: str = Depends(require_admin_key),
    db: Session = Depends(get_db)
):
    """Update configuration"""
    for key, value in config.items():
        ConfigHelper.set_setting(db, key, value)
    return {"success": True}
