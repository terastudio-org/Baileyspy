"""
BaileysClient - Main client class for Baileyspy wrapper

This module provides the primary interface for interacting with WhatsApp
through the Baileys library using Python.

Author: MiniMax Agent
"""

import asyncio
import json
import logging
import os
from typing import Optional, Dict, Any, Callable, List
from datetime import datetime
import aiofiles
from dotenv import load_dotenv

from .connection import ConnectionManager
from .messages import MessageHandler
from .groups import GroupManager
from .call_manager import CallManager
from .pairing import PairingManager
from .media import MediaHandler
from .utils import Utils

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class BaileysClient:
    """
    Main client class for Baileyspy wrapper.
    
    This class provides a comprehensive interface to interact with WhatsApp
    using the Baileys library. It handles connection management, message sending,
    group operations, and various WhatsApp features.
    
    Attributes:
        session_id (str): Unique identifier for the session
        is_connected (bool): Connection status
        phone_number (str): Associated phone number
        config (dict): Configuration settings
        
    Example:
        >>> client = BaileysClient(session_id="my_bot")
        >>> await client.connect()
        >>> await client.send_message("1234567890", "Hello World!")
    """
    
    def __init__(self, session_id: str = None, config: Dict[str, Any] = None):
        """
        Initialize the BaileysClient.
        
        Args:
            session_id (str, optional): Unique identifier for the session
            config (dict, optional): Configuration settings
        """
        self.session_id = session_id or f"baileyspy_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.is_connected = False
        self.phone_number = None
        self.config = config or {}
        
        # Initialize handlers
        self.connection_manager = ConnectionManager(self.config)
        self.message_handler = MessageHandler()
        self.group_manager = GroupManager()
        self.call_manager = CallManager()
        self.pairing_manager = PairingManager()
        self.media_handler = MediaHandler()
        self.utils = Utils()
        
        # Event handlers
        self.event_handlers = {}
        
        # Load configuration
        self._load_config()
        
        logger.info(f"BaileysClient initialized with session_id: {self.session_id}")
    
    def _load_config(self):
        """Load configuration from environment variables and config dict."""
        self.config.update({
            'session_dir': self.config.get('session_dir', f'sessions/{self.session_id}'),
            'qr_timeout': self.config.get('qr_timeout', 30),
            'message_timeout': self.config.get('message_timeout', 30),
            'pairing_code': self.config.get('pairing_code'),
            'is_bot': self.config.get('is_bot', True),
            'connection_retries': self.config.get('connection_retries', 3)
        })
        
        # Create session directory
        os.makedirs(self.config['session_dir'], exist_ok=True)
    
    async def connect(self, pairing_code: str = None) -> Dict[str, Any]:
        """
        Establish connection to WhatsApp.
        
        Args:
            pairing_code (str, optional): Custom pairing code for authentication
            
        Returns:
            Dict[str, Any]: Connection information including QR code if needed
            
        Raises:
            ConnectionError: If connection fails after retries
        """
        try:
            logger.info("Attempting to connect to WhatsApp...")
            
            # Use provided pairing code or generate one
            code = pairing_code or self.config.get('pairing_code') or 'AAAAAAAA'
            
            # Initialize connection
            connection_info = await self.connection_manager.connect(
                session_id=self.session_id,
                pairing_code=code
            )
            
            if connection_info.get('status') == 'qr_required':
                self.is_connected = False
                logger.info("QR code required for authentication")
                return {
                    'status': 'qr_required',
                    'qr_code': connection_info.get('qr_code'),
                    'session_id': self.session_id
                }
            
            elif connection_info.get('status') == 'connected':
                self.is_connected = True
                self.phone_number = connection_info.get('phone_number')
                logger.info(f"Successfully connected to WhatsApp with number: {self.phone_number}")
                
                # Start event listeners
                await self._start_event_listeners()
                
                return {
                    'status': 'connected',
                    'phone_number': self.phone_number,
                    'session_id': self.session_id
                }
                
        except Exception as e:
            logger.error(f"Connection failed: {str(e)}")
            raise ConnectionError(f"Failed to connect to WhatsApp: {str(e)}")
    
    async def disconnect(self):
        """Disconnect from WhatsApp."""
        try:
            if self.is_connected:
                await self.connection_manager.disconnect()
                self.is_connected = False
                self.phone_number = None
                logger.info("Disconnected from WhatsApp")
        except Exception as e:
            logger.error(f"Error during disconnect: {str(e)}")
    
    async def send_message(self, jid: str, message: str, **kwargs) -> Dict[str, Any]:
        """
        Send a text message.
        
        Args:
            jid (str): WhatsApp JID (e.g., "1234567890@s.whatsapp.net")
            message (str): Message text to send
            **kwargs: Additional message options
            
        Returns:
            Dict[str, Any]: Send result information
        """
        if not self.is_connected:
            raise ConnectionError("Not connected to WhatsApp")
        
        try:
            result = await self.message_handler.send_text_message(
                jid=jid,
                message=message,
                client=self.connection_manager,
                **kwargs
            )
            
            logger.info(f"Message sent to {jid}")
            return result
            
        except Exception as e:
            logger.error(f"Failed to send message: {str(e)}")
            raise
    
    async def send_media(self, jid: str, media_path: str, media_type: str = None, **kwargs) -> Dict[str, Any]:
        """
        Send media file (image, video, document, etc.).
        
        Args:
            jid (str): WhatsApp JID
            media_path (str): Path to media file
            media_type (str, optional): Type of media ('image', 'video', 'document', etc.)
            **kwargs: Additional options
            
        Returns:
            Dict[str, Any]: Send result information
        """
        if not self.is_connected:
            raise ConnectionError("Not connected to WhatsApp")
        
        try:
            result = await self.media_handler.send_media(
                jid=jid,
                media_path=media_path,
                media_type=media_type,
                client=self.connection_manager,
                **kwargs
            )
            
            logger.info(f"Media sent to {jid}")
            return result
            
        except Exception as e:
            logger.error(f"Failed to send media: {str(e)}")
            raise
    
    async def offer_call(self, jid: str) -> Dict[str, Any]:
        """
        Initiate a call to a specific JID.
        
        Args:
            jid (str): WhatsApp JID to call
            
        Returns:
            Dict[str, Any]: Call information
        """
        if not self.is_connected:
            raise ConnectionError("Not connected to WhatsApp")
        
        try:
            result = await self.call_manager.offer_call(jid, self.connection_manager)
            logger.info(f"Call offered to {jid}")
            return result
            
        except Exception as e:
            logger.error(f"Failed to offer call: {str(e)}")
            raise
    
    async def get_groups(self) -> List[Dict[str, Any]]:
        """
        Get list of all groups the client is part of.
        
        Returns:
            List[Dict[str, Any]]: List of group information
        """
        if not self.is_connected:
            raise ConnectionError("Not connected to WhatsApp")
        
        try:
            groups = await self.group_manager.get_groups(self.connection_manager)
            logger.info(f"Retrieved {len(groups)} groups")
            return groups
            
        except Exception as e:
            logger.error(f"Failed to get groups: {str(e)}")
            raise
    
    async def create_group(self, name: str, participants: List[str]) -> Dict[str, Any]:
        """
        Create a new group.
        
        Args:
            name (str): Group name
            participants (List[str]): List of participant JIDs
            
        Returns:
            Dict[str, Any]: Created group information
        """
        if not self.is_connected:
            raise ConnectionError("Not connected to WhatsApp")
        
        try:
            result = await self.group_manager.create_group(
                name=name,
                participants=participants,
                client=self.connection_manager
            )
            
            logger.info(f"Group '{name}' created with {len(participants)} participants")
            return result
            
        except Exception as e:
            logger.error(f"Failed to create group: {str(e)}")
            raise
    
    async def get_profile_info(self, jid: str) -> Dict[str, Any]:
        """
        Get profile information for a specific JID.
        
        Args:
            jid (str): WhatsApp JID
            
        Returns:
            Dict[str, Any]: Profile information
        """
        try:
            result = await self.message_handler.get_profile_info(jid, self.connection_manager)
            return result
            
        except Exception as e:
            logger.error(f"Failed to get profile info: {str(e)}")
            raise
    
    async def set_profile_picture(self, image_path: str) -> Dict[str, Any]:
        """
        Set profile picture.
        
        Args:
            image_path (str): Path to image file
            
        Returns:
            Dict[str, Any]: Update result
        """
        if not self.is_connected:
            raise ConnectionError("Not connected to WhatsApp")
        
        try:
            result = await self.media_handler.set_profile_picture(
                image_path=image_path,
                client=self.connection_manager
            )
            
            logger.info("Profile picture updated")
            return result
            
        except Exception as e:
            logger.error(f"Failed to set profile picture: {str(e)}")
            raise
    
    def on(self, event: str, handler: Callable):
        """
        Register an event handler.
        
        Args:
            event (str): Event name ('message', 'qr', 'connected', etc.)
            handler (Callable): Handler function
        """
        if event not in self.event_handlers:
            self.event_handlers[event] = []
        
        self.event_handlers[event].append(handler)
        logger.info(f"Event handler registered for '{event}'")
    
    async def _start_event_listeners(self):
        """Start listening for events."""
        try:
            # Start message listeners
            await self.message_handler.start_listeners(
                client=self.connection_manager,
                event_handlers=self.event_handlers
            )
            
            # Start connection listeners
            await self.connection_manager.start_listeners(
                event_handlers=self.event_handlers
            )
            
        except Exception as e:
            logger.error(f"Failed to start event listeners: {str(e)}")
    
    async def save_session(self, file_path: str = None):
        """
        Save session information to file.
        
        Args:
            file_path (str, optional): Custom file path
        """
        if not file_path:
            file_path = f"{self.config['session_dir']}/session.json"
        
        session_data = {
            'session_id': self.session_id,
            'phone_number': self.phone_number,
            'is_connected': self.is_connected,
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            async with aiofiles.open(file_path, 'w') as f:
                await f.write(json.dumps(session_data, indent=2))
            
            logger.info(f"Session saved to {file_path}")
            
        except Exception as e:
            logger.error(f"Failed to save session: {str(e)}")
            raise
    
    async def load_session(self, file_path: str = None):
        """
        Load session information from file.
        
        Args:
            file_path (str, optional): Custom file path
        """
        if not file_path:
            file_path = f"{self.config['session_dir']}/session.json"
        
        try:
            async with aiofiles.open(file_path, 'r') as f:
                content = await f.read()
                session_data = json.loads(content)
            
            self.session_id = session_data.get('session_id', self.session_id)
            self.phone_number = session_data.get('phone_number')
            self.is_connected = session_data.get('is_connected', False)
            
            logger.info(f"Session loaded from {file_path}")
            
        except Exception as e:
            logger.error(f"Failed to load session: {str(e)}")
            raise
    
    def get_connection_info(self) -> Dict[str, Any]:
        """
        Get current connection information.
        
        Returns:
            Dict[str, Any]: Connection information
        """
        return {
            'session_id': self.session_id,
            'is_connected': self.is_connected,
            'phone_number': self.phone_number,
            'config': self.config
        }
    
    async def __aenter__(self):
        """Async context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.disconnect()


# Factory function for easy instantiation
def create_client(session_id: str = None, config: Dict[str, Any] = None) -> BaileysClient:
    """
    Create a BaileysClient instance.
    
    Args:
        session_id (str, optional): Unique identifier for the session
        config (dict, optional): Configuration settings
        
    Returns:
        BaileysClient: Configured client instance
    """
    return BaileysClient(session_id=session_id, config=config)