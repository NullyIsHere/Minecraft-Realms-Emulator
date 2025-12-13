from enum import Enum, IntEnum


class GamemodeEnum(IntEnum):
    Survival = 0
    Creative = 1
    Adventure = 2


class DifficultyEnum(IntEnum):
    Peaceful = 0
    Easy = 1
    Normal = 2
    Hard = 3


class StateEnum(str, Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    UNINITIALIZED = "UNINITIALIZED"


class WorldTypeEnum(str, Enum):
    NORMAL = "NORMAL"
    MINIGAME = "MINIGAME"
    ADVENTUREMAP = "ADVENTUREMAP"
    EXPERIENCE = "EXPERIENCE"
    INSPIRATION = "INSPIRATION"


class CompatibilityEnum(str, Enum):
    UNVERIFIABLE = "UNVERIFIABLE"
    INCOMPATIBLE = "INCOMPATIBLE"
    NEEDS_DOWNGRADE = "NEEDS_DOWNGRADE"
    NEEDS_UPGRADE = "NEEDS_UPGRADE"
    COMPATIBLE = "COMPATIBLE"


class SubscriptionTypeEnum(str, Enum):
    NORMAL = "NORMAL"
    RECURRING = "RECURRING"


class VersionCompatibilityEnum(str, Enum):
    COMPATIBLE = "COMPATIBLE"
    OUTDATED = "OUTDATED"
    OTHER = "OTHER"


class WorldTemplateTypeEnum(str, Enum):
    WORLD_TEMPLATE = "WORLD_TEMPLATE"
    MINIGAME = "MINIGAME"
    ADVENTUREMAP = "ADVENTUREMAP"
    EXPERIENCE = "EXPERIENCE"
    INSPIRATION = "INSPIRATION"


class RegionEnum(IntEnum):
    AustraliaEast = 0
    AustraliaSoutheast = 1
    BrazilSouth = 2
    CentralIndia = 3
    CentralUs = 4
    EastAsia = 5
    EastUs = 6
    EastUs2 = 7
    FranceCentral = 8
    JapanEast = 9
    JapanWest = 10
    KoreaCentral = 11
    NorthCentralUs = 12
    NorthEurope = 13
    SouthCentralUs = 14
    SoutheastAsia = 15
    SwedenCentral = 16
    UAENorth = 17
    UKSouth = 18
    WestCentralUs = 19
    WestEurope = 20
    WestUs = 21
    WestUs2 = 22


class RegionSelectionPreferenceEnum(IntEnum):
    AutomaticPlayer = 0
    AutomaticOwner = 1
    Manual = 2


class RegionServiceQualityEnum(IntEnum):
    Great = 1
    Good = 2
    Okay = 3
    Poor = 4
    Unknown = 5


class SettingsEnum(str, Enum):
    NewsLink = "NewsLink"
    DefaultServerAddress = "DefaultServerAddress"
    TrialMode = "TrialMode"
    OnlineMode = "OnlineMode"
    AutomaticRealmsCreation = "AutomaticRealmsCreation"
