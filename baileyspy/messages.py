"""
MessageHandler - Handles WhatsApp message operations

This module provides functionality for sending and receiving WhatsApp messages,
including text messages, media, and interactive messages.

Author: MiniMax Agent
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class MessageHandler:
    """
    Handles all WhatsApp message operations.
    
    This class provides methods for:
    - Sending text messages
    - Sending media messages
    - Handling interactive messages (buttons, lists)
    - Managing message reactions
    - Processing incoming messages
    """
    
    def __init__(self):
        """Initialize MessageHandler."""
        self.message_handlers = []
        self.is_running = False
        
        logger.info("MessageHandler initialized")
    
    async def send_text_message(self, jid: str, message: str, client, **kwargs) -> Dict[str, Any]:
        """
        Send a text message to a WhatsApp user or group.
        
        Args:
            jid (str): WhatsApp JID (e.g., "1234567890@s.whatsapp.net")
            message (str): Message text
            client: Connection manager instance
            **kwargs: Additional options (quoted_message_id, mentioned_jids, etc.)
            
        Returns:
            Dict[str, Any]: Send result information
        """
        try:
            # Prepare message payload
            message_data = {
                'type': 'text',
                'content': message,
                'quoted_message_id': kwargs.get('quoted_message_id'),
                'mentioned_jids': kwargs.get('mentioned_jids', []),
                'link_preview': kwargs.get('link_preview', True),
                'view_once': kwargs.get('view_once', False)
            }
            
            # Send message through client
            result = await client.send_message(
                jid=jid,
                message=json.dumps(message_data),
                message_type='text'
            )
            
            # Extract message ID and timestamp from result
            message_id = result.get('message_id', f"msg_{int(asyncio.get_event_loop().time())}")
            timestamp = datetime.now().isoformat()
            
            return {
                'status': 'sent',
                'message_id': message_id,
                'timestamp': timestamp,
                'jid': jid,
                'content': message
            }
            
        except Exception as e:
            logger.error(f"Failed to send text message: {str(e)}")
            raise
    
    async def send_interactive_message(self, jid: str, message: str, buttons: List[Dict] = None, 
                                     list_items: List[Dict] = None, client=None, **kwargs) -> Dict[str, Any]:
        """
        Send an interactive message with buttons or list options.
        
        Args:
            jid (str): WhatsApp JID
            message (str): Message text
            buttons (List[Dict], optional): Button configurations
            list_items (List[Dict], optional): List item configurations
            client: Connection manager instance
            **kwargs: Additional options
            
        Returns:
            Dict[str, Any]: Send result information
        """
        try:
            if buttons and list_items:
                raise ValueError("Cannot specify both buttons and list_items")
            
            # Prepare interactive message payload
            message_data = {
                'type': 'interactive',
                'content': message,
                'view_once': kwargs.get('view_once', False)
            }
            
            if buttons:
                message_data['buttons'] = buttons
                message_data['interactive_type'] = 'button'
                
            elif list_items:
                message_data['list_items'] = list_items
                message_data['interactive_type'] = 'list'
            
            result = await client.send_message(
                jid=jid,
                message=json.dumps(message_data),
                message_type='interactive'
            )
            
            message_id = result.get('message_id', f"int_msg_{int(asyncio.get_event_loop().time())}")
            
            return {
                'status': 'sent',
                'message_id': message_id,
                'timestamp': datetime.now().isoformat(),
                'jid': jid,
                'content': message,
                'interactive_type': message_data.get('interactive_type')
            }
            
        except Exception as e:
            logger.error(f"Failed to send interactive message: {str(e)}")
            raise
    
    async def send_poll_message(self, jid: str, question: str, options: List[str], 
                              client=None, multiple_answers: bool = False, **kwargs) -> Dict[str, Any]:
        """
        Send a poll message.
        
        Args:
            jid (str): WhatsApp JID
            question (str): Poll question
            options (List[str]): Poll options
            client: Connection manager instance
            multiple_answers (bool): Whether multiple answers are allowed
            **kwargs: Additional options
            
        Returns:
            Dict[str, Any]: Send result information
        """
        try:
            # Validate poll options
            if len(options) < 2:
                raise ValueError("Poll must have at least 2 options")
            if len(options) > 12:
                raise ValueError("Poll cannot have more than 12 options")
            
            # Prepare poll message payload
            poll_data = {
                'type': 'poll',
                'question': question,
                'options': options,
                'multiple_answers': multiple_answers,
                'view_once': kwargs.get('view_once', False)
            }
            
            message_data = {
                'type': 'interactive',
                'content': json.dumps(poll_data),
                'interactive_type': 'poll'
            }
            
            result = await client.send_message(
                jid=jid,
                message=json.dumps(message_data),
                message_type='poll'
            )
            
            message_id = result.get('message_id', f"poll_{int(asyncio.get_event_loop().time())}")
            
            return {
                'status': 'sent',
                'message_id': message_id,
                'timestamp': datetime.now().isoformat(),
                'jid': jid,
                'poll_question': question,
                'poll_options': options,
                'multiple_answers': multiple_answers
            }
            
        except Exception as e:
            logger.error(f"Failed to send poll message: {str(e)}")
            raise
    
    async def send_ephemeral_message(self, jid: str, message: str, ephemeral_duration: int, 
                                   client=None, **kwargs) -> Dict[str, Any]:
        """
        Send an ephemeral message that disappears after viewing.
        
        Args:
            jid (str): WhatsApp JID
            message (str): Message text
            ephemeral_duration (int): Duration in seconds (24*60*60 for 24 hours)
            client: Connection manager instance
            **kwargs: Additional options
            
        Returns:
            Dict[str, Any]: Send result information
        """
        try:
            # Validate duration (WhatsApp allows 24 hours maximum for ephemeral messages)
            if ephemeral_duration > 24 * 60 * 60:
                raise ValueError("Ephemeral message duration cannot exceed 24 hours")
            if ephemeral_duration < 60:
                raise ValueError("Ephemeral message duration must be at least 60 seconds")
            
            message_data = {
                'type': 'text',
                'content': message,
                'ephemeral_duration': ephemeral_duration,
                'ephemeral': True
            }
            
            result = await client.send_message(
                jid=jid,
                message=json.dumps(message_data),
                message_type='text'
            )
            
            message_id = result.get('message_id', f"eph_{int(asyncio.get_event_loop().time())}")
            
            return {
                'status': 'sent',
                'message_id': message_id,
                'timestamp': datetime.now().isoformat(),
                'jid': jid,
                'content': message,
                'ephemeral_duration': ephemeral_duration
            }
            
        except Exception as e:
            logger.error(f"Failed to send ephemeral message: {str(e)}")
            raise
    
    async def reply_to_message(self, jid: str, reply_to_message_id: str, message: str, 
                             client=None, **kwargs) -> Dict[str, Any]:
        """
        Reply to a specific message.
        
        Args:
            jid (str): WhatsApp JID
            reply_to_message_id (str): ID of message to reply to
            message (str): Reply text
            client: Connection manager instance
            **kwargs: Additional options
            
        Returns:
            Dict[str, Any]: Send result information
        """
        try:
            result = await self.send_text_message(
                jid=jid,
                message=message,
                client=client,
                quoted_message_id=reply_to_message_id,
                **kwargs
            )
            
            logger.info(f"Reply sent to message {reply_to_message_id}")
            return result
            
        except Exception as e:
            logger.error(f"Failed to reply to message: {str(e)}")
            raise
    
    async def react_to_message(self, jid: str, message_id: str, emoji: str, client=None) -> Dict[str, Any]:
        """
        Add a reaction to a message.
        
        Args:
            jid (str): WhatsApp JID
            message_id (str): ID of message to react to
            emoji (str): Emoji to use as reaction
            client: Connection manager instance
            
        Returns:
            Dict[str, Any]: Reaction result information
        """
        try:
            # Validate emoji (basic validation)
            if len(emoji) > 10:  # WhatsApp reactions typically use single emojis
                logger.warning("Emoji might be too long for a reaction")
            
            reaction_data = {
                'type': 'reaction',
                'message_id': message_id,
                'emoji': emoji,
                'jid': jid
            }
            
            result = await client.send_message(
                jid=jid,
                message=json.dumps(reaction_data),
                message_type='reaction'
            )
            
            return {
                'status': 'reacted',
                'message_id': message_id,
                'emoji': emoji,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to react to message: {str(e)}")
            raise
    
    async def get_profile_info(self, jid: str, client=None) -> Dict[str, Any]:
        """
        Get profile information for a specific JID.
        
        Args:
            jid (str): WhatsApp JID
            client: Connection manager instance
            
        Returns:
            Dict[str, Any]: Profile information
        """
        try:
            # In a real implementation, this would query the Baileys backend
            # for profile information
            
            # Simulate profile info retrieval
            profile_data = {
                'jid': jid,
                'name': jid.split('@')[0] if '@' in jid else jid,
                'about': 'Profile information not available',
                'picture_url': None,
                'verified': False,
                'business': False,
                'last_seen': datetime.now().isoformat()
            }
            
            logger.info(f"Retrieved profile info for {jid}")
            return profile_data
            
        except Exception as e:
            logger.error(f"Failed to get profile info: {str(e)}")
            raise
    
    async def get_message_info(self, jid: str, message_id: str, client=None) -> Dict[str, Any]:
        """
        Get information about a specific message.
        
        Args:
            jid (str): WhatsApp JID where message was sent
            message_id (str): Message ID
            client: Connection manager instance
            
        Returns:
            Dict[str, Any]: Message information
        """
        try:
            # In a real implementation, this would query message status
            # from the Baileys backend
            
            # Simulate message info
            message_info = {
                'message_id': message_id,
                'jid': jid,
                'status': 'delivered',
                'timestamp': datetime.now().isoformat(),
                'type': 'text',
                'viewed': False,
                'forwarded': False
            }
            
            return message_info
            
        except Exception as e:
            logger.error(f"Failed to get message info: {str(e)}")
            raise
    
    async def delete_message(self, jid: str, message_id: str, for_everyone: bool = True, client=None) -> Dict[str, Any]:
        """
        Delete a sent message.
        
        Args:
            jid (str): WhatsApp JID
            message_id (str): ID of message to delete
            for_everyone (bool): Delete for everyone or just yourself
            client: Connection manager instance
            
        Returns:
            Dict[str, Any]: Delete result
        """
        try:
            delete_data = {
                'type': 'delete_message',
                'message_id': message_id,
                'for_everyone': for_everyone,
                'jid': jid
            }
            
            result = await client.send_message(
                jid=jid,
                message=json.dumps(delete_data),
                message_type='delete'
            )
            
            return {
                'status': 'deleted',
                'message_id': message_id,
                'for_everyone': for_everyone,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to delete message: {str(e)}")
            raise
    
    async def send_typing_indicator(self, jid: str, client=None):
        """
        Send typing indicator to a chat.
        
        Args:
            jid (str): WhatsApp JID
            client: Connection manager instance
        """
        try:
            typing_data = {
                'type': 'typing',
                'jid': jid
            }
            
            await client.send_message(
                jid=jid,
                message=json.dumps(typing_data),
                message_type='typing'
            )
            
        except Exception as e:
            logger.error(f"Failed to send typing indicator: {str(e)}")
            raise
    
    async def stop_typing_indicator(self, jid: str, client=None):
        """
        Stop typing indicator in a chat.
        
        Args:
            jid (str): WhatsApp JID
            client: Connection manager instance
        """
        try:
            stop_typing_data = {
                'type': 'stop_typing',
                'jid': jid
            }
            
            await client.send_message(
                jid=jid,
                message=json.dumps(stop_typing_data),
                message_type='stop_typing'
            )
            
        except Exception as e:
            logger.error(f"Failed to stop typing indicator: {str(e)}")
            raise
    
    def register_message_handler(self, handler: Callable):
        """
        Register a handler for incoming messages.
        
        Args:
            handler (Callable): Function to handle incoming messages
        """
        self.message_handlers.append(handler)
        logger.info("Message handler registered")
    
    async def start_listeners(self, client, event_handlers: Dict[str, Any]):
        """
        Start listening for incoming messages and events.
        
        Args:
            client: Connection manager instance
            event_handlers (dict): Event handlers for different events
        """
        if self.is_running:
            logger.warning("Message listeners already running")
            return
        
        self.is_running = True
        
        try:
            # Register message handler if available in event handlers
            if 'message' in event_handlers:
                message_handlers = event_handlers['message']
                for handler in message_handlers:
                    self.register_message_handler(handler)
            
            logger.info("Message listeners started")
            
            # In a real implementation, this would start WebSocket listeners
            # for incoming messages and events
            
        except Exception as e:
            logger.error(f"Failed to start message listeners: {str(e)}")
            self.is_running = False
            raise
    
    async def stop_listeners(self):
        """Stop all message listeners."""
        self.is_running = False
        self.message_handlers = []
        logger.info("Message listeners stopped")


# Utility functions for message formatting
def create_button(text: str, button_id: str, **kwargs) -> Dict[str, Any]:
    """
    Create a button configuration for interactive messages.
    
    Args:
        text (str): Button text
        button_id (str): Unique button identifier
        **kwargs: Additional button options
        
    Returns:
        Dict[str, Any]: Button configuration
    """
    return {
        'button_id': button_id,
        'text': text,
        'type': 1,
        'url': kwargs.get('url'),
        'call_to_action': kwargs.get('call_to_action'),
        'sections': kwargs.get('sections')
    }


def create_list_item(title: str, description: str = '', value: str = None) -> Dict[str, Any]:
    """
    Create a list item for interactive list messages.
    
    Args:
        title (str): Item title
        description (str, optional): Item description
        value (str, optional): Item value
        
    Returns:
        Dict[str, Any]: List item configuration
    """
    return {
        'title': title,
        'description': description,
        'value': value or title.lower().replace(' ', '_')
    }