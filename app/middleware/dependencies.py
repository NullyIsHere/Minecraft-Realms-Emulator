import os
from fastapi import Header, HTTPException, Depends, Request
from typing import Optional
from sqlalchemy.orm import Session
from app.models import get_db
from app.models.entities import World


def require_minecraft_cookie(cookie: Optional[str] = Header(None)) -> str:
    """Dependency to require Minecraft cookie"""
    if not cookie:
        raise HTTPException(status_code=401, detail="Authorization required")
    
    if not ("sid" in cookie and "user" in cookie and "version" in cookie):
        raise HTTPException(status_code=401, detail="Malformed cookie header")
    
    return cookie


def require_admin_key(authorization: Optional[str] = Header(None)) -> str:
    """Dependency to require admin key"""
    admin_key = os.getenv("ADMIN_KEY")
    if not authorization or authorization != admin_key:
        raise HTTPException(status_code=403, detail="You don't have access to this resource")
    
    return authorization


def check_realm_owner(
    world_id: int,
    cookie: str = Depends(require_minecraft_cookie),
    db: Session = Depends(get_db)
) -> World:
    """Dependency to check if user is realm owner"""
    player_uuid = cookie.split(";")[0].split(":")[2]
    
    world = db.query(World).filter(World.Id == world_id).first()
    if not world:
        raise HTTPException(status_code=404, detail="World not found")
    
    if world.OwnerUUID != player_uuid:
        raise HTTPException(status_code=403, detail="You don't own this world")
    
    return world


def check_active_subscription(
    world: World = Depends(check_realm_owner)
) -> World:
    """Dependency to check if world has active subscription"""
    if not world.Subscription:
        raise HTTPException(status_code=403, detail="No active subscription")
    
    return world


def check_for_world(
    world_id: int,
    db: Session = Depends(get_db)
) -> World:
    """Dependency to check if world exists"""
    world = db.query(World).filter(World.Id == world_id).first()
    if not world:
        raise HTTPException(status_code=404, detail="World not found")
    
    return world


def get_player_info(cookie: str = Depends(require_minecraft_cookie)) -> dict:
    """Extract player information from cookie"""
    player_uuid = cookie.split(";")[0].split(":")[2]
    player_name = cookie.split(";")[1].split("=")[1]
    game_version = cookie.split(";")[2].split("=")[1]
    
    return {
        "uuid": player_uuid,
        "name": player_name,
        "version": game_version
    }
