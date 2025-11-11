"""
MediaHandler - Handles WhatsApp media operations

This module provides functionality for sending and receiving media files
including images, videos, documents, audio, and setting profile pictures.

Author: MiniMax Agent
"""

import asyncio
import logging
import mimetypes
import os
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class MediaHandler:
    """
    Handles WhatsApp media operations.
    
    This class provides methods for:
    - Sending images, videos, documents, and audio
    - Setting profile pictures
    - Managing media uploads and downloads
    - Handling media captions and metadata
    """
    
    def __init__(self):
        """Initialize MediaHandler."""
        self.supported_image_types = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'}
        self.supported_video_types = {'.mp4', '.mov', '.avi', '.mkv', '.webm', '.3gp'}
        self.supported_audio_types = {'.mp3', '.wav', '.ogg', '.aac', '.m4a'}
        self.supported_document_types = {'.pdf', '.doc', '.docx', '.txt', '.rtf', '.xls', '.xlsx', '.ppt', '.pptx', '.zip', '.rar'}
        
        logger.info("MediaHandler initialized")
    
    async def send_media(self, jid: str, media_path: str, media_type: str = None, client=None, **kwargs) -> Dict[str, Any]:
        """
        Send a media file to WhatsApp.
        
        Args:
            jid (str): WhatsApp JID
            media_path (str): Path to media file
            media_type (str, optional): Type of media ('image', 'video', 'audio', 'document')
            client: Connection manager instance
            **kwargs: Additional options (caption, quoted_message_id, etc.)
            
        Returns:
            Dict[str, Any]: Send result information
        """
        try:
            # Validate file exists
            if not os.path.exists(media_path):
                raise FileNotFoundError(f"Media file not found: {media_path}")
            
            # Determine media type if not provided
            if not media_type:
                media_type = self._determine_media_type(media_path)
            
            if not media_type:
                raise ValueError(f"Unsupported or unknown media type for file: {media_path}")
            
            # Validate file size (WhatsApp has limits)
            file_size = os.path.getsize(media_path)
            max_size = self._get_max_file_size(media_type)
            if file_size > max_size:
                raise ValueError(f"File size ({file_size} bytes) exceeds {media_type} limit ({max_size} bytes)")
            
            # Prepare media upload data
            media_data = {
                'type': f'send_{media_type}',
                'media_path': media_path,
                'media_type': media_type,
                'file_name': os.path.basename(media_path),
                'file_size': file_size,
                'mime_type': mimetypes.guess_type(media_path)[0],
                'caption': kwargs.get('caption'),
                'quoted_message_id': kwargs.get('quoted_message_id'),
                'mentioned_jids': kwargs.get('mentioned_jids', []),
                'view_once': kwargs.get('view_once', False)
            }
            
            # Add media-specific options
            if media_type == 'image':
                media_data['width'] = kwargs.get('width')
                media_data['height'] = kwargs.get('height')
                media_data['quality'] = kwargs.get('quality', 'high')  # 'high', 'medium', 'low'
                
            elif media_type == 'video':
                media_data['duration'] = kwargs.get('duration')  # in seconds
                media_data['loop'] = kwargs.get('loop', False)
                
            elif media_type == 'audio':
                media_data['duration'] = kwargs.get('duration')  # in seconds
                media_data['audio_type'] = kwargs.get('audio_type', 'voice')  # 'voice', 'music'
            
            # Send media through client
            result = await client.send_message(
                jid=jid,
                message=json.dumps(media_data),
                message_type='media'
            )
            
            message_id = result.get('message_id', f"media_{int(asyncio.get_event_loop().time())}")
            
            logger.info(f"Media sent: {media_type} to {jid}")
            
            return {
                'status': 'sent',
                'message_id': message_id,
                'timestamp': datetime.now().isoformat(),
                'jid': jid,
                'media_type': media_type,
                'file_name': media_data['file_name'],
                'file_size': file_size,
                'caption': media_data.get('caption')
            }
            
        except Exception as e:
            logger.error(f"Failed to send media: {str(e)}")
            raise
    
    async def send_image(self, jid: str, image_path: str, caption: str = None, client=None, **kwargs) -> Dict[str, Any]:
        """
        Send an image to WhatsApp.
        
        Args:
            jid (str): WhatsApp JID
            image_path (str): Path to image file
            caption (str, optional): Image caption
            client: Connection manager instance
            **kwargs: Additional options
            
        Returns:
            Dict[str, Any]: Send result information
        """
        try:
            return await self.send_media(
                jid=jid,
                media_path=image_path,
                media_type='image',
                client=client,
                caption=caption,
                **kwargs
            )
            
        except Exception as e:
            logger.error(f"Failed to send image: {str(e)}")
            raise
    
    async def send_video(self, jid: str, video_path: str, caption: str = None, client=None, **kwargs) -> Dict[str, Any]:
        """
        Send a video to WhatsApp.
        
        Args:
            jid (str): WhatsApp JID
            video_path (str): Path to video file
            caption (str, optional): Video caption
            client: Connection manager instance
            **kwargs: Additional options
            
        Returns:
            Dict[str, Any]: Send result information
        """
        try:
            return await self.send_media(
                jid=jid,
                media_path=video_path,
                media_type='video',
                client=client,
                caption=caption,
                **kwargs
            )
            
        except Exception as e:
            logger.error(f"Failed to send video: {str(e)}")
            raise
    
    async def send_audio(self, jid: str, audio_path: str, caption: str = None, audio_type: str = 'voice', client=None, **kwargs) -> Dict[str, Any]:
        """
        Send an audio file to WhatsApp.
        
        Args:
            jid (str): WhatsApp JID
            audio_path (str): Path to audio file
            caption (str, optional): Audio caption
            audio_type (str): Type of audio ('voice', 'music')
            client: Connection manager instance
            **kwargs: Additional options
            
        Returns:
            Dict[str, Any]: Send result information
        """
        try:
            return await self.send_media(
                jid=jid,
                media_path=audio_path,
                media_type='audio',
                client=client,
                caption=caption,
                audio_type=audio_type,
                **kwargs
            )
            
        except Exception as e:
            logger.error(f"Failed to send audio: {str(e)}")
            raise
    
    async def send_document(self, jid: str, document_path: str, caption: str = None, client=None, **kwargs) -> Dict[str, Any]:
        """
        Send a document to WhatsApp.
        
        Args:
            jid (str): WhatsApp JID
            document_path (str): Path to document file
            caption (str, optional): Document caption
            client: Connection manager instance
            **kwargs: Additional options
            
        Returns:
            Dict[str, Any]: Send result information
        """
        try:
            return await self.send_media(
                jid=jid,
                media_path=document_path,
                media_type='document',
                client=client,
                caption=caption,
                **kwargs
            )
            
        except Exception as e:
            logger.error(f"Failed to send document: {str(e)}")
            raise
    
    async def send_sticker(self, jid: str, sticker_path: str, client=None, **kwargs) -> Dict[str, Any]:
        """
        Send a sticker to WhatsApp.
        
        Args:
            jid (str): WhatsApp JID
            sticker_path (str): Path to sticker file (typically webp format)
            client: Connection manager instance
            **kwargs: Additional options
            
        Returns:
            Dict[str, Any]: Send result information
        """
        try:
            # Validate sticker format
            file_extension = Path(sticker_path).suffix.lower()
            if file_extension != '.webp':
                raise ValueError("Stickers must be in WebP format")
            
            # Validate file size (stickers are smaller)
            file_size = os.path.getsize(sticker_path)
            max_sticker_size = 100 * 1024  # 100KB for stickers
            if file_size > max_sticker_size:
                raise ValueError(f"Sticker file too large ({file_size} bytes), maximum is {max_sticker_size} bytes")
            
            return await self.send_media(
                jid=jid,
                media_path=sticker_path,
                media_type='sticker',
                client=client,
                **kwargs
            )
            
        except Exception as e:
            logger.error(f"Failed to send sticker: {str(e)}")
            raise
    
    async def set_profile_picture(self, image_path: str, client=None) -> Dict[str, Any]:
        """
        Set the profile picture.
        
        Args:
            image_path (str): Path to image file
            client: Connection manager instance
            
        Returns:
            Dict[str, Any]: Update result
        """
        try:
            # Validate image file
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image file not found: {image_path}")
            
            file_extension = Path(image_path).suffix.lower()
            if file_extension not in self.supported_image_types:
                raise ValueError(f"Unsupported image format: {file_extension}")
            
            # Check file size (profile pictures have limits)
            file_size = os.path.getsize(image_path)
            max_profile_size = 5 * 1024 * 1024  # 5MB for profile pictures
            if file_size > max_profile_size:
                raise ValueError(f"Profile picture too large ({file_size} bytes), maximum is {max_profile_size} bytes")
            
            # Prepare profile picture update data
            profile_data = {
                'type': 'set_profile_picture',
                'image_path': image_path,
                'file_name': os.path.basename(image_path),
                'file_size': file_size,
                'mime_type': mimetypes.guess_type(image_path)[0],
                'timestamp': datetime.now().isoformat()
            }
            
            result = await client.send_message(
                jid='0@profile',  # Special JID for profile operations
                message=json.dumps(profile_data),
                message_type='profile_update'
            )
            
            logger.info("Profile picture updated")
            
            return {
                'status': 'updated',
                'file_name': profile_data['file_name'],
                'file_size': file_size,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to set profile picture: {str(e)}")
            raise
    
    async def set_group_picture(self, group_id: str, image_path: str, client=None) -> Dict[str, Any]:
        """
        Set the group picture.
        
        Args:
            group_id (str): Group ID
            image_path (str): Path to image file
            client: Connection manager instance
            
        Returns:
            Dict[str, Any]: Update result
        """
        try:
            # Validate image file
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image file not found: {image_path}")
            
            file_extension = Path(image_path).suffix.lower()
            if file_extension not in self.supported_image_types:
                raise ValueError(f"Unsupported image format: {file_extension}")
            
            # Check file size
            file_size = os.path.getsize(image_path)
            max_group_size = 5 * 1024 * 1024  # 5MB for group pictures
            if file_size > max_group_size:
                raise ValueError(f"Group picture too large ({file_size} bytes), maximum is {max_group_size} bytes")
            
            # Prepare group picture update data
            group_pic_data = {
                'type': 'set_group_picture',
                'group_id': group_id,
                'image_path': image_path,
                'file_name': os.path.basename(image_path),
                'file_size': file_size,
                'mime_type': mimetypes.guess_type(image_path)[0],
                'timestamp': datetime.now().isoformat()
            }
            
            result = await client.send_message(
                jid=group_id,
                message=json.dumps(group_pic_data),
                message_type='group_update'
            )
            
            logger.info(f"Group picture updated for group {group_id}")
            
            return {
                'status': 'updated',
                'group_id': group_id,
                'file_name': group_pic_data['file_name'],
                'file_size': file_size,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to set group picture: {str(e)}")
            raise
    
    def _determine_media_type(self, media_path: str) -> Optional[str]:
        """
        Determine media type based on file extension.
        
        Args:
            media_path (str): Path to media file
            
        Returns:
            Optional[str]: Media type or None if unsupported
        """
        file_extension = Path(media_path).suffix.lower()
        
        if file_extension in self.supported_image_types:
            return 'image'
        elif file_extension in self.supported_video_types:
            return 'video'
        elif file_extension in self.supported_audio_types:
            return 'audio'
        elif file_extension in self.supported_document_types:
            return 'document'
        elif file_extension == '.webp':
            return 'sticker'
        else:
            return None
    
    def _get_max_file_size(self, media_type: str) -> int:
        """
        Get maximum file size for media type.
        
        Args:
            media_type (str): Type of media
            
        Returns:
            int: Maximum file size in bytes
        """
        size_limits = {
            'image': 16 * 1024 * 1024,    # 16MB
            'video': 16 * 1024 * 1024,    # 16MB
            'audio': 16 * 1024 * 1024,    # 16MB
            'document': 100 * 1024 * 1024, # 100MB
            'sticker': 100 * 1024         # 100KB
        }
        
        return size_limits.get(media_type, 16 * 1024 * 1024)  # Default 16MB
    
    async def download_media(self, message_id: str, output_path: str, client=None) -> Dict[str, Any]:
        """
        Download media from a message.
        
        Args:
            message_id (str): Message ID containing the media
            output_path (str): Path to save the downloaded media
            client: Connection manager instance
            
        Returns:
            Dict[str, Any]: Download result
        """
        try:
            # Prepare download request
            download_data = {
                'type': 'download_media',
                'message_id': message_id,
                'output_path': output_path,
                'timestamp': datetime.now().isoformat()
            }
            
            result = await client.send_message(
                jid='0@download',  # Special JID for download operations
                message=json.dumps(download_data),
                message_type='download'
            )
            
            # In a real implementation, this would handle the actual download
            logger.info(f"Media download requested for message {message_id}")
            
            return {
                'status': 'downloading',
                'message_id': message_id,
                'output_path': output_path,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to download media: {str(e)}")
            raise
    
    async def get_media_info(self, media_path: str) -> Dict[str, Any]:
        """
        Get information about a media file.
        
        Args:
            media_path (str): Path to media file
            
        Returns:
            Dict[str, Any]: Media information
        """
        try:
            if not os.path.exists(media_path):
                raise FileNotFoundError(f"Media file not found: {media_path}")
            
            file_stats = os.stat(media_path)
            file_extension = Path(media_path).suffix.lower()
            
            media_info = {
                'file_path': media_path,
                'file_name': os.path.basename(media_path),
                'file_size': file_stats.st_size,
                'file_extension': file_extension,
                'mime_type': mimetypes.guess_type(media_path)[0],
                'media_type': self._determine_media_type(media_path),
                'modified_time': datetime.fromtimestamp(file_stats.st_mtime).isoformat()
            }
            
            # Add media-specific information
            if media_info['media_type'] == 'image':
                # In a real implementation, this would use PIL to get image dimensions
                media_info['width'] = None
                media_info['height'] = None
            
            elif media_info['media_type'] == 'video':
                # In a real implementation, this would use ffmpeg or similar to get video info
                media_info['duration'] = None
            
            elif media_info['media_type'] == 'audio':
                # In a real implementation, this would use audio libraries to get audio info
                media_info['duration'] = None
            
            return media_info
            
        except Exception as e:
            logger.error(f"Failed to get media info: {str(e)}")
            raise
    
    def validate_media_file(self, media_path: str, expected_type: str = None) -> bool:
        """
        Validate if a media file is supported and valid.
        
        Args:
            media_path (str): Path to media file
            expected_type (str, optional): Expected media type
            
        Returns:
            bool: True if file is valid
        """
        try:
            if not os.path.exists(media_path):
                return False
            
            media_type = self._determine_media_type(media_path)
            if not media_type:
                return False
            
            if expected_type and media_type != expected_type:
                return False
            
            # Check file size
            file_size = os.path.getsize(media_path)
            max_size = self._get_max_file_size(media_type)
            if file_size > max_size:
                return False
            
            return True
            
        except Exception:
            return False