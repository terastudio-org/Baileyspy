"""
Baileyspy - Python Wrapper for Baileys WhatsApp Library

A comprehensive Python wrapper for the Baileys JavaScript WhatsApp library,
providing easy-to-use interfaces for WhatsApp automation and bot development.

Author: MiniMax Agent
Version: 1.0.0
License: MIT
"""

from .client import BaileysClient
from .connection import ConnectionManager
from .messages import MessageHandler
from .groups import GroupManager
from .call_manager import CallManager
from .pairing import PairingManager
from .media import MediaHandler
from .utils import Utils

__version__ = "1.0.0"
__author__ = "MiniMax Agent"

__all__ = [
    "BaileysClient",
    "ConnectionManager", 
    "MessageHandler",
    "GroupManager",
    "CallManager",
    "PairingManager",
    "MediaHandler",
    "Utils",
    "create_client"
]


def create_client(session_id: str | None = None, config: dict | None = None) -> BaileysClient:
    """
    Create and configure a new BaileysClient instance.
    
    Args:
        session_id (str | None): Unique identifier for the session
        config (dict | None): Configuration settings
        
    Returns:
        BaileysClient: Configured client instance
        
    Example:
        >>> client = create_client("my_bot_session", {"debug": True})
        >>> await client.connect()
    """
    return BaileysClient(session_id=session_id, config=config or {})

# Package metadata
PACKAGE_INFO = {
    "name": "baileyspy",
    "version": __version__,
    "description": "Python wrapper for Baileys WhatsApp library",
    "author": __author__,
    "license": "MIT",
    "keywords": ["whatsapp", "bot", "automation", "wrapper", "api"],
    "python_requires": ">=3.14.0",
    "dependencies": [
        "requests>=2.31.0",
        "websocket-client>=1.7.0",
        "aiofiles>=23.0.0",
        "python-dotenv>=1.0.0"
    ]
}