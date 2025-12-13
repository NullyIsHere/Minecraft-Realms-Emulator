import re
from typing import Optional


class MinecraftVersion:
    def __init__(self, version: str):
        self.major: int = 0
        self.minor: int = 0
        self.patch: int = 0
        self.pre_release: Optional[str] = None
        self.snapshot: Optional[str] = None
        
        version_regex = re.compile(
            r'^(\d+)\.(\d+)(\.(\d+))?(-[a-zA-Z0-9\-]+)?$|^(\d{2})w(\d{2})([a-z])$'
        )
        
        match = version_regex.match(version)
        if not match:
            raise ValueError(f"Invalid version format: {version}")
        
        if match.group(1):
            self.major = int(match.group(1))
            self.minor = int(match.group(2))
            self.patch = int(match.group(4)) if match.group(4) else 0
            self.pre_release = match.group(5)[1:] if match.group(5) else None
        elif match.group(6):
            self.major = 0
            self.minor = int(match.group(6))
            self.patch = int(match.group(7))
            self.snapshot = match.group(8)
    
    def __lt__(self, other: 'MinecraftVersion') -> bool:
        return self._compare_to(other) < 0
    
    def __le__(self, other: 'MinecraftVersion') -> bool:
        return self._compare_to(other) <= 0
    
    def __gt__(self, other: 'MinecraftVersion') -> bool:
        return self._compare_to(other) > 0
    
    def __ge__(self, other: 'MinecraftVersion') -> bool:
        return self._compare_to(other) >= 0
    
    def __eq__(self, other: 'MinecraftVersion') -> bool:
        return self._compare_to(other) == 0
    
    def _compare_to(self, other: 'MinecraftVersion') -> int:
        if other is None:
            return 1
        
        # Both are snapshots
        if self.snapshot and other.snapshot:
            if self.minor != other.minor:
                return -1 if self.minor < other.minor else 1
            if self.patch != other.patch:
                return -1 if self.patch < other.patch else 1
            if self.snapshot < other.snapshot:
                return -1
            elif self.snapshot > other.snapshot:
                return 1
            return 0
        
        # One is snapshot
        if self.snapshot:
            return -1
        if other.snapshot:
            return 1
        
        # Compare major, minor, patch
        if self.major != other.major:
            return -1 if self.major < other.major else 1
        if self.minor != other.minor:
            return -1 if self.minor < other.minor else 1
        if self.patch != other.patch:
            return -1 if self.patch < other.patch else 1
        
        # Compare pre-release
        if self.pre_release is None and other.pre_release is None:
            return 0
        if self.pre_release is None:
            return 1
        if other.pre_release is None:
            return -1
        
        if self.pre_release < other.pre_release:
            return -1
        elif self.pre_release > other.pre_release:
            return 1
        return 0
