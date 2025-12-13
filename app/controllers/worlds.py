from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from datetime import datetime, timedelta

from app.models import get_db
from app.models.entities import World, Player, Slot
from app.models.enums import GamemodeEnum, CompatibilityEnum, SettingsEnum, WorldTypeEnum
from app.schemas.responses import WorldResponse, ServersResponse, SlotResponse, PlayerResponse
from app.schemas.requests import WorldCreateRequest, UpdateWorldConfigurationRequest, SlotOptionsRequest
from app.middleware.dependencies import require_minecraft_cookie, get_player_info, check_realm_owner
from app.helpers.minecraft_version_parser import MinecraftVersion
from app.helpers.world_helper import WorldHelper
from app.helpers.config_helper import ConfigHelper
from app.helpers.docker_helper import DockerHelper

router = APIRouter()


@router.get("", response_model=ServersResponse)
async def get_stable_worlds(
    player_info: dict = Depends(get_player_info),
    db: Session = Depends(get_db)
):
    """Get all stable worlds for the player"""
    player_uuid = player_info["uuid"]
    player_name = player_info["name"]
    game_version = player_info["version"]
    
    # Get owned worlds
    owned_worlds = db.query(World).filter(
        World.OwnerUUID == player_uuid
    ).options(
        joinedload(World.Subscription),
        joinedload(World.Slots),
        joinedload(World.ActiveSlot),
        joinedload(World.Minigame),
        joinedload(World.Players)
    ).all()
    
    # Get member worlds
    member_worlds = db.query(World).join(Player).filter(
        Player.Uuid == player_uuid,
        Player.Accepted == True
    ).options(
        joinedload(World.Subscription),
        joinedload(World.Slots),
        joinedload(World.ActiveSlot),
        joinedload(World.Minigame),
        joinedload(World.Players)
    ).all()
    
    # Auto-create realm if enabled and no worlds exist
    if len(owned_worlds) == 0 and ConfigHelper.get_setting(SettingsEnum.AutomaticRealmsCreation.value):
        world = World(
            Owner=player_name,
            OwnerUUID=player_uuid,
            Name=None,
            Motd=None,
            WorldType=WorldTypeEnum.NORMAL.value,
            MaxPlayers=10,
            Minigame=None,
            ActiveSlot=None,
            Member=False
        )
        db.add(world)
        db.commit()
        db.refresh(world)
        owned_worlds.append(world)
    
    all_worlds = []
    
    # Process owned worlds
    for world in owned_worlds:
        active_version = world.ActiveSlot.Version if world.ActiveSlot else game_version
        game_ver = MinecraftVersion(game_version)
        active_ver = MinecraftVersion(active_version)
        
        if game_ver == active_ver:
            versions_compared = 0
        elif game_ver < active_ver:
            versions_compared = -1
        else:
            versions_compared = 1
        
        is_compatible = (
            CompatibilityEnum.COMPATIBLE.value if versions_compared == 0 else
            CompatibilityEnum.NEEDS_DOWNGRADE.value if versions_compared < 0 else
            CompatibilityEnum.NEEDS_UPGRADE.value
        )
        
        world_helper = WorldHelper(db, world.Id)
        state = await world_helper.get_state()
        
        response = WorldResponse(
            Id=world.Id,
            Owner=world.Owner,
            OwnerUUID=world.OwnerUUID,
            Name=world.Name,
            Motd=world.Motd,
            GameMode=world.ActiveSlot.GameMode if world.ActiveSlot else GamemodeEnum.Survival,
            IsHardcore=world.ActiveSlot.Hardcore if world.ActiveSlot else False,
            State=state,
            WorldType=world.WorldType,
            MaxPlayers=world.MaxPlayers,
            ActiveSlot=world.ActiveSlot.SlotId if world.ActiveSlot else 1,
            Member=world.Member,
            Players=[PlayerResponse.model_validate(p) for p in world.Players],
            ActiveVersion=active_version,
            Compatibility=is_compatible
        )
        
        if world.Minigame:
            response.MinigameId = world.Minigame.Id
            response.MinigameName = world.Minigame.Name
            response.MinigameImage = world.Minigame.Image
        
        if world.Subscription:
            days_left = (world.Subscription.StartDate + timedelta(days=30) - datetime.now()).days
            response.DaysLeft = days_left
            response.Expired = days_left < 0
            response.ExpiredTrial = False
        
        all_worlds.append(response)
    
    # Process member worlds
    for world in member_worlds:
        if not world.ActiveSlot or not world.Subscription:
            continue
        
        game_ver = MinecraftVersion(game_version)
        active_ver = MinecraftVersion(world.ActiveSlot.Version)
        
        if game_ver == active_ver:
            versions_compared = 0
        elif game_ver < active_ver:
            versions_compared = -1
        else:
            versions_compared = 1
        is_compatible = (
            CompatibilityEnum.COMPATIBLE.value if versions_compared == 0 else
            CompatibilityEnum.NEEDS_DOWNGRADE.value if versions_compared < 0 else
            CompatibilityEnum.NEEDS_UPGRADE.value
        )
        
        world_helper = WorldHelper(db, world.Id)
        state = await world_helper.get_state()
        
        response = WorldResponse(
            Id=world.Id,
            Owner=world.Owner,
            OwnerUUID=world.OwnerUUID,
            Name=world.Name,
            Motd=world.Motd,
            GameMode=world.ActiveSlot.GameMode,
            IsHardcore=world.ActiveSlot.Hardcore,
            State=state,
            WorldType=world.WorldType,
            MaxPlayers=world.MaxPlayers,
            ActiveSlot=world.ActiveSlot.SlotId,
            Member=True,
            Players=[PlayerResponse.model_validate(p) for p in world.Players],
            DaysLeft=0,
            Expired=(world.Subscription.StartDate + timedelta(days=30) - datetime.now()).days < 0,
            ExpiredTrial=False,
            ActiveVersion=world.ActiveSlot.Version,
            Compatibility=is_compatible
        )
        
        if world.Minigame:
            response.MinigameId = world.Minigame.Id
            response.MinigameName = world.Minigame.Name
            response.MinigameImage = world.Minigame.Image
        
        all_worlds.append(response)
    
    return ServersResponse(servers=all_worlds)


@router.get("/{world_id}")
async def get_world(
    world_id: int,
    player_info: dict = Depends(get_player_info),
    db: Session = Depends(get_db)
):
    """Get a specific world"""
    world = db.query(World).filter(World.Id == world_id).options(
        joinedload(World.Subscription),
        joinedload(World.Slots),
        joinedload(World.ActiveSlot),
        joinedload(World.Minigame),
        joinedload(World.Players)
    ).first()
    
    if not world:
        raise HTTPException(status_code=404, detail="World not found")
    
    game_version = player_info["version"]
    active_version = world.ActiveSlot.Version if world.ActiveSlot else game_version
    game_ver = MinecraftVersion(game_version)
    active_ver = MinecraftVersion(active_version)
    
    if game_ver == active_ver:
        versions_compared = 0
    elif game_ver < active_ver:
        versions_compared = -1
    else:
        versions_compared = 1
    
    is_compatible = (
        CompatibilityEnum.COMPATIBLE.value if versions_compared == 0 else
        CompatibilityEnum.NEEDS_DOWNGRADE.value if versions_compared < 0 else
        CompatibilityEnum.NEEDS_UPGRADE.value
    )
    
    world_helper = WorldHelper(db, world.Id)
    state = await world_helper.get_state()
    
    response = WorldResponse(
        Id=world.Id,
        Owner=world.Owner,
        OwnerUUID=world.OwnerUUID,
        Name=world.Name,
        Motd=world.Motd,
        GameMode=world.ActiveSlot.GameMode if world.ActiveSlot else GamemodeEnum.Survival,
        IsHardcore=world.ActiveSlot.Hardcore if world.ActiveSlot else False,
        State=state,
        WorldType=world.WorldType,
        MaxPlayers=world.MaxPlayers,
        ActiveSlot=world.ActiveSlot.SlotId if world.ActiveSlot else 1,
        Member=world.Member,
        Players=[PlayerResponse.model_validate(p) for p in world.Players],
        ActiveVersion=active_version,
        Compatibility=is_compatible
    )
    
    if world.Minigame:
        response.MinigameId = world.Minigame.Id
        response.MinigameName = world.Minigame.Name
        response.MinigameImage = world.Minigame.Image
    
    if world.Subscription:
        days_left = (world.Subscription.StartDate + timedelta(days=30) - datetime.now()).days
        response.DaysLeft = days_left
        response.Expired = days_left < 0
    
    return response


@router.post("")
async def create_world(
    request: WorldCreateRequest,
    player_info: dict = Depends(get_player_info),
    db: Session = Depends(get_db)
):
    """Create a new world"""
    world = World(
        Owner=player_info["name"],
        OwnerUUID=player_info["uuid"],
        Name=request.Name,
        Motd=request.Motd,
        WorldType=request.WorldType,
        MaxPlayers=10,
        Member=False
    )
    db.add(world)
    db.commit()
    db.refresh(world)
    
    return {"id": world.Id}


@router.post("/{world_id}")
async def update_world(
    world_id: int,
    request: UpdateWorldConfigurationRequest,
    world: World = Depends(check_realm_owner),
    db: Session = Depends(get_db)
):
    """Update world configuration"""
    if request.Name is not None:
        world.Name = request.Name
    if request.Motd is not None:
        world.Motd = request.Motd
    if request.WorldType is not None:
        world.WorldType = request.WorldType
    
    db.commit()
    return {"success": True}


@router.put("/{world_id}/open")
async def open_world(
    world_id: int,
    world: World = Depends(check_realm_owner),
    db: Session = Depends(get_db)
):
    """Open/start a world server"""
    if not world.ActiveSlot:
        raise HTTPException(status_code=400, detail="No active slot")
    
    docker_helper = DockerHelper(world_id)
    if not await docker_helper.is_running():
        await docker_helper.start_server(world.ActiveSlot.SlotId)
    
    return {"success": True}


@router.put("/{world_id}/close")
async def close_world(
    world_id: int,
    world: World = Depends(check_realm_owner),
    db: Session = Depends(get_db)
):
    """Close/stop a world server"""
    docker_helper = DockerHelper(world_id)
    if await docker_helper.is_running():
        await docker_helper.stop_server()
    
    return {"success": True}


@router.delete("/{world_id}")
async def delete_world(
    world_id: int,
    world: World = Depends(check_realm_owner),
    db: Session = Depends(get_db)
):
    """Delete a world"""
    docker_helper = DockerHelper(world_id)
    await docker_helper.delete_server()
    
    db.delete(world)
    db.commit()
    
    return {"success": True}
