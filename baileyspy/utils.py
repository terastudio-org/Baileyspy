"""
Utils - Utility functions for Baileyspy

This module provides various utility functions for handling WhatsApp operations,
formatting, validation, and helper methods.

Author: MiniMax Agent
"""

import asyncio
import hashlib
import logging
import re
from typing import Dict, Any, List, Optional, Union
from datetime import datetime, timedelta
import json

logger = logging.getLogger(__name__)


class Utils:
    """
    Utility functions for Baileyspy wrapper.
    
    This class provides helper methods for:
    - WhatsApp JID formatting and validation
    - Message formatting and processing
    - Date and time utilities
    - Data conversion helpers
    - Security and encryption utilities
    """
    
    def __init__(self):
        """Initialize Utils."""
        self.country_codes = {
            'US': '1', 'CA': '1', 'GB': '44', 'DE': '49', 'FR': '33', 'IT': '39',
            'ES': '34', 'RU': '7', 'IN': '91', 'CN': '86', 'JP': '81', 'KR': '82',
            'AU': '61', 'BR': '55', 'MX': '52', 'AR': '54', 'CL': '56', 'CO': '57',
            'PE': '51', 'VE': '58', 'PH': '63', 'ID': '62', 'TH': '66', 'VN': '84',
            'MY': '60', 'SG': '65', 'TW': '886', 'HK': '852', 'NZ': '64'
        }
        
        logger.info("Utils initialized")
    
    def format_phone_number(self, phone_number: str, country_code: str = None, add_suffix: bool = True) -> str:
        """
        Format a phone number for WhatsApp usage.
        
        Args:
            phone_number (str): Phone number
            country_code (str, optional): Country code (e.g., 'US', '44')
            add_suffix (bool): Whether to add @s.whatsapp.net suffix
            
        Returns:
            str: Formatted phone number
        """
        try:
            # Remove all non-digits
            clean_number = ''.join(filter(str.isdigit, phone_number))
            
            # Add country code if provided
            if country_code and len(clean_number) <= 10:
                if country_code.upper() in self.country_codes:
                    clean_number = self.country_codes[country_code.upper()] + clean_number
                else:
                    clean_number = country_code + clean_number
            
            # Add WhatsApp suffix if requested
            if add_suffix:
                return f"{clean_number}@s.whatsapp.net"
            else:
                return clean_number
                
        except Exception as e:
            logger.error(f"Failed to format phone number: {str(e)}")
            raise
    
    def is_valid_whatsapp_jid(self, jid: str) -> bool:
        """
        Validate if a string is a valid WhatsApp JID.
        
        Args:
            jid (str): WhatsApp JID to validate
            
        Returns:
            bool: True if valid JID
        """
        try:
            # Basic WhatsApp JID pattern
            jid_pattern = r'^\d+@s\.whatsapp\.net$'
            
            # Check basic format
            if not re.match(jid_pattern, jid):
                return False
            
            # Check if number part is valid (digits only, reasonable length)
            number_part = jid.split('@')[0]
            if not number_part.isdigit() or len(number_part) < 8 or len(number_part) > 15:
                return False
            
            return True
            
        except Exception:
            return False
    
    def is_group_jid(self, jid: str) -> bool:
        """
        Check if a JID belongs to a group.
        
        Args:
            jid (str): WhatsApp JID
            
        Returns:
            bool: True if it's a group JID
        """
        return '@g.us' in jid
    
    def extract_number_from_jid(self, jid: str) -> Optional[str]:
        """
        Extract phone number from a WhatsApp JID.
        
        Args:
            jid (str): WhatsApp JID
            
        Returns:
            Optional[str]: Phone number or None if not a user JID
        """
        try:
            if self.is_valid_whatsapp_jid(jid):
                return jid.split('@')[0]
            return None
            
        except Exception:
            return None
    
    def format_message_for_display(self, message_data: Dict[str, Any]) -> str:
        """
        Format a message for display purposes.
        
        Args:
            message_data (dict): Message data
            
        Returns:
            str: Formatted message string
        """
        try:
            message_type = message_data.get('type', 'unknown')
            content = message_data.get('content', '')
            
            if message_type == 'text':
                return content
            elif message_type == 'image':
                caption = message_data.get('caption', '')
                return f"[Image] {caption}"
            elif message_type == 'video':
                caption = message_data.get('caption', '')
                return f"[Video] {caption}"
            elif message_type == 'audio':
                caption = message_data.get('caption', '')
                return f"[Audio] {caption}"
            elif message_type == 'document':
                file_name = message_data.get('file_name', 'Document')
                return f"[Document] {file_name}"
            elif message_type == 'location':
                name = message_data.get('name', 'Location')
                return f"[Location] {name}"
            else:
                return f"[{message_type}] {content}"
                
        except Exception as e:
            logger.error(f"Failed to format message: {str(e)}")
            return str(message_data)
    
    def generate_message_id(self) -> str:
        """
        Generate a unique message ID.
        
        Returns:
            str: Unique message ID
        """
        timestamp = int(datetime.now().timestamp() * 1000)
        random_suffix = hashlib.md5(str(timestamp).encode()).hexdigest()[:8]
        return f"msg_{timestamp}_{random_suffix}"
    
    def format_timestamp(self, timestamp: Union[str, datetime, int]) -> str:
        """
        Format a timestamp for display.
        
        Args:
            timestamp: Timestamp to format (string, datetime, or int)
            
        Returns:
            str: Formatted timestamp string
        """
        try:
            if isinstance(timestamp, str):
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            elif isinstance(timestamp, datetime):
                dt = timestamp
            elif isinstance(timestamp, (int, float)):
                dt = datetime.fromtimestamp(timestamp)
            else:
                return str(timestamp)
            
            return dt.strftime("%Y-%m-%d %H:%M:%S")
            
        except Exception as e:
            logger.error(f"Failed to format timestamp: {str(e)}")
            return str(timestamp)
    
    def parse_duration(self, duration_str: str) -> int:
        """
        Parse a duration string to seconds.
        
        Args:
            duration_str (str): Duration string (e.g., "1h", "30m", "45s")
            
        Returns:
            int: Duration in seconds
        """
        try:
            duration_str = duration_str.lower().strip()
            
            # Extract number and unit
            match = re.match(r'(\d+)([hms]?)', duration_str)
            if not match:
                raise ValueError(f"Invalid duration format: {duration_str}")
            
            number = int(match.group(1))
            unit = match.group(2)
            
            if unit == 'h':
                return number * 3600
            elif unit == 'm':
                return number * 60
            elif unit == 's' or not unit:
                return number
            else:
                raise ValueError(f"Invalid duration unit: {unit}")
                
        except Exception as e:
            logger.error(f"Failed to parse duration: {str(e)}")
            raise
    
    def human_readable_size(self, size_bytes: int) -> str:
        """
        Convert bytes to human readable format.
        
        Args:
            size_bytes (int): Size in bytes
            
        Returns:
            str: Human readable size string
        """
        try:
            if size_bytes == 0:
                return "0B"
            
            size_names = ["B", "KB", "MB", "GB", "TB"]
            import math
            i = int(math.floor(math.log(size_bytes, 1024)))
            p = math.pow(1024, i)
            s = round(size_bytes / p, 2)
            return f"{s} {size_names[i]}"
            
        except Exception as e:
            logger.error(f"Failed to format size: {str(e)}")
            return f"{size_bytes} bytes"
    
    def clean_text(self, text: str, max_length: int = None) -> str:
        """
        Clean and optionally truncate text.
        
        Args:
            text (str): Text to clean
            max_length (int, optional): Maximum length
            
        Returns:
            str: Cleaned text
        """
        try:
            # Remove control characters
            cleaned = ''.join(char for char in text if ord(char) >= 32 or char in '\n\t\r')
            
            # Trim whitespace
            cleaned = cleaned.strip()
            
            # Truncate if needed
            if max_length and len(cleaned) > max_length:
                cleaned = cleaned[:max_length-3] + "..."
            
            return cleaned
            
        except Exception as e:
            logger.error(f"Failed to clean text: {str(e)}")
            return text
    
    def extract_mentions(self, message_text: str) -> List[str]:
        """
        Extract @mentions from message text.
        
        Args:
            message_text (str): Message text
            
        Returns:
            List[str]: List of mentioned JIDs
        """
        try:
            # Pattern to match @mentions in WhatsApp
            mention_pattern = r'@(\d+)'
            mentions = re.findall(mention_pattern, message_text)
            
            # Convert to full JIDs
            mentioned_jids = []
            for number in mentions:
                jid = f"{number}@s.whatsapp.net"
                if self.is_valid_whatsapp_jid(jid):
                    mentioned_jids.append(jid)
            
            return mentioned_jids
            
        except Exception as e:
            logger.error(f"Failed to extract mentions: {str(e)}")
            return []
    
    def encode_message_for_url(self, message_data: Dict[str, Any]) -> str:
        """
        Encode message data for URL parameters.
        
        Args:
            message_data (dict): Message data to encode
            
        Returns:
            str: URL-encoded message data
        """
        try:
            json_str = json.dumps(message_data, separators=(',', ':'))
            import urllib.parse
            return urllib.parse.quote(json_str)
            
        except Exception as e:
            logger.error(f"Failed to encode message: {str(e)}")
            return ""
    
    def decode_message_from_url(self, encoded_data: str) -> Dict[str, Any]:
        """
        Decode message data from URL parameters.
        
        Args:
            encoded_data (str): URL-encoded message data
            
        Returns:
            Dict[str, Any]: Decoded message data
        """
        try:
            import urllib.parse
            json_str = urllib.parse.unquote(encoded_data)
            return json.loads(json_str)
            
        except Exception as e:
            logger.error(f"Failed to decode message: {str(e)}")
            return {}
    
    def create_status_emoji(self, status: str) -> str:
        """
        Create an emoji representation of a status.
        
        Args:
            status (str): Status string
            
        Returns:
            str: Emoji representation
        """
        status_emojis = {
            'online': '🟢',
            'offline': '⚫',
            'away': '🟡',
            'busy': '🔴',
            'typing': '⌨️',
            'recording': '🎤',
            'connecting': '🔄',
            'connected': '✅',
            'disconnected': '❌',
            'error': '❌',
            'success': '✅',
            'warning': '⚠️',
            'info': 'ℹ️'
        }
        
        return status_emojis.get(status.lower(), '•')
    
    def mask_phone_number(self, phone_number: str) -> str:
        """
        Mask phone number for privacy (show only last 4 digits).
        
        Args:
            phone_number (str): Phone number
            
        Returns:
            str: Masked phone number
        """
        try:
            # Extract digits
            digits = ''.join(filter(str.isdigit, phone_number))
            
            if len(digits) <= 4:
                return '*' * len(digits)
            
            # Show last 4 digits, mask the rest
            return '*' * (len(digits) - 4) + digits[-4:]
            
        except Exception as e:
            logger.error(f"Failed to mask phone number: {str(e)}")
            return phone_number
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate similarity between two texts.
        
        Args:
            text1 (str): First text
            text2 (str): Second text
            
        Returns:
            float: Similarity score (0-1)
        """
        try:
            # Simple similarity calculation based on common words
            words1 = set(text1.lower().split())
            words2 = set(text2.lower().split())
            
            if not words1 and not words2:
                return 1.0
            if not words1 or not words2:
                return 0.0
            
            intersection = len(words1.intersection(words2))
            union = len(words1.union(words2))
            
            return intersection / union if union > 0 else 0.0
            
        except Exception as e:
            logger.error(f"Failed to calculate similarity: {str(e)}")
            return 0.0
    
    def is_spam_message(self, message_text: str, threshold: float = 0.8) -> bool:
        """
        Check if a message might be spam based on simple heuristics.
        
        Args:
            message_text (str): Message text to check
            threshold (float): Threshold for spam detection
            
        Returns:
            bool: True if message appears to be spam
        """
        try:
            text = message_text.lower()
            
            # Common spam indicators
            spam_indicators = [
                'click here', 'buy now', 'limited time', 'act fast', 'free money',
                'congratulations', 'you won', 'prize', 'lottery', 'win money',
                'urgent', 'exclusive offer', 'special promotion', 'money back'
            ]
            
            # Check for spam indicators
            spam_score = 0
            for indicator in spam_indicators:
                if indicator in text:
                    spam_score += 1
            
            # Check for excessive capitalization
            if text.isupper() and len(text) > 10:
                spam_score += 1
            
            # Check for excessive punctuation
            if text.count('!') > 3 or text.count('?') > 5:
                spam_score += 1
            
            # Check for repeated characters
            if re.search(r'(.)\1{4,}', text):
                spam_score += 1
            
            # Normalize score
            max_score = len(spam_indicators) + 3
            similarity = spam_score / max_score
            
            return similarity > threshold
            
        except Exception as e:
            logger.error(f"Failed to check spam: {str(e)}")
            return False
    
    def get_message_priority(self, message_data: Dict[str, Any]) -> int:
        """
        Get priority level for a message (higher number = higher priority).
        
        Args:
            message_data (dict): Message data
            
        Returns:
            int: Priority level (1-10)
        """
        try:
            message_type = message_data.get('type', 'text')
            priority_map = {
                'text': 5,
                'image': 6,
                'video': 7,
                'audio': 4,
                'document': 8,
                'location': 9,
                'sticker': 3,
                'system': 10,
                'call': 10,
                'notification': 7
            }
            
            return priority_map.get(message_type, 5)
            
        except Exception as e:
            logger.error(f"Failed to get message priority: {str(e)}")
            return 5