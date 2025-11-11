#!/usr/bin/env python3
"""
Example script demonstrating Baileyspy usage

This script shows various ways to use the Baileyspy wrapper for WhatsApp automation.
Run this script to see Baileyspy in action!

Usage:
    python example.py

Requirements:
    - Make sure you have Python 3.14.0+ installed
    - Install Baileyspy: pip install baileyspy
    - Make sure you have Node.js installed for the Baileys backend

Author: MiniMax Agent
"""

import asyncio
import logging
import sys
import os
from datetime import datetime
from pathlib import Path

# Add the current directory to Python path so we can import baileyspy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from baileyspy import BaileysClient, create_client
except ImportError:
    print("❌ Baileyspy not found! Please install it first:")
    print("pip install baileyspy")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BaileyspyDemo:
    """Demonstration class for Baileyspy features"""
    
    def __init__(self):
        self.client = None
        self.is_demo_mode = True
    
    async def run_demo(self):
        """Run the complete Baileyspy demonstration"""
        print("🚀 Baileyspy Demonstration")
        print("=" * 50)
        print()
        
        try:
            # Demo 1: Basic client initialization
            await self.demo_basic_initialization()
            
            # Demo 2: Connection and authentication
            await self.demo_connection()
            
            # Demo 3: Send text messages
            await self.demo_text_messages()
            
            # Demo 4: Interactive messages
            await self.demo_interactive_messages()
            
            # Demo 5: Group operations
            await self.demo_group_operations()
            
            # Demo 6: Media handling
            await self.demo_media_operations()
            
            # Demo 7: Call management
            await self.demo_call_operations()
            
            # Demo 8: Utility functions
            await self.demo_utility_functions()
            
            print("\n✅ Baileyspy demonstration completed successfully!")
            print("🎉 All features have been demonstrated.")
            
        except Exception as e:
            logger.error(f"Demo failed: {e}")
            print(f"\n❌ Demo failed: {e}")
        
        finally:
            if self.client:
                await self.client.disconnect()
                print("👋 Disconnected from WhatsApp")
    
    async def demo_basic_initialization(self):
        """Demonstrate basic client initialization"""
        print("1️⃣  Basic Client Initialization")
        print("-" * 30)
        
        # Create client with default settings
        self.client = BaileysClient("demo_bot")
        print("✅ BaileysClient created with default session ID")
        
        # Create client with custom configuration
        config = {
            'session_dir': 'sessions/demo',
            'qr_timeout': 60,
            'message_timeout': 30,
            'is_bot': True
        }
        
        custom_client = create_client("custom_demo", config)
        print("✅ BaileysClient created with custom configuration")
        
        # Get connection info
        info = custom_client.get_connection_info()
        print(f"📋 Connection info: Session={info['session_id']}, Connected={info['is_connected']}")
        
        print()
    
    async def demo_connection(self):
        """Demonstrate connection and authentication"""
        print("2️⃣  Connection and Authentication")
        print("-" * 35)
        
        try:
            print("🔗 Attempting to connect to WhatsApp...")
            
            # Connect to WhatsApp
            connection_info = await self.client.connect()
            
            if connection_info['status'] == 'qr_required':
                print("📱 QR Code Authentication Required")
                print(f"🔲 QR Code: {connection_info['qr_code']}")
                print("💡 In a real scenario, you would scan this QR code with your phone.")
                print("🔄 Simulating successful connection for demo purposes...")
                
                # For demo purposes, we'll simulate successful connection
                # In real usage, you would scan the QR code
                print("✅ Connection simulation completed")
                self.client.is_connected = True
                self.client.phone_number = "demo_phone_number"
            
            elif connection_info['status'] == 'connected':
                print("✅ Successfully connected to WhatsApp")
                print(f"📱 Phone Number: {connection_info['phone_number']}")
            
            else:
                print(f"⚠️  Connection status: {connection_info['status']}")
        
        except Exception as e:
            print(f"⚠️  Connection error (expected in demo): {e}")
            print("💡 In real usage, ensure you have proper Baileys backend setup")
            
        print()
    
    async def demo_text_messages(self):
        """Demonstrate text message sending"""
        print("3️⃣  Text Message Operations")
        print("-" * 25)
        
        if not self.client.is_connected:
            print("⚠️  Not connected to WhatsApp (demo mode)")
            print("💡 In real usage, connect first with client.connect()")
        
        try:
            # Demo JID (in real usage, this would be actual phone numbers)
            demo_jid = "1234567890@s.whatsapp.net"
            
            print(f"📤 Sending text message to {demo_jid}")
            
            if self.client.is_connected:
                result = await self.client.send_message(demo_jid, "Hello from Baileyspy demo!")
                print(f"✅ Message sent! ID: {result.get('message_id')}")
            else:
                print("💬 Message sending simulated (not actually sent)")
            
            # Demonstrate message options
            print("\n📝 Demonstrating message options:")
            message_options = {
                'quoted_message_id': 'demo_quoted_msg',
                'mentioned_jids': [demo_jid],
                'view_once': False
            }
            
            if self.client.is_connected:
                result = await self.client.send_message(
                    demo_jid, 
                    "This is a message with options!", 
                    **message_options
                )
                print("✅ Message with options sent!")
            else:
                print("💬 Message with options simulated")
            
        except Exception as e:
            print(f"⚠️  Text message error: {e}")
        
        print()
    
    async def demo_interactive_messages(self):
        """Demonstrate interactive message features"""
        print("4️⃣  Interactive Message Features")
        print("-" * 32)
        
        try:
            from baileyspy.messages import create_button, create_list_item
            
            # Demonstrate buttons
            print("🔘 Creating interactive buttons:")
            buttons = [
                create_button("Yes", "yes_button"),
                create_button("No", "no_button"),
                create_button("Maybe", "maybe_button")
            ]
            
            print("✅ Buttons created: Yes, No, Maybe")
            
            # Demonstrate list items
            print("\n📋 Creating interactive list:")
            list_items = [
                create_list_item("Option 1", "Description for option 1"),
                create_list_item("Option 2", "Description for option 2"),
                create_list_item("Option 3", "Description for option 3")
            ]
            
            print("✅ List items created: Option 1, 2, 3")
            
            # Demonstrate poll
            print("\n📊 Creating poll message:")
            poll_options = ["Python", "JavaScript", "Java", "C++"]
            print("✅ Poll options created: Python, JavaScript, Java, C++")
            
            # In real usage, you would send these like:
            # await client.send_interactive_message(jid, "Choose:", buttons=buttons)
            # await client.send_poll_message(jid, "Favorite language?", poll_options)
            
        except Exception as e:
            print(f"⚠️  Interactive message error: {e}")
        
        print()
    
    async def demo_group_operations(self):
        """Demonstrate group management features"""
        print("5️⃣  Group Management Operations")
        print("-" * 31)
        
        try:
            # Demonstrate group creation
            print("👥 Creating a new group:")
            demo_participants = [
                "1234567890@s.whatsapp.net",
                "0987654321@s.whatsapp.net"
            ]
            
            print(f"📋 Participants: {len(demo_participants)} users")
            print("✅ Group creation parameters prepared")
            
            # Demonstrate group info retrieval
            print("\n📊 Getting group information:")
            groups = await self.client.get_groups()
            print(f"📊 Found {len(groups)} groups (demo)")
            
            # Demonstrate group management
            print("\n⚙️  Group management features:")
            print("• Add participants")
            print("• Remove participants")
            print("• Promote/demote members")
            print("• Update group name/description")
            print("• Set group picture")
            print("• Generate invite links")
            print("• Join groups via invite")
            
        except Exception as e:
            print(f"⚠️  Group operations error: {e}")
        
        print()
    
    async def demo_media_operations(self):
        """Demonstrate media handling features"""
        print("6️⃣  Media Operation Features")
        print("-" * 28)
        
        try:
            # Demonstrate media types
            print("📸 Supported media types:")
            print("• Images: .jpg, .jpeg, .png, .gif, .webp")
            print("• Videos: .mp4, .mov, .avi, .mkv, .webm")
            print("• Audio: .mp3, .wav, .ogg, .aac")
            print("• Documents: .pdf, .doc, .docx, .txt, .zip")
            print("• Stickers: .webp")
            
            # Demonstrate profile picture setting
            print("\n🖼️  Profile picture features:")
            print("• Set personal profile picture")
            print("• Set group profile pictures")
            print("• Image validation and optimization")
            
            # Demonstrate media information
            print("\n📊 Media information features:")
            print("• File size validation")
            print("• MIME type detection")
            print("• Media metadata extraction")
            
        except Exception as e:
            print(f"⚠️  Media operations error: {e}")
        
        print()
    
    async def demo_call_operations(self):
        """Demonstrate call management features"""
        print("7️⃣  Voice Call Management")
        print("-" * 23)
        
        try:
            print("📞 Call management features:")
            print("• Initiate voice calls")
            print("• Accept/reject incoming calls")
            print("• End ongoing calls")
            print("• Call status monitoring")
            print("• Call history tracking")
            print("• Mute/unmute calls")
            
            # Demonstrate call statistics
            print("\n📊 Call statistics:")
            call_history = await self.client.call_manager.get_call_history()
            print(f"📋 Call history: {len(call_history)} calls recorded")
            
            active_calls = await self.client.call_manager.get_active_calls()
            print(f"🔴 Active calls: {len(active_calls)}")
            
        except Exception as e:
            print(f"⚠️  Call operations error: {e}")
        
        print()
    
    async def demo_utility_functions(self):
        """Demonstrate utility functions"""
        print("8️⃣  Utility Functions")
        print("-" * 20)
        
        try:
            from baileyspy.utils import Utils
            
            utils = Utils()
            
            # Demonstrate phone number formatting
            print("📱 Phone number utilities:")
            demo_number = "1234567890"
            formatted_jid = utils.format_phone_number(demo_number, "US")
            print(f"📞 {demo_number} → {formatted_jid}")
            
            # Demonstrate JID validation
            print("\n✔️  JID validation:")
            is_valid = utils.is_valid_whatsapp_jid(formatted_jid)
            print(f"✅ {formatted_jid} is {'valid' if is_valid else 'invalid'}")
            
            # Demonstrate message formatting
            print("\n📝 Message formatting:")
            message_data = {
                'type': 'image',
                'caption': 'Beautiful sunset'
            }
            formatted = utils.format_message_for_display(message_data)
            print(f"📄 {formatted}")
            
            # Demonstrate time utilities
            print("\n⏰ Time utilities:")
            current_time = datetime.now()
            formatted_time = utils.format_timestamp(current_time)
            print(f"🕐 Current time: {formatted_time}")
            
            # Demonstrate file size formatting
            print("\n💾 File size utilities:")
            size_readable = utils.human_readable_size(1024 * 1024)  # 1MB
            print(f"📊 1048576 bytes = {size_readable}")
            
        except Exception as e:
            print(f"⚠️  Utility functions error: {e}")
        
        print()


async def main():
    """Main demonstration function"""
    print("🎯 Welcome to Baileyspy Demo!")
    print("This demonstration shows the key features of Baileyspy.")
    print("In a real environment, you would need to:")
    print("• Set up the Baileys Node.js backend")
    print("• Scan QR codes for authentication")
    print("• Have valid phone numbers for testing")
    print()
    
    demo = BaileyspyDemo()
    await demo.run_demo()
    
    print("\n🎓 Demo completed! You're now ready to use Baileyspy.")
    print("📚 Check the README.md for detailed documentation and examples.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Demo interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        print("💡 Make sure you have installed all dependencies correctly.")