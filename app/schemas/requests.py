from pydantic import BaseModel, Field
from typing import Optional
from app.models.enums import DifficultyEnum, GamemodeEnum


class SlotOptionsRequest(BaseModel):
    SlotName: str = ""
    Version: str
    Difficulty: DifficultyEnum = DifficultyEnum.Normal
    GameMode: GamemodeEnum = GamemodeEnum.Survival
    ForceGameMode: bool = False
    SpawnProtection: int = 0
    Hardcore: bool = False


class WorldCreateRequest(BaseModel):
    Name: Optional[str] = None
    Motd: Optional[str] = None
    WorldType: str = "NORMAL"


class UpdateWorldConfigurationRequest(BaseModel):
    Name: Optional[str] = None
    Motd: Optional[str] = None
    WorldType: Optional[str] = None


class PlayerRequest(BaseModel):
    Name: str
    Uuid: str
    Operator: bool = False
    Accepted: bool = False
    Online: bool = False
    Permission: str = "MEMBER"
