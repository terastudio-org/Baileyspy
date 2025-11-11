"""
GroupManager - Handles WhatsApp group operations

This module provides functionality for managing WhatsApp groups including
creating, joining, leaving, and managing group members.

Author: MiniMax Agent
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class GroupManager:
    """
    Handles WhatsApp group operations.
    
    This class provides methods for:
    - Creating new groups
    - Managing group members
    - Updating group settings
    - Getting group information
    - Managing group invites
    """
    
    def __init__(self):
        """Initialize GroupManager."""
        self.group_cache = {}
        
        logger.info("GroupManager initialized")
    
    async def create_group(self, name: str, participants: List[str], client=None, **kwargs) -> Dict[str, Any]:
        """
        Create a new WhatsApp group.
        
        Args:
            name (str): Group name
            participants (List[str]): List of participant JIDs
            client: Connection manager instance
            **kwargs: Additional group options (description, etc.)
            
        Returns:
            Dict[str, Any]: Created group information
        """
        try:
            if len(participants) < 1:
                raise ValueError("Group must have at least 1 participant")
            if len(participants) > 1024:  # WhatsApp group limit
                raise ValueError("Group cannot have more than 1024 participants")
            
            # Validate participant JIDs
            for participant in participants:
                if '@' not in participant or 'whatsapp.net' not in participant:
                    raise ValueError(f"Invalid participant JID: {participant}")
            
            # Prepare group creation data
            group_data = {
                'type': 'create_group',
                'name': name,
                'participants': participants,
                'description': kwargs.get('description'),
                'announce': kwargs.get('announce', False),  # Restrict who can edit group info
                'no_frequently_forwarded': kwargs.get('no_frequently_forwarded', False)
            }
            
            # Send group creation request
            result = await client.send_message(
                jid='0@group',  # Special JID for group operations
                message=json.dumps(group_data),
                message_type='group_operation'
            )
            
            # Simulate group creation response
            group_id = f"{int(asyncio.get_event_loop().time())}@g.us"
            
            # Cache group information
            group_info = {
                'group_id': group_id,
                'name': name,
                'participants': participants,
                'owner': client.auth_state.get('phone_number'),
                'created_at': datetime.now().isoformat(),
                'description': group_data.get('description'),
                'announce': group_data.get('announce'),
                'member_count': len(participants)
            }
            
            self.group_cache[group_id] = group_info
            
            logger.info(f"Group '{name}' created with {len(participants)} participants")
            
            return {
                'status': 'created',
                'group_id': group_id,
                'group_info': group_info
            }
            
        except Exception as e:
            logger.error(f"Failed to create group: {str(e)}")
            raise
    
    async def get_groups(self, client=None) -> List[Dict[str, Any]]:
        """
        Get list of all groups the client is part of.
        
        Args:
            client: Connection manager instance
            
        Returns:
            List[Dict[str, Any]]: List of group information
        """
        try:
            # In a real implementation, this would query the Baileys backend
            # for the list of groups
            
            # Return cached groups or simulate fetching from backend
            groups = list(self.group_cache.values())
            
            logger.info(f"Retrieved {len(groups)} groups")
            return groups
            
        except Exception as e:
            logger.error(f"Failed to get groups: {str(e)}")
            raise
    
    async def get_group_info(self, group_id: str, client=None) -> Dict[str, Any]:
        """
        Get detailed information about a specific group.
        
        Args:
            group_id (str): Group ID
            client: Connection manager instance
            
        Returns:
            Dict[str, Any]: Group information
        """
        try:
            # Check cache first
            if group_id in self.group_cache:
                group_info = self.group_cache[group_id]
                
                # In a real implementation, this would refresh group info
                # from the Baileys backend
                logger.info(f"Retrieved group info for {group_id}")
                return group_info
            
            # If not in cache, simulate fetching
            # This would normally query the Baileys backend
            group_info = {
                'group_id': group_id,
                'name': f'Group {group_id.split("@")[0]}',
                'participants': [],
                'owner': 'unknown',
                'description': 'Group information unavailable',
                'created_at': datetime.now().isoformat(),
                'member_count': 0
            }
            
            return group_info
            
        except Exception as e:
            logger.error(f"Failed to get group info: {str(e)}")
            raise
    
    async def add_participants(self, group_id: str, participants: List[str], client=None) -> Dict[str, Any]:
        """
        Add participants to a group.
        
        Args:
            group_id (str): Group ID
            participants (List[str]): List of participant JIDs to add
            client: Connection manager instance
            
        Returns:
            Dict[str, Any]: Operation result
        """
        try:
            if not participants:
                raise ValueError("No participants provided to add")
            
            # Validate participant JIDs
            for participant in participants:
                if '@' not in participant or 'whatsapp.net' not in participant:
                    raise ValueError(f"Invalid participant JID: {participant}")
            
            add_data = {
                'type': 'add_participants',
                'group_id': group_id,
                'participants': participants
            }
            
            result = await client.send_message(
                jid=group_id,
                message=json.dumps(add_data),
                message_type='group_operation'
            )
            
            # Update cache
            if group_id in self.group_cache:
                current_participants = self.group_cache[group_id]['participants']
                self.group_cache[group_id]['participants'] = list(set(current_participants + participants))
                self.group_cache[group_id]['member_count'] = len(self.group_cache[group_id]['participants'])
            
            logger.info(f"Added {len(participants)} participants to group {group_id}")
            
            return {
                'status': 'added',
                'group_id': group_id,
                'participants_added': participants,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to add participants: {str(e)}")
            raise
    
    async def remove_participants(self, group_id: str, participants: List[str], client=None) -> Dict[str, Any]:
        """
        Remove participants from a group.
        
        Args:
            group_id (str): Group ID
            participants (List[str]): List of participant JIDs to remove
            client: Connection manager instance
            
        Returns:
            Dict[str, Any]: Operation result
        """
        try:
            if not participants:
                raise ValueError("No participants provided to remove")
            
            remove_data = {
                'type': 'remove_participants',
                'group_id': group_id,
                'participants': participants
            }
            
            result = await client.send_message(
                jid=group_id,
                message=json.dumps(remove_data),
                message_type='group_operation'
            )
            
            # Update cache
            if group_id in self.group_cache:
                current_participants = self.group_cache[group_id]['participants']
                self.group_cache[group_id]['participants'] = [
                    p for p in current_participants if p not in participants
                ]
                self.group_cache[group_id]['member_count'] = len(self.group_cache[group_id]['participants'])
            
            logger.info(f"Removed {len(participants)} participants from group {group_id}")
            
            return {
                'status': 'removed',
                'group_id': group_id,
                'participants_removed': participants,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to remove participants: {str(e)}")
            raise
    
    async def promote_participants(self, group_id: str, participants: List[str], client=None) -> Dict[str, Any]:
        """
        Promote participants to admin in a group.
        
        Args:
            group_id (str): Group ID
            participants (List[str]): List of participant JIDs to promote
            client: Connection manager instance
            
        Returns:
            Dict[str, Any]: Operation result
        """
        try:
            if not participants:
                raise ValueError("No participants provided to promote")
            
            promote_data = {
                'type': 'promote_participants',
                'group_id': group_id,
                'participants': participants
            }
            
            result = await client.send_message(
                jid=group_id,
                message=json.dumps(promote_data),
                message_type='group_operation'
            )
            
            logger.info(f"Promoted {len(participants)} participants in group {group_id}")
            
            return {
                'status': 'promoted',
                'group_id': group_id,
                'participants_promoted': participants,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to promote participants: {str(e)}")
            raise
    
    async def demote_participants(self, group_id: str, participants: List[str], client=None) -> Dict[str, Any]:
        """
        Demote admin participants to regular members.
        
        Args:
            group_id (str): Group ID
            participants (List[str]): List of participant JIDs to demote
            client: Connection manager instance
            
        Returns:
            Dict[str, Any]: Operation result
        """
        try:
            if not participants:
                raise ValueError("No participants provided to demote")
            
            demote_data = {
                'type': 'demote_participants',
                'group_id': group_id,
                'participants': participants
            }
            
            result = await client.send_message(
                jid=group_id,
                message=json.dumps(demote_data),
                message_type='group_operation'
            )
            
            logger.info(f"Demoted {len(participants)} participants in group {group_id}")
            
            return {
                'status': 'demoted',
                'group_id': group_id,
                'participants_demoted': participants,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to demote participants: {str(e)}")
            raise
    
    async def update_group_name(self, group_id: str, new_name: str, client=None) -> Dict[str, Any]:
        """
        Update the group name.
        
        Args:
            group_id (str): Group ID
            new_name (str): New group name
            client: Connection manager instance
            
        Returns:
            Dict[str, Any]: Operation result
        """
        try:
            if not new_name.strip():
                raise ValueError("Group name cannot be empty")
            
            if len(new_name) > 25:  # WhatsApp group name limit
                raise ValueError("Group name cannot exceed 25 characters")
            
            name_data = {
                'type': 'update_group_name',
                'group_id': group_id,
                'new_name': new_name
            }
            
            result = await client.send_message(
                jid=group_id,
                message=json.dumps(name_data),
                message_type='group_operation'
            )
            
            # Update cache
            if group_id in self.group_cache:
                self.group_cache[group_id]['name'] = new_name
            
            logger.info(f"Group name updated to '{new_name}' for group {group_id}")
            
            return {
                'status': 'updated',
                'group_id': group_id,
                'new_name': new_name,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to update group name: {str(e)}")
            raise
    
    async def update_group_description(self, group_id: str, description: str, client=None) -> Dict[str, Any]:
        """
        Update the group description.
        
        Args:
            group_id (str): Group ID
            description (str): New group description
            client: Connection manager instance
            
        Returns:
            Dict[str, Any]: Operation result
        """
        try:
            if len(description) > 512:  # WhatsApp group description limit
                raise ValueError("Group description cannot exceed 512 characters")
            
            desc_data = {
                'type': 'update_group_description',
                'group_id': group_id,
                'description': description
            }
            
            result = await client.send_message(
                jid=group_id,
                message=json.dumps(desc_data),
                message_type='group_operation'
            )
            
            # Update cache
            if group_id in self.group_cache:
                self.group_cache[group_id]['description'] = description
            
            logger.info(f"Group description updated for group {group_id}")
            
            return {
                'status': 'updated',
                'group_id': group_id,
                'description': description,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to update group description: {str(e)}")
            raise
    
    async def leave_group(self, group_id: str, client=None) -> Dict[str, Any]:
        """
        Leave a group.
        
        Args:
            group_id (str): Group ID to leave
            client: Connection manager instance
            
        Returns:
            Dict[str, Any]: Operation result
        """
        try:
            leave_data = {
                'type': 'leave_group',
                'group_id': group_id
            }
            
            result = await client.send_message(
                jid=group_id,
                message=json.dumps(leave_data),
                message_type='group_operation'
            )
            
            # Remove from cache
            if group_id in self.group_cache:
                del self.group_cache[group_id]
            
            logger.info(f"Left group {group_id}")
            
            return {
                'status': 'left',
                'group_id': group_id,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to leave group: {str(e)}")
            raise
    
    async def get_invite_link(self, group_id: str, client=None) -> Dict[str, Any]:
        """
        Get the invite link for a group.
        
        Args:
            group_id (str): Group ID
            client: Connection manager instance
            
        Returns:
            Dict[str, Any]: Invite link information
        """
        try:
            invite_data = {
                'type': 'get_invite_link',
                'group_id': group_id
            }
            
            result = await client.send_message(
                jid=group_id,
                message=json.dumps(invite_data),
                message_type='group_operation'
            )
            
            # Simulate invite link generation
            invite_link = f"https://chat.whatsapp.com/{group_id.split('@')[0]}"
            
            logger.info(f"Invite link generated for group {group_id}")
            
            return {
                'status': 'generated',
                'group_id': group_id,
                'invite_link': invite_link,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to get invite link: {str(e)}")
            raise
    
    async def revoke_invite_link(self, group_id: str, client=None) -> Dict[str, Any]:
        """
        Revoke the current invite link and generate a new one.
        
        Args:
            group_id (str): Group ID
            client: Connection manager instance
            
        Returns:
            Dict[str, Any]: New invite link information
        """
        try:
            revoke_data = {
                'type': 'revoke_invite_link',
                'group_id': group_id
            }
            
            result = await client.send_message(
                jid=group_id,
                message=json.dumps(revoke_data),
                message_type='group_operation'
            )
            
            # Simulate new invite link
            invite_link = f"https://chat.whatsapp.com/{int(asyncio.get_event_loop().time())}"
            
            logger.info(f"Invite link revoked and new one generated for group {group_id}")
            
            return {
                'status': 'revoked',
                'group_id': group_id,
                'new_invite_link': invite_link,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to revoke invite link: {str(e)}")
            raise
    
    async def join_group(self, invite_link: str, client=None) -> Dict[str, Any]:
        """
        Join a group using an invite link.
        
        Args:
            invite_link (str): Group invite link
            client: Connection manager instance
            
        Returns:
            Dict[str, Any]: Join result
        """
        try:
            join_data = {
                'type': 'join_group',
                'invite_link': invite_link
            }
            
            result = await client.send_message(
                jid='0@group',
                message=json.dumps(join_data),
                message_type='group_operation'
            )
            
            # Simulate group joining
            group_id = f"{int(asyncio.get_event_loop().time())}@g.us"
            
            # Add to cache
            group_info = {
                'group_id': group_id,
                'name': 'Joined Group',
                'participants': [],
                'owner': 'unknown',
                'description': 'Joined via invite link',
                'created_at': datetime.now().isoformat(),
                'member_count': 0
            }
            
            self.group_cache[group_id] = group_info
            
            logger.info(f"Joined group via invite link: {invite_link}")
            
            return {
                'status': 'joined',
                'group_id': group_id,
                'invite_link': invite_link,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to join group: {str(e)}")
            raise
    
    async def mute_group(self, group_id: str, duration: int = -1, client=None) -> Dict[str, Any]:
        """
        Mute group notifications.
        
        Args:
            group_id (str): Group ID
            duration (int): Mute duration in seconds (-1 for indefinite)
            client: Connection manager instance
            
        Returns:
            Dict[str, Any]: Mute operation result
        """
        try:
            mute_data = {
                'type': 'mute_group',
                'group_id': group_id,
                'duration': duration
            }
            
            result = await client.send_message(
                jid=group_id,
                message=json.dumps(mute_data),
                message_type='group_operation'
            )
            
            duration_str = "indefinitely" if duration == -1 else f"for {duration} seconds"
            logger.info(f"Group {group_id} muted {duration_str}")
            
            return {
                'status': 'muted',
                'group_id': group_id,
                'duration': duration,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to mute group: {str(e)}")
            raise