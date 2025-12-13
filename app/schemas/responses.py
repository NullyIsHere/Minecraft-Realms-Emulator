from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Any
from datetime import datetime
from app.models.enums import GamemodeEnum, DifficultyEnum, StateEnum


class PlayerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    Id: int
    Name: str
    Uuid: str
    Operator: bool
    Accepted: bool
    Online: bool
    Permission: str


class SlotResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    Id: int
    SlotId: int
    SlotName: str
    Version: str
    Difficulty: DifficultyEnum
    GameMode: GamemodeEnum
    ForceGameMode: bool
    SpawnProtection: int
    Hardcore: bool


class WorldResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    Id: int
    Owner: Optional[str]
    OwnerUUID: Optional[str]
    Name: Optional[str]
    Motd: Optional[str]
    WorldType: str
    MaxPlayers: int
    Member: bool
    RemoteSubscriptionId: Optional[str] = None
    IsHardcore: bool = False
    GameMode: GamemodeEnum
    DaysLeft: int = 30
    Expired: bool = False
    ExpiredTrial: bool = False
    GracePeriod: bool = False
    Compatibility: str
    ActiveSlot: int
    Slots: Optional[List[SlotResponse]] = None
    ActiveVersion: str
    ParentWorldId: Optional[int] = None
    ParentWorldName: Optional[str] = None
    MinigameId: Optional[int] = None
    MinigameName: Optional[str] = None
    MinigameImage: Optional[str] = None
    State: str
    Players: List[PlayerResponse] = []


class ServersResponse(BaseModel):
    servers: List[WorldResponse]


class BackupResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    Id: int
    BackupId: str
    LastModifiedDate: datetime
    Size: int
    Metadata: Any
    DownloadUrl: str
    ResourcePackUrl: Optional[str] = None
    ResourcePackHash: Optional[str] = None


class BackupsResponse(BaseModel):
    backups: List[BackupResponse]


class SubscriptionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    Id: int
    StartDate: datetime
    SubscriptionType: str
    DaysLeft: int


class ConnectionResponse(BaseModel):
    address: str
    pendingUpdate: bool = False


class ErrorResponse(BaseModel):
    errorCode: int
    errorMsg: str


class InviteList(BaseModel):
    invites: List[Any]


class OpsResponse(BaseModel):
    ops: List[str]


class RegionDataListResponse(BaseModel):
    regions: List[Any]


class NotificationsResponse(BaseModel):
    notifications: List[Any]


class NewsResponse(BaseModel):
    newsLink: str


class MinecraftPlayerInfo(BaseModel):
    id: str
    name: str


class LivePlayerListsResponse(BaseModel):
    online: List[str] = []


class TemplatesResponse(BaseModel):
    templates: List[Any]


class BackupDownloadResponse(BaseModel):
    downloadLink: str
    resourcePackUrl: Optional[str] = None
    resourcePackHash: Optional[str] = None


class BackupUploadResponse(BaseModel):
    uploadUrl: str
