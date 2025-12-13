import json
from typing import Dict, Any
from sqlalchemy.orm import Session
from app.models.entities import Configuration


class Settings:
    """Default settings for the application"""
    NewsLink: str = ""
    DefaultServerAddress: str = "localhost"
    TrialMode: bool = False
    OnlineMode: bool = False
    AutomaticRealmsCreation: bool = True


class ConfigHelper:
    """Helper class for managing configuration"""
    _config_cache: Dict[str, Any] = {}
    
    @classmethod
    def initialize(cls, db: Session) -> None:
        """Initialize configuration from database"""
        settings = Settings()
        
        # Add default settings if they don't exist
        for key in dir(settings):
            if not key.startswith('_'):
                value = getattr(settings, key)
                existing = db.query(Configuration).filter(Configuration.Key == key).first()
                if not existing:
                    config = Configuration(Key=key, Value=json.dumps(value))
                    db.add(config)
        
        db.commit()
        
        # Load all settings into cache
        all_settings = db.query(Configuration).all()
        for setting in all_settings:
            cls._config_cache[setting.Key] = json.loads(setting.Value) if isinstance(setting.Value, str) else setting.Value
    
    @classmethod
    def get_config(cls) -> Dict[str, Any]:
        """Get all configuration"""
        return cls._config_cache
    
    @classmethod
    def get_setting(cls, key: str) -> Any:
        """Get a specific setting"""
        return cls._config_cache.get(key)
    
    @classmethod
    def set_setting(cls, db: Session, key: str, value: Any) -> None:
        """Set a specific setting"""
        cls._config_cache[key] = value
        config = db.query(Configuration).filter(Configuration.Key == key).first()
        if config:
            config.Value = json.dumps(value)
        else:
            config = Configuration(Key=key, Value=json.dumps(value))
            db.add(config)
        db.commit()
