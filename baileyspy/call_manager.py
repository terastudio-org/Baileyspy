"""
CallManager - Handles WhatsApp voice call operations

This module provides functionality for initiating and managing WhatsApp voice calls
using the Baileys library's call capabilities.

Author: MiniMax Agent
"""

import asyncio
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class CallManager:
    """
    Handles WhatsApp voice call operations.
    
    This class provides methods for:
    - Initiating voice calls
    - Managing call states
    - Handling call events
    - Querying call information
    """
    
    def __init__(self):
        """Initialize CallManager."""
        self.active_calls = {}
        self.call_handlers = []
        self.is_call_active = False
        
        logger.info("CallManager initialized")
    
    async def offer_call(self, jid: str, client=None) -> Dict[str, Any]:
        """
        Initiate a voice call to a specific JID.
        
        Args:
            jid (str): WhatsApp JID to call
            client: Connection manager instance
            
        Returns:
            Dict[str, Any]: Call initiation result
        """
        try:
            # Validate JID
            if '@' not in jid or 'whatsapp.net' not in jid:
                raise ValueError(f"Invalid WhatsApp JID: {jid}")
            
            # Prepare call data
            call_data = {
                'type': 'offer_call',
                'jid': jid,
                'call_type': 'voice',
                'timestamp': datetime.now().isoformat()
            }
            
            # In a real implementation, this would use Baileys's offerCall method
            result = await client.send_message(
                jid=jid,
                message=json.dumps(call_data),
                message_type='call'
            )
            
            # Track the call
            call_id = f"call_{int(asyncio.get_event_loop().time())}"
            self.active_calls[call_id] = {
                'call_id': call_id,
                'jid': jid,
                'status': 'initiating',
                'start_time': datetime.now().isoformat(),
                'call_type': 'voice'
            }
            
            logger.info(f"Call initiated to {jid}")
            
            return {
                'status': 'initiated',
                'call_id': call_id,
                'jid': jid,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to offer call: {str(e)}")
            raise
    
    async def accept_call(self, call_id: str, client=None) -> Dict[str, Any]:
        """
        Accept an incoming call.
        
        Args:
            call_id (str): ID of the call to accept
            client: Connection manager instance
            
        Returns:
            Dict[str, Any]: Call acceptance result
        """
        try:
            if call_id not in self.active_calls:
                raise ValueError(f"Call {call_id} not found")
            
            call_info = self.active_calls[call_id]
            
            accept_data = {
                'type': 'accept_call',
                'call_id': call_id,
                'jid': call_info['jid']
            }
            
            await client.send_message(
                jid=call_info['jid'],
                message=json.dumps(accept_data),
                message_type='call'
            )
            
            # Update call status
            self.active_calls[call_id]['status'] = 'in_progress'
            self.active_calls[call_id]['answered_at'] = datetime.now().isoformat()
            self.is_call_active = True
            
            logger.info(f"Call {call_id} accepted")
            
            return {
                'status': 'accepted',
                'call_id': call_id,
                'jid': call_info['jid'],
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to accept call: {str(e)}")
            raise
    
    async def reject_call(self, call_id: str, reason: str = 'busy', client=None) -> Dict[str, Any]:
        """
        Reject an incoming call.
        
        Args:
            call_id (str): ID of the call to reject
            reason (str): Rejection reason ('busy', 'declined', 'unavailable')
            client: Connection manager instance
            
        Returns:
            Dict[str, Any]: Call rejection result
        """
        try:
            if call_id not in self.active_calls:
                raise ValueError(f"Call {call_id} not found")
            
            call_info = self.active_calls[call_id]
            
            reject_data = {
                'type': 'reject_call',
                'call_id': call_id,
                'jid': call_info['jid'],
                'reason': reason
            }
            
            await client.send_message(
                jid=call_info['jid'],
                message=json.dumps(reject_data),
                message_type='call'
            )
            
            # Update call status
            self.active_calls[call_id]['status'] = 'rejected'
            self.active_calls[call_id]['rejected_at'] = datetime.now().isoformat()
            self.active_calls[call_id]['rejection_reason'] = reason
            
            logger.info(f"Call {call_id} rejected: {reason}")
            
            return {
                'status': 'rejected',
                'call_id': call_id,
                'jid': call_info['jid'],
                'reason': reason,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to reject call: {str(e)}")
            raise
    
    async def end_call(self, call_id: str, client=None) -> Dict[str, Any]:
        """
        End an active call.
        
        Args:
            call_id (str): ID of the call to end
            client: Connection manager instance
            
        Returns:
            Dict[str, Any]: Call end result
        """
        try:
            if call_id not in self.active_calls:
                raise ValueError(f"Call {call_id} not found")
            
            call_info = self.active_calls[call_id]
            
            end_data = {
                'type': 'end_call',
                'call_id': call_id,
                'jid': call_info['jid']
            }
            
            await client.send_message(
                jid=call_info['jid'],
                message=json.dumps(end_data),
                message_type='call'
            )
            
            # Update call status
            self.active_calls[call_id]['status'] = 'ended'
            self.active_calls[call_id]['ended_at'] = datetime.now().isoformat()
            
            # Calculate call duration
            start_time = datetime.fromisoformat(call_info['start_time'])
            end_time = datetime.fromisoformat(self.active_calls[call_id]['ended_at'])
            duration = int((end_time - start_time).total_seconds())
            
            self.active_calls[call_id]['duration'] = duration
            self.is_call_active = False
            
            logger.info(f"Call {call_id} ended after {duration} seconds")
            
            return {
                'status': 'ended',
                'call_id': call_id,
                'jid': call_info['jid'],
                'duration': duration,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to end call: {str(e)}")
            raise
    
    async def mute_call(self, call_id: str, mute: bool = True, client=None) -> Dict[str, Any]:
        """
        Mute or unmute the current call.
        
        Args:
            call_id (str): ID of the call
            mute (bool): True to mute, False to unmute
            client: Connection manager instance
            
        Returns:
            Dict[str, Any]: Mute operation result
        """
        try:
            if call_id not in self.active_calls:
                raise ValueError(f"Call {call_id} not found")
            
            call_info = self.active_calls[call_id]
            
            mute_data = {
                'type': 'mute_call',
                'call_id': call_id,
                'jid': call_info['jid'],
                'mute': mute
            }
            
            await client.send_message(
                jid=call_info['jid'],
                message=json.dumps(mute_data),
                message_type='call'
            )
            
            # Update call status
            self.active_calls[call_id]['muted'] = mute
            
            action = 'muted' if mute else 'unmuted'
            logger.info(f"Call {call_id} {action}")
            
            return {
                'status': action,
                'call_id': call_id,
                'muted': mute,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to {'' if mute else 'un'}mute call: {str(e)}")
            raise
    
    async def get_call_info(self, call_id: str, client=None) -> Dict[str, Any]:
        """
        Get information about a specific call.
        
        Args:
            call_id (str): ID of the call
            client: Connection manager instance
            
        Returns:
            Dict[str, Any]: Call information
        """
        try:
            if call_id not in self.active_calls:
                raise ValueError(f"Call {call_id} not found")
            
            call_info = self.active_calls[call_id].copy()
            
            # Calculate current duration if call is still active
            if call_info['status'] == 'in_progress':
                start_time = datetime.fromisoformat(call_info['start_time'])
                current_time = datetime.now()
                call_info['duration'] = int((current_time - start_time).total_seconds())
                call_info['current_duration'] = call_info['duration']
            
            return call_info
            
        except Exception as e:
            logger.error(f"Failed to get call info: {str(e)}")
            raise
    
    async def get_active_calls(self) -> List[Dict[str, Any]]:
        """
        Get list of all active calls.
        
        Returns:
            List[Dict[str, Any]]: List of active call information
        """
        try:
            active_calls = [
                call_info for call_info in self.active_calls.values()
                if call_info['status'] in ['initiating', 'ringing', 'in_progress']
            ]
            
            return active_calls
            
        except Exception as e:
            logger.error(f"Failed to get active calls: {str(e)}")
            raise
    
    async def get_call_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get call history.
        
        Args:
            limit (int): Maximum number of calls to return
            
        Returns:
            List[Dict[str, Any]]: List of call history
        """
        try:
            # Sort calls by timestamp (most recent first)
            all_calls = sorted(
                self.active_calls.values(),
                key=lambda x: x.get('ended_at', x.get('start_time', '')),
                reverse=True
            )
            
            return all_calls[:limit]
            
        except Exception as e:
            logger.error(f"Failed to get call history: {str(e)}")
            raise
    
    async def clear_call_history(self):
        """Clear all call history."""
        try:
            self.active_calls = {}
            self.is_call_active = False
            logger.info("Call history cleared")
            
        except Exception as e:
            logger.error(f"Failed to clear call history: {str(e)}")
            raise
    
    def register_call_handler(self, handler):
        """
        Register a handler for call events.
        
        Args:
            handler: Function to handle call events
        """
        self.call_handlers.append(handler)
        logger.info("Call handler registered")
    
    async def handle_incoming_call(self, call_data: Dict[str, Any], client=None):
        """
        Handle an incoming call notification.
        
        Args:
            call_data (dict): Call data from WhatsApp
            client: Connection manager instance
        """
        try:
            # Extract call information
            jid = call_data.get('from', call_data.get('jid'))
            call_id = call_data.get('call_id', f"inc_{int(asyncio.get_event_loop().time())}")
            
            # Track the incoming call
            self.active_calls[call_id] = {
                'call_id': call_id,
                'jid': jid,
                'status': 'incoming',
                'start_time': datetime.now().isoformat(),
                'call_type': call_data.get('call_type', 'voice'),
                'is_incoming': True
            }
            
            logger.info(f"Incoming call from {jid}")
            
            # Notify registered handlers
            for handler in self.call_handlers:
                try:
                    await handler('incoming_call', self.active_calls[call_id])
                except Exception as e:
                    logger.error(f"Error in call handler: {str(e)}")
            
        except Exception as e:
            logger.error(f"Failed to handle incoming call: {str(e)}")
            raise
    
    async def handle_call_event(self, event_type: str, event_data: Dict[str, Any], client=None):
        """
        Handle various call events.
        
        Args:
            event_type (str): Type of call event
            event_data (dict): Event data
            client: Connection manager instance
        """
        try:
            call_id = event_data.get('call_id')
            
            if call_id and call_id in self.active_calls:
                # Update call status based on event
                if event_type == 'call_accepted':
                    self.active_calls[call_id]['status'] = 'in_progress'
                    self.active_calls[call_id]['answered_at'] = datetime.now().isoformat()
                    self.is_call_active = True
                    
                elif event_type == 'call_rejected':
                    self.active_calls[call_id]['status'] = 'rejected'
                    self.active_calls[call_id]['rejected_at'] = datetime.now().isoformat()
                    
                elif event_type == 'call_ended':
                    self.active_calls[call_id]['status'] = 'ended'
                    self.active_calls[call_id]['ended_at'] = datetime.now().isoformat()
                    
                    # Calculate duration
                    if 'answered_at' in self.active_calls[call_id]:
                        start_time = datetime.fromisoformat(self.active_calls[call_id]['answered_at'])
                    else:
                        start_time = datetime.fromisoformat(self.active_calls[call_id]['start_time'])
                    
                    end_time = datetime.fromisoformat(self.active_calls[call_id]['ended_at'])
                    duration = int((end_time - start_time).total_seconds())
                    self.active_calls[call_id]['duration'] = duration
                    
                    self.is_call_active = False
            
            # Notify handlers
            for handler in self.call_handlers:
                try:
                    await handler(event_type, event_data)
                except Exception as e:
                    logger.error(f"Error in call handler: {str(e)}")
            
        except Exception as e:
            logger.error(f"Failed to handle call event: {str(e)}")
            raise
    
    def is_any_call_active(self) -> bool:
        """
        Check if any call is currently active.
        
        Returns:
            bool: True if any call is active
        """
        return self.is_call_active