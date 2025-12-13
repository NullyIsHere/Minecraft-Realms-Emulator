from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from app.models import Base
from app.models.enums import GamemodeEnum, DifficultyEnum


class World(Base):
    __tablename__ = "Worlds"

    Id = Column(Integer, primary_key=True, index=True)
    Owner = Column(String, nullable=True)
    OwnerUUID = Column(String, nullable=True)
    Name = Column(String, nullable=True)
    Motd = Column(String, nullable=True)
    WorldType = Column(String, default="NORMAL")
    MaxPlayers = Column(Integer, default=10)
    Member = Column(Boolean, default=False)
    RegionSelectionPreference = Column(JSONB, nullable=True)

    # Foreign Keys
    SubscriptionId = Column(Integer, ForeignKey("Subscriptions.Id"), nullable=True)
    MinigameId = Column(Integer, ForeignKey("Templates.Id"), nullable=True)
    ActiveSlotId = Column(Integer, ForeignKey("Slots.Id"), nullable=True)
    ParentWorldId = Column(Integer, ForeignKey("Worlds.Id"), nullable=True)

    # Relationships
    Subscription = relationship("Subscription", back_populates="World", foreign_keys=[SubscriptionId])
    Minigame = relationship("Template")
    ActiveSlot = relationship("Slot", foreign_keys=[ActiveSlotId], post_update=True)
    Slots = relationship("Slot", back_populates="World", foreign_keys="Slot.WorldId")
    Players = relationship("Player", back_populates="World")
    ParentWorld = relationship("World", remote_side=[Id])


class Subscription(Base):
    __tablename__ = "Subscriptions"

    Id = Column(Integer, primary_key=True, index=True)
    WorldId = Column(Integer, ForeignKey("Worlds.Id"))
    StartDate = Column(DateTime, default=datetime.utcnow)
    SubscriptionType = Column(String, nullable=False)

    # Relationships
    World = relationship("World", back_populates="Subscription", foreign_keys=[WorldId])


class Player(Base):
    __tablename__ = "Players"

    Id = Column(Integer, primary_key=True, index=True)
    Name = Column(String, default="")
    Uuid = Column(String, default="")
    Operator = Column(Boolean, default=False)
    Accepted = Column(Boolean, default=False)
    Online = Column(Boolean, default=False)
    Permission = Column(String, default="MEMBER")
    WorldId = Column(Integer, ForeignKey("Worlds.Id"), nullable=False)

    # Relationships
    World = relationship("World", back_populates="Players")


class Slot(Base):
    __tablename__ = "Slots"

    Id = Column(Integer, primary_key=True, index=True)
    WorldId = Column(Integer, ForeignKey("Worlds.Id"), nullable=False)
    SlotId = Column(Integer, nullable=False)
    SlotName = Column(String, default="")
    Version = Column(String, nullable=False)
    Difficulty = Column(Integer, default=DifficultyEnum.Normal)
    GameMode = Column(Integer, default=GamemodeEnum.Survival)
    ForceGameMode = Column(Boolean, default=False)
    SpawnProtection = Column(Integer, default=0)
    Hardcore = Column(Boolean, default=False)

    # Relationships
    World = relationship("World", back_populates="Slots", foreign_keys=[WorldId])
    Backups = relationship("Backup", back_populates="Slot")


class Backup(Base):
    __tablename__ = "Backups"

    Id = Column(Integer, primary_key=True, index=True)
    SlotId = Column(Integer, ForeignKey("Slots.Id"), nullable=False)
    BackupId = Column(String, nullable=False)
    LastModifiedDate = Column(DateTime, default=datetime.utcnow)
    Size = Column(Integer, default=0)
    Metadata = Column(JSONB, nullable=False)
    DownloadUrl = Column(String, nullable=False)
    ResourcePackUrl = Column(String, nullable=True)
    ResourcePackHash = Column(String, nullable=True)

    # Relationships
    Slot = relationship("Slot", back_populates="Backups")


class Invite(Base):
    __tablename__ = "Invites"

    Id = Column(Integer, primary_key=True, index=True)
    InvitationId = Column(String, nullable=False)
    RecipientUuid = Column(String, nullable=False)
    WorldId = Column(Integer, ForeignKey("Worlds.Id"), nullable=False)
    Date = Column(DateTime, default=datetime.utcnow)

    # Relationships
    World = relationship("World")


class Configuration(Base):
    __tablename__ = "Configuration"

    Key = Column(String, primary_key=True)
    Value = Column(JSONB, nullable=False)


class Template(Base):
    __tablename__ = "Templates"

    Id = Column(Integer, primary_key=True, index=True)
    Name = Column(String, default="")
    Version = Column(String, default="")
    Author = Column(String, default="")
    Link = Column(String, default="")
    Image = Column(String, nullable=True)
    Trailer = Column(String, default="")
    RecommendedPlayers = Column(String, default="")
    Type = Column(String, nullable=False)


class Notification(Base):
    __tablename__ = "Notifications"

    Id = Column(Integer, primary_key=True, index=True)
    NotificationUuid = Column(String, nullable=False)
    Dismissable = Column(Boolean, default=False)
    Type = Column(String, nullable=False)
    Title = Column(JSONB, nullable=True)
    Message = Column(JSONB, nullable=False)
    Image = Column(String, nullable=True)
    UrlButton = Column(JSONB, nullable=True)
    Url = Column(String, nullable=True)
    ButtonText = Column(JSONB, nullable=True)


class SeenNotification(Base):
    __tablename__ = "SeenNotifications"

    Id = Column(Integer, primary_key=True, index=True)
    PlayerUUID = Column(String, nullable=False)
    NotificationUUID = Column(String, nullable=False)
