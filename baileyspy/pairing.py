"""
PairingManager - Handles WhatsApp device pairing operations

This module provides functionality for pairing devices and generating custom
pairing codes using the Baileys library's pairing capabilities.

Author: MiniMax Agent
"""

import asyncio
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
import json
import random
import string

logger = logging.getLogger(__name__)


class PairingManager:
    """
    Handles WhatsApp device pairing operations.
    
    This class provides methods for:
    - Generating custom pairing codes
    - Managing device pairing sessions
    - Handling pairing process events
    - Querying pairing status
    """
    
    def __init__(self):
        """Initialize PairingManager."""
        self.pairing_codes = {}
        self.active_pairings = {}
        self.is_pairing_active = False
        
        logger.info("PairingManager initialized")
    
    async def request_pairing_code(self, number: str, code: str = None, client=None) -> Dict[str, Any]:
        """
        Request a custom pairing code for device linking.
        
        Args:
            number (str): Phone number to pair (without country code)
            code (str, optional): Custom pairing code (e.g., 'AAAA-AAAA')
            client: Connection manager instance
            
        Returns:
            Dict[str, Any]: Pairing request result
        """
        try:
            # Validate number
            if not number or not number.strip():
                raise ValueError("Phone number cannot be empty")
            
            # Clean number (remove non-digits)
            clean_number = ''.join(filter(str.isdigit, number))
            if len(clean_number) < 8:
                raise ValueError("Phone number appears to be too short")
            
            # Generate or use provided code
            if not code:
                code = self._generate_pairing_code()
            else:
                self._validate_pairing_code(code)
            
            # Prepare pairing request
            pairing_data = {
                'type': 'request_pairing',
                'number': clean_number,
                'code': code,
                'timestamp': datetime.now().isoformat()
            }
            
            # In a real implementation, this would use Baileys's requestPairingCode method
            result = await client.send_message(
                jid='0@pairing',  # Special JID for pairing operations
                message=json.dumps(pairing_data),
                message_type='pairing'
            )
            
            # Track the pairing request
            pairing_id = f"pair_{int(asyncio.get_event_loop().time())}"
            self.pairing_codes[pairing_id] = {
                'pairing_id': pairing_id,
                'number': clean_number,
                'code': code,
                'status': 'requested',
                'requested_at': datetime.now().isoformat(),
                'expires_at': self._calculate_expiry()
            }
            
            logger.info(f"Pairing code {code} requested for number {clean_number}")
            
            return {
                'status': 'requested',
                'pairing_id': pairing_id,
                'number': clean_number,
                'pairing_code': code,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to request pairing code: {str(e)}")
            raise
    
    def _generate_pairing_code(self, length: int = 8, format_with_hyphen: bool = False) -> str:
        """
        Generate a random pairing code.
        
        Args:
            length (int): Length of the code (default: 8)
            format_with_hyphen (bool): Whether to format with hyphen (e.g., 'AAAA-AAAA')
            
        Returns:
            str: Generated pairing code
        """
        # Baileys typically uses uppercase letters A-F for pairing codes
        characters = 'ABCDEF'
        
        # Generate random code
        code = ''.join(random.choices(characters, k=length))
        
        # Format with hyphen if requested
        if format_with_hyphen and length >= 4:
            return f"{code[:4]}-{code[4:]}"
        
        return code
    
    def _validate_pairing_code(self, code: str):
        """
        Validate a pairing code format.
        
        Args:
            code (str): Pairing code to validate
            
        Raises:
            ValueError: If code format is invalid
        """
        if not code or len(code) < 4:
            raise ValueError("Pairing code must be at least 4 characters")
        
        # Remove hyphens for validation
        clean_code = code.replace('-', '').upper()
        
        # Check if code contains only valid characters (A-F)
        valid_chars = set('ABCDEF')
        if not all(char in valid_chars for char in clean_code):
            raise ValueError("Pairing code must contain only characters A-F")
        
        return clean_code
    
    def _calculate_expiry(self, minutes: int = 60) -> str:
        """
        Calculate expiry time for pairing code.
        
        Args:
            minutes (int): Minutes until expiry
            
        Returns:
            str: ISO format expiry timestamp
        """
        expiry_time = datetime.now().timestamp() + (minutes * 60)
        return datetime.fromtimestamp(expiry_time).isoformat()
    
    async def verify_pairing_code(self, pairing_id: str, code: str, client=None) -> Dict[str, Any]:
        """
        Verify a pairing code for device linking.
        
        Args:
            pairing_id (str): ID of the pairing request
            code (str): Pairing code to verify
            client: Connection manager instance
            
        Returns:
            Dict[str, Any]: Verification result
        """
        try:
            if pairing_id not in self.pairing_codes:
                raise ValueError(f"Pairing request {pairing_id} not found")
            
            pairing_info = self.pairing_codes[pairing_id]
            
            # Check if pairing code has expired
            expiry_time = datetime.fromisoformat(pairing_info['expires_at'])
            if datetime.now() > expiry_time:
                self.pairing_codes[pairing_id]['status'] = 'expired'
                raise ValueError("Pairing code has expired")
            
            # Validate the provided code
            provided_code = self._validate_pairing_code(code)
            expected_code = pairing_info['code'].replace('-', '').upper()
            
            if provided_code != expected_code:
                raise ValueError("Invalid pairing code")
            
            # Prepare verification request
            verify_data = {
                'type': 'verify_pairing',
                'pairing_id': pairing_id,
                'number': pairing_info['number'],
                'code': provided_code,
                'timestamp': datetime.now().isoformat()
            }
            
            result = await client.send_message(
                jid='0@pairing',
                message=json.dumps(verify_data),
                message_type='pairing'
            )
            
            # Update pairing status
            self.pairing_codes[pairing_id]['status'] = 'verified'
            self.pairing_codes[pairing_id]['verified_at'] = datetime.now().isoformat()
            
            logger.info(f"Pairing code verified for request {pairing_id}")
            
            return {
                'status': 'verified',
                'pairing_id': pairing_id,
                'number': pairing_info['number'],
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to verify pairing code: {str(e)}")
            raise
    
    async def complete_pairing(self, pairing_id: str, client=None) -> Dict[str, Any]:
        """
        Complete the pairing process and get authentication tokens.
        
        Args:
            pairing_id (str): ID of the pairing request
            client: Connection manager instance
            
        Returns:
            Dict[str, Any]: Pairing completion result
        """
        try:
            if pairing_id not in self.pairing_codes:
                raise ValueError(f"Pairing request {pairing_id} not found")
            
            pairing_info = self.pairing_codes[pairing_id]
            
            if pairing_info['status'] != 'verified':
                raise ValueError("Pairing code must be verified before completion")
            
            # Prepare completion request
            complete_data = {
                'type': 'complete_pairing',
                'pairing_id': pairing_id,
                'number': pairing_info['number'],
                'timestamp': datetime.now().isoformat()
            }
            
            result = await client.send_message(
                jid='0@pairing',
                message=json.dumps(complete_data),
                message_type='pairing'
            )
            
            # Simulate successful pairing response
            auth_tokens = {
                'auth_token': f"auth_{int(asyncio.get_event_loop().time())}",
                'device_id': f"device_{int(asyncio.get_event_loop().time())}",
                'phone_number': pairing_info['number']
            }
            
            # Update pairing status
            self.pairing_codes[pairing_id]['status'] = 'completed'
            self.pairing_codes[pairing_id]['completed_at'] = datetime.now().isoformat()
            self.pairing_codes[pairing_id]['auth_tokens'] = auth_tokens
            
            # Create active pairing record
            device_id = auth_tokens['device_id']
            self.active_pairings[device_id] = {
                'device_id': device_id,
                'phone_number': pairing_info['number'],
                'paired_at': datetime.now().isoformat(),
                'auth_token': auth_tokens['auth_token'],
                'pairing_id': pairing_id
            }
            
            self.is_pairing_active = True
            
            logger.info(f"Pairing completed for device {device_id}")
            
            return {
                'status': 'completed',
                'pairing_id': pairing_id,
                'device_id': device_id,
                'phone_number': pairing_info['number'],
                'auth_tokens': auth_tokens,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to complete pairing: {str(e)}")
            raise
    
    async def get_pairing_status(self, pairing_id: str) -> Dict[str, Any]:
        """
        Get the status of a pairing request.
        
        Args:
            pairing_id (str): ID of the pairing request
            
        Returns:
            Dict[str, Any]: Pairing status information
        """
        try:
            if pairing_id not in self.pairing_codes:
                raise ValueError(f"Pairing request {pairing_id} not found")
            
            pairing_info = self.pairing_codes[pairing_id].copy()
            
            # Check if code has expired
            if pairing_info['status'] in ['requested', 'verified']:
                expiry_time = datetime.fromisoformat(pairing_info['expires_at'])
                if datetime.now() > expiry_time:
                    pairing_info['status'] = 'expired'
                    self.pairing_codes[pairing_id]['status'] = 'expired'
            
            return pairing_info
            
        except Exception as e:
            logger.error(f"Failed to get pairing status: {str(e)}")
            raise
    
    async def get_active_pairings(self) -> List[Dict[str, Any]]:
        """
        Get list of active device pairings.
        
        Returns:
            List[Dict[str, Any]]: List of active pairings
        """
        try:
            return list(self.active_pairings.values())
            
        except Exception as e:
            logger.error(f"Failed to get active pairings: {str(e)}")
            raise
    
    async def revoke_pairing(self, pairing_id: str, client=None) -> Dict[str, Any]:
        """
        Revoke a pairing request.
        
        Args:
            pairing_id (str): ID of the pairing request
            client: Connection manager instance
            
        Returns:
            Dict[str, Any]: Revocation result
        """
        try:
            if pairing_id not in self.pairing_codes:
                raise ValueError(f"Pairing request {pairing_id} not found")
            
            pairing_info = self.pairing_codes[pairing_id]
            
            # Prepare revocation request
            revoke_data = {
                'type': 'revoke_pairing',
                'pairing_id': pairing_id,
                'number': pairing_info['number'],
                'timestamp': datetime.now().isoformat()
            }
            
            await client.send_message(
                jid='0@pairing',
                message=json.dumps(revoke_data),
                message_type='pairing'
            )
            
            # Update pairing status
            self.pairing_codes[pairing_id]['status'] = 'revoked'
            self.pairing_codes[pairing_id]['revoked_at'] = datetime.now().isoformat()
            
            logger.info(f"Pairing request {pairing_id} revoked")
            
            return {
                'status': 'revoked',
                'pairing_id': pairing_id,
                'number': pairing_info['number'],
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to revoke pairing: {str(e)}")
            raise
    
    async def generate_default_pairing_code(self, length: int = 8) -> str:
        """
        Generate a default pairing code for convenience.
        
        Args:
            length (int): Length of the code
            
        Returns:
            str: Generated pairing code
        """
        return self._generate_pairing_code(length)
    
    async def cleanup_expired_codes(self):
        """Clean up expired pairing codes."""
        try:
            current_time = datetime.now()
            expired_count = 0
            
            for pairing_id, pairing_info in list(self.pairing_codes.items()):
                if pairing_info['status'] in ['requested', 'verified']:
                    expiry_time = datetime.fromisoformat(pairing_info['expires_at'])
                    if current_time > expiry_time:
                        self.pairing_codes[pairing_id]['status'] = 'expired'
                        expired_count += 1
            
            if expired_count > 0:
                logger.info(f"Cleaned up {expired_count} expired pairing codes")
            
        except Exception as e:
            logger.error(f"Failed to cleanup expired codes: {str(e)}")
    
    def get_pairing_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about pairing operations.
        
        Returns:
            Dict[str, Any]: Pairing statistics
        """
        try:
            total_requests = len(self.pairing_codes)
            completed_requests = sum(
                1 for p in self.pairing_codes.values() 
                if p['status'] == 'completed'
            )
            expired_requests = sum(
                1 for p in self.pairing_codes.values() 
                if p['status'] == 'expired'
            )
            
            return {
                'total_requests': total_requests,
                'completed_requests': completed_requests,
                'expired_requests': expired_requests,
                'active_pairings': len(self.active_pairings),
                'is_pairing_active': self.is_pairing_active
            }
            
        except Exception as e:
            logger.error(f"Failed to get pairing statistics: {str(e)}")
            return {}
    
    async def reset_pairing_state(self):
        """Reset pairing state and clear all records."""
        try:
            self.pairing_codes = {}
            self.active_pairings = {}
            self.is_pairing_active = False
            
            logger.info("Pairing state reset")
            
        except Exception as e:
            logger.error(f"Failed to reset pairing state: {str(e)}")
            raise