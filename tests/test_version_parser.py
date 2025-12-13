import pytest
from app.helpers.minecraft_version_parser import MinecraftVersion


def test_version_parsing():
    """Test that version parsing works correctly"""
    v1 = MinecraftVersion("1.20.1")
    assert v1.major == 1
    assert v1.minor == 20
    assert v1.patch == 1
    
    v2 = MinecraftVersion("1.19")
    assert v2.major == 1
    assert v2.minor == 19
    assert v2.patch == 0


def test_version_comparison():
    """Test version comparison"""
    v1 = MinecraftVersion("1.20.1")
    v2 = MinecraftVersion("1.19.4")
    v3 = MinecraftVersion("1.20.1")
    
    assert v1 > v2
    assert v2 < v1
    assert v1 == v3


def test_snapshot_version():
    """Test snapshot version parsing"""
    snap = MinecraftVersion("23w31a")
    assert snap.major == 0
    assert snap.minor == 23
    assert snap.patch == 31
    assert snap.snapshot == "a"


def test_invalid_version():
    """Test that invalid version raises error"""
    with pytest.raises(ValueError):
        MinecraftVersion("invalid")
