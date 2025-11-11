# Baileyspy 🤖

**Baileyspy** is a comprehensive Python wrapper for the [Baileys WhatsApp library](https://github.com/angstvorfrauen/Baileys), providing a robust and easy-to-use interface for WhatsApp automation and bot development. Built on top of the powerful Baileys JavaScript library, Baileyspy brings Pythonic elegance to WhatsApp bot development while maintaining full feature parity with the original Baileys library.

[![Python 3.14+](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](https://github.com/angstvorfrauen/Baileys)
[![Status](https://img.shields.io/badge/status-stable-brightgreen.svg)]()

## ✨ Features

### 🔗 **Core Connection Management**
- **WhatsApp Web Protocol Integration**: Full compatibility with WhatsApp Web's latest protocol version (2.3000.1028620558)
- **QR Code Authentication**: Seamless QR code scanning and authentication process
- **Custom Pairing Codes**: Support for custom pairing codes (e.g., 'AAAA-AAAA') with Baileys's pairing system
- **Session Persistence**: Automatic session management and restoration
- **Multi-Device Support**: Works with linked devices, optimized for iOS/Safari
- **Signal Protocol Integration**: Built-in libsignal-xeuka for enhanced encryption

### 📱 **Comprehensive Messaging**
- **Text Messages**: Send and receive text messages with full formatting support
- **Media Support**: Send images, videos, documents, audio files, and stickers
- **Interactive Messages**: Create buttons, lists, and polls for enhanced user engagement
- **Message Reactions**: Add reactions to messages with emoji support
- **Ephemeral Messages**: Send disappearing messages with configurable timeouts
- **Reply System**: Reply to specific messages with threading support
- **Typing Indicators**: Send and receive typing status notifications
- **Message Status**: Track message delivery, read receipts, and status

### 👥 **Group Management**
- **Group Creation**: Create groups with customizable settings
- **Member Management**: Add, remove, promote, and demote group participants
- **Group Settings**: Configure group name, description, and permissions
- **Group Pictures**: Set and manage group profile pictures
- **Invite Links**: Generate, revoke, and use group invite links
- **Group Polls**: Create and manage polls within groups
- **Group Admin Features**: Full administrative control over group operations

### 📞 **Call Management**
- **Voice Calls**: Initiate voice calls to any WhatsApp user
- **Call Control**: Accept, reject, and manage ongoing calls
- **Call Status**: Real-time call status monitoring and management
- **Call History**: Track and retrieve call history information
- **Call Statistics**: Detailed call analytics and reporting

### 🔐 **Security & Authentication**
- **Secure Pairing**: Safe device pairing with custom pairing codes
- **Session Management**: Secure session storage and management
- **Token Validation**: Automatic token validation and renewal
- **Device Linking**: Support for multiple device linking scenarios

### 📊 **Media Handling**
- **File Upload**: Support for various media formats with automatic type detection
- **Image Processing**: Advanced image handling with quality optimization
- **Video Processing**: Video file handling with duration and metadata extraction
- **Document Support**: PDF, Office documents, and various file formats
- **Profile Management**: Set profile pictures and group pictures
- **Media Download**: Download media from incoming messages

### 🛠️ **Developer Tools**
- **Event System**: Comprehensive event handling for all WhatsApp activities
- **Async/Await Support**: Full asynchronous programming support
- **Logging**: Detailed logging and debugging capabilities
- **Error Handling**: Robust error handling and recovery mechanisms
- **Type Hints**: Full type annotation support for better development experience

## 🚀 Installation

### Prerequisites

Before installing Baileyspy, ensure you have:

- **Python 3.14.0 or higher**
- **Node.js 14+** (required for Baileys backend)
- **npm or yarn** (for Baileys dependencies)

### Installation Methods

#### Method 1: pip install (Recommended)

```bash
pip install baileyspy
```

#### Method 2: Development Installation

```bash
git clone https://github.com/angstvorfrauen/Baileys.git
cd Baileys
pip install -e .
```

#### Method 3: Install with Development Dependencies

```bash
pip install baileyspy[dev]
```

#### Method 4: Install with Documentation Tools

```bash
pip install baileyspy[docs]
```

### Dependencies

Baileyspy requires the following Python packages:

```
requests>=2.25.0
websocket-client>=1.3.0
aiofiles>=0.7.0
python-dotenv>=0.19.0
```

Optional dependencies for enhanced functionality:
```
pillow>=8.0.0
beautifulsoup4>=4.9.0
jsonschema>=3.2.0
colorama>=0.4.4
rich>=12.0.0
```

## 📖 Quick Start Guide

### Basic Usage Example

```python
import asyncio
from baileyspy import BaileysClient

async def main():
    # Initialize the client
    client = BaileysClient(session_id="my_bot")
    
    # Connect to WhatsApp
    connection_info = await client.connect()
    
    if connection_info['status'] == 'qr_required':
        print("Scan the QR code to connect:")
        print(f"QR Code: {connection_info['qr_code']}")
        
        # Wait for connection (in a real scenario, user would scan QR)
        connection_info = await client.connect()
    
    if connection_info['status'] == 'connected':
        print(f"Connected as: {connection_info['phone_number']}")
        
        # Send a message
        await client.send_message("1234567890@s.whatsapp.net", "Hello from Baileyspy!")
        
        # Create a group
        groups = await client.get_groups()
        print(f"Available groups: {len(groups)}")

# Run the bot
asyncio.run(main())
```

### Event-Driven Bot Example

```python
import asyncio
from baileyspy import BaileysClient

async def on_message(client, message):
    """Handle incoming messages."""
    if message['from_me']:
        return  # Skip self-messages
    
    sender = message['sender']
    content = message['content']
    
    # Respond to commands
    if content.startswith('!help'):
        help_text = """
🤖 Baileyspy Bot Commands:
!help - Show this help message
!ping - Check bot status
!time - Current time
!groups - List available groups
        """
        await client.send_message(sender, help_text)
    
    elif content.startswith('!ping'):
        await client.send_message(sender, "🏓 Pong! Bot is online.")
    
    elif content.startswith('!time'):
        from datetime import datetime
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await client.send_message(sender, f"🕐 Current time: {current_time}")

async def on_connect(client, info):
    """Handle connection events."""
    print(f"Connected to WhatsApp: {info['phone_number']}")
    print("Bot is ready to receive messages!")

async def main():
    client = BaileysClient(session_id="event_bot")
    
    # Register event handlers
    client.on('message', on_message)
    client.on('connected', on_connect)
    
    # Connect and start listening
    await client.connect()
    
    # Keep the bot running
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await client.disconnect()

asyncio.run(main())
```

## 📚 Detailed Documentation

### Configuration Options

Baileyspy provides extensive configuration options:

```python
config = {
    'session_dir': 'sessions/my_bot',
    'qr_timeout': 60,
    'message_timeout': 30,
    'pairing_code': 'BBBB-CCCC',
    'is_bot': True,
    'connection_retries': 5,
    'max_message_size': 16 * 1024 * 1024,  # 16MB
    'media_quality': 'high',
    'enable_logging': True,
    'log_level': 'INFO'
}

client = BaileysClient(session_id="configured_bot", config=config)
```

### Message Types

#### Text Messages

```python
# Simple text message
await client.send_message("jid@s.whatsapp.net", "Hello World!")

# Message with options
await client.send_message(
    "jid@s.whatsapp.net", 
    "Bold message",
    quoted_message_id="message_id",
    mentioned_jids=["jid@s.whatsapp.net"],
    view_once=True
)
```

#### Media Messages

```python
# Send image
await client.send_image("jid@s.whatsapp.net", "path/to/image.jpg", 
                       caption="Check this out!")

# Send video
await client.send_video("jid@s.whatsapp.net", "path/to/video.mp4",
                       caption="Cool video!")

# Send document
await client.send_document("jid@s.whatsapp.net", "path/to/document.pdf")

# Send audio
await client.send_audio("jid@s.whatsapp.net", "path/to/audio.mp3", 
                       audio_type="voice")

# Send sticker
await client.send_sticker("jid@s.whatsapp.net", "path/to/sticker.webp")
```

#### Interactive Messages

```python
from baileyspy.messages import create_button, create_list_item

# Buttons
buttons = [
    create_button("Yes", "yes"),
    create_button("No", "no"),
    create_button("Maybe", "maybe")
]

await client.send_interactive_message(
    "jid@s.whatsapp.net",
    "Do you agree?",
    buttons=buttons
)

# List messages
list_items = [
    create_list_item("Option 1", "Description 1"),
    create_list_item("Option 2", "Description 2"),
    create_list_item("Option 3", "Description 3")
]

await client.send_interactive_message(
    "jid@s.whatsapp.net",
    "Choose an option:",
    list_items=list_items
)

# Poll messages
poll_options = ["Yes", "No", "Maybe"]
await client.send_poll_message(
    "jid@s.whatsapp.net",
    "Do you like Python?",
    poll_options,
    multiple_answers=False
)
```

#### Ephemeral Messages

```python
# 24-hour ephemeral message
await client.send_ephemeral_message(
    "jid@s.whatsapp.net",
    "This message will disappear in 24 hours",
    ephemeral_duration=24 * 60 * 60
)
```

### Group Operations

#### Group Management

```python
# Create a group
participants = ["jid1@s.whatsapp.net", "jid2@s.whatsapp.net"]
group_info = await client.create_group(
    name="My Awesome Group",
    participants=participants,
    description="A group for awesome people"
)

# Get all groups
groups = await client.get_groups()
for group in groups:
    print(f"Group: {group['name']} ({group['member_count']} members)")

# Add participants to group
await client.add_participants(
    group_info['group_id'],
    ["jid3@s.whatsapp.net", "jid4@s.whatsapp.net"]
)

# Set group picture
await client.set_group_picture(
    group_info['group_id'],
    "path/to/group_picture.jpg"
)

# Get invite link
invite_info = await client.get_invite_link(group_info['group_id'])
print(f"Join link: {invite_info['invite_link']}")

# Join group via invite link
joined_info = await client.join_group(invite_info['invite_link'])
```

### Call Management

```python
# Initiate a call
call_info = await client.offer_call("jid@s.whatsapp.net")
print(f"Call initiated: {call_info['call_id']}")

# Accept a call
await client.accept_call(call_info['call_id'])

# End a call
await client.end_call(call_info['call_id'])

# Get call history
call_history = await client.get_call_history(limit=10)
for call in call_history:
    print(f"Call with {call['jid']}: {call['duration']} seconds")
```

### Media Operations

```python
# Set profile picture
await client.set_profile_picture("path/to/profile.jpg")

# Download media from message
download_info = await client.download_media(
    message_id="message_id",
    output_path="downloaded_media"
)

# Get media information
media_info = client.media_handler.get_media_info("path/to/media.jpg")
print(f"Media type: {media_info['media_type']}")
print(f"File size: {media_info['file_size']} bytes")
```

### Device Pairing

```python
# Request custom pairing code
pairing_info = await client.pairing_manager.request_pairing_code(
    number="1234567890",
    code="DDDD-EEEE"
)
print(f"Pairing code: {pairing_info['pairing_code']}")

# Verify pairing code
await client.pairing_manager.verify_pairing_code(
    pairing_info['pairing_id'],
    "DDDD-EEEE"
)

# Complete pairing
auth_info = await client.pairing_manager.complete_pairing(
    pairing_info['pairing_id']
)
print(f"Device paired: {auth_info['device_id']}")
```

## 🔧 Advanced Features

### Custom Event Handlers

```python
async def custom_message_handler(client, message):
    """Custom message processing."""
    # Implement your custom logic here
    pass

async def custom_call_handler(event_type, call_info):
    """Custom call event handling."""
    # Handle call events
    if event_type == 'incoming_call':
        print(f"Incoming call from {call_info['jid']}")
    elif event_type == 'call_ended':
        print(f"Call ended, duration: {call_info['duration']}s")

# Register custom handlers
client.message_handler.register_message_handler(custom_message_handler)
client.call_manager.register_call_handler(custom_call_handler)
```

### Async Context Manager

```python
async with BaileysClient("context_bot") as client:
    connection_info = await client.connect()
    if connection_info['status'] == 'connected':
        await client.send_message("jid@s.whatsapp.net", "Hello from context manager!")
    # Connection automatically closed when exiting context
```

### Session Management

```python
# Save session to file
await client.save_session("custom_session.json")

# Load session from file
await client.load_session("custom_session.json")

# Get connection info
info = client.get_connection_info()
print(f"Connected: {info['is_connected']}")
print(f"Phone: {info['phone_number']}")
```

### Utility Functions

```python
from baileyspy.utils import Utils

utils = Utils()

# Format phone numbers
jid = utils.format_phone_number("1234567890", country_code="US")
print(jid)  # "11234567890@s.whatsapp.net"

# Validate JIDs
is_valid = utils.is_valid_whatsapp_jid("1234567890@s.whatsapp.net")
print(is_valid)  # True

# Format message for display
message_data = {"type": "image", "caption": "Beautiful sunset"}
display_text = utils.format_message_for_display(message_data)
print(display_text)  # "[Image] Beautiful sunset"

# Generate unique message ID
msg_id = utils.generate_message_id()
print(msg_id)  # "msg_1634567890123_abcdef12"
```

## 🏗️ Architecture

### Project Structure

```
baileyspy/
├── __init__.py           # Package initialization and exports
├── client.py            # Main BaileysClient class
├── connection.py        # Connection and authentication management
├── messages.py          # Message sending and receiving
├── groups.py            # Group management operations
├── call_manager.py      # Voice call handling
├── pairing.py           # Device pairing and authentication
├── media.py             # Media file handling
├── utils.py             # Utility functions and helpers
├── requirements.txt     # Python dependencies
└── setup.py            # Package installation script
```

### Key Components

1. **BaileysClient**: Main client class that orchestrates all operations
2. **ConnectionManager**: Handles WhatsApp Web connection and authentication
3. **MessageHandler**: Manages message sending, receiving, and formatting
4. **GroupManager**: Provides group creation and management functionality
5. **CallManager**: Handles voice call operations and call state management
6. **PairingManager**: Manages device pairing and custom pairing codes
7. **MediaHandler**: Processes media files and profile picture operations
8. **Utils**: Utility functions for common operations and data processing

## 🛡️ Security Considerations

### Best Practices

1. **Session Security**: Always store sessions in secure directories with appropriate permissions
2. **API Keys**: Never commit API keys or authentication tokens to version control
3. **Rate Limiting**: Implement rate limiting to avoid being flagged as spam
4. **Content Filtering**: Filter and validate all user content before processing
5. **Error Handling**: Implement proper error handling to prevent information leakage

### Environment Variables

Use environment variables for sensitive configuration:

```python
import os
from dotenv import load_dotenv

load_dotenv()

config = {
    'session_dir': os.getenv('BAILEYS_SESSION_DIR', 'sessions/default'),
    'api_key': os.getenv('WHATSAPP_API_KEY'),
    'max_retries': int(os.getenv('MAX_RETRIES', '3'))
}
```

## 📋 Examples

### Complete Bot Example

```python
import asyncio
import logging
from datetime import datetime
from baileyspy import BaileysClient, create_client

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WhatsAppBot:
    def __init__(self, session_id="my_bot"):
        self.client = create_client(session_id)
        self.setup_handlers()
    
    def setup_handlers(self):
        """Setup event handlers."""
        self.client.on('message', self.handle_message)
        self.client.on('connected', self.handle_connect)
        self.client.on('disconnected', self.handle_disconnect)
    
    async def handle_message(self, client, message):
        """Handle incoming messages."""
        try:
            if message.get('from_me'):
                return
            
            sender = message['sender']
            content = message.get('content', '')
            
            # Simple command system
            if content.startswith('!time'):
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                await client.send_message(sender, f"🕐 {current_time}")
            
            elif content.startswith('!stats'):
                groups = await client.get_groups()
                info = client.get_connection_info()
                stats_text = f"""
📊 Bot Statistics:
• Connected: {info['is_connected']}
• Phone: {info['phone_number']}
• Groups: {len(groups)}
• Session: {info['session_id']}
                """
                await client.send_message(sender, stats_text)
            
            elif content.startswith('!groups'):
                groups = await client.get_groups()
                if groups:
                    group_list = "\n".join([
                        f"• {group['name']} ({group['member_count']} members)"
                        for group in groups[:5]
                    ])
                    await client.send_message(sender, f"📋 Your groups:\n{group_list}")
                else:
                    await client.send_message(sender, "❌ No groups found")
            
            elif content.startswith('!ping'):
                await client.send_message(sender, "🏓 Pong! Bot is online and ready!")
            
            elif content.startswith('!help'):
                help_text = """
🤖 **WhatsApp Bot Commands**

🕐 `!time` - Show current time
📊 `!stats` - Show bot statistics  
📋 `!groups` - List your groups
🏓 `!ping` - Check bot status
❓ `!help` - Show this help message

*Powered by Baileyspy* 🚀
                """
                await client.send_message(sender, help_text)
            
            # Echo non-command messages (demo)
            else:
                response = f"👋 I received: '{content}'\n\nType !help for available commands!"
                await client.send_message(sender, response)
        
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            await client.send_message(sender, "❌ An error occurred while processing your message.")
    
    async def handle_connect(self, client, info):
        """Handle connection event."""
        logger.info(f"Connected to WhatsApp: {info['phone_number']}")
        print(f"✅ Bot connected as: {info['phone_number']}")
        print("🤖 Bot is ready to receive messages!")
        print("📱 Send '!help' to this number to see available commands.")
    
    async def handle_disconnect(self, client, info):
        """Handle disconnection event."""
        logger.warning(f"Disconnected from WhatsApp: {info}")
    
    async def start(self):
        """Start the bot."""
        try:
            print("🚀 Starting WhatsApp Bot...")
            connection_info = await self.client.connect()
            
            if connection_info['status'] == 'qr_required':
                print("📱 Please scan the QR code to connect:")
                print(f"QR Code: {connection_info['qr_code']}")
                
                # Wait for QR scan
                while True:
                    try:
                        connection_info = await self.client.connect()
                        if connection_info['status'] == 'connected':
                            break
                        await asyncio.sleep(2)
                    except Exception as e:
                        logger.error(f"Connection check failed: {e}")
                        await asyncio.sleep(5)
            
            # Keep bot running
            try:
                while True:
                    await asyncio.sleep(10)
            except KeyboardInterrupt:
                print("\n🛑 Bot stopped by user")
            finally:
                await self.client.disconnect()
        
        except Exception as e:
            logger.error(f"Bot failed to start: {e}")
            raise

# Run the bot
if __name__ == "__main__":
    bot = WhatsAppBot()
    asyncio.run(bot.start())
```

### Media Bot Example

```python
import asyncio
from baileyspy import BaileysClient

class MediaBot:
    def __init__(self):
        self.client = BaileysClient("media_bot")
        self.setup_handlers()
    
    def setup_handlers(self):
        self.client.on('message', self.handle_media_request)
    
    async def handle_media_request(self, client, message):
        """Handle media-related requests."""
        if message.get('from_me'):
            return
        
        sender = message['sender']
        content = message.get('content', '')
        
        if content.startswith('!image'):
            # Send an image
            await client.send_image(
                sender,
                "examples/sample_image.jpg",
                caption="🖼️ Sample image sent via Baileyspy!"
            )
        
        elif content.startswith('!video'):
            # Send a video
            await client.send_video(
                sender,
                "examples/sample_video.mp4",
                caption="🎬 Sample video sent via Baileyspy!"
            )
        
        elif content.startswith('!profile'):
            # Set profile picture (demo)
            await client.send_message(
                sender,
                "📸 To set your profile picture, use:\n!set_profile path/to/image.jpg"
            )
        
        elif content.startswith('!set_profile'):
            # Parse file path from message
            parts = content.split(' ', 1)
            if len(parts) > 1:
                image_path = parts[1].strip()
                try:
                    await client.set_profile_picture(image_path)
                    await client.send_message(sender, "✅ Profile picture updated!")
                except Exception as e:
                    await client.send_message(sender, f"❌ Error: {str(e)}")
            else:
                await client.send_message(sender, "📝 Usage: !set_profile path/to/image.jpg")

async def main():
    bot = MediaBot()
    await bot.client.connect()
    print("📸 Media Bot ready!")
    
    # Keep running
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await bot.client.disconnect()

asyncio.run(main())
```

## 🤝 Contributing

We welcome contributions to Baileyspy! Here's how you can help:

### Development Setup

1. **Fork the repository**
2. **Clone your fork**:
   ```bash
   git clone https://github.com/your-username/Baileys.git
   cd Baileys
   ```

3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install development dependencies**:
   ```bash
   pip install -e .[dev]
   ```

5. **Install pre-commit hooks**:
   ```bash
   pre-commit install
   ```

### Development Guidelines

1. **Code Style**: Follow PEP 8 and use `black` for formatting
2. **Type Hints**: Add type hints to all new functions and classes
3. **Documentation**: Add docstrings to all public functions
4. **Testing**: Write tests for new features
5. **Commits**: Use conventional commit messages

### Testing

Run tests with:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=baileyspy

# Run specific test file
pytest tests/test_client.py
```

### Pull Request Process

1. Create a feature branch
2. Make your changes
3. Add tests for new functionality
4. Update documentation
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Baileys Library**: [angstvorfrauen/Baileys](https://github.com/angstvorfrauen/Baileys) - The powerful JavaScript WhatsApp library this wrapper is built upon
- **WhatsApp Web**: For providing the protocol that enables automation
- **Python Community**: For the excellent libraries and tools that make this wrapper possible

## 📞 Support

### Getting Help

- **Documentation**: Check this README and the [Wiki](https://github.com/angstvorfrauen/Baileys/wiki)
- **Issues**: Report bugs and request features in [GitHub Issues](https://github.com/angstvorfrauen/Baileys/issues)
- **Discussions**: Join discussions in [GitHub Discussions](https://github.com/angstvorfrauen/Baileys/discussions)

### Common Issues

**Q: Connection fails with QR code**
A: Ensure your internet connection is stable and try again. The QR code expires after a short time.

**Q: Media files not sending**
A: Check file size limits (16MB for media, 100MB for documents) and supported formats.

**Q: Bot stops responding**
A: Check the logs for error messages and ensure your session file is not corrupted.

### Troubleshooting

Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

client = BaileysClient("debug_bot")
```

## 🔮 Roadmap

### Version 1.1.0 (Planned)
- [ ] Enhanced media processing capabilities
- [ ] Improved error handling and recovery
- [ ] Additional message types support
- [ ] Performance optimizations

### Version 1.2.0 (Future)
- [ ] Webhook support for real-time events
- [ ] Database integration for message storage
- [ ] Advanced analytics and reporting
- [ ] Multi-language support

### Long-term Goals
- [ ] Official WhatsApp Business API integration
- [ ] Machine learning for message classification
- [ ] Advanced automation features
- [ ] Enterprise-grade features

---

**Made with ❤️ by MiniMax Agent**

*Transform your WhatsApp automation dreams into reality with Baileyspy!* 🚀