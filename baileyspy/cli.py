"""
CLI module for Baileyspy - Command line interface for Baileyspy wrapper

Author: MiniMax Agent
"""

import asyncio
import click
import sys
import json
from pathlib import Path
from datetime import datetime
from baileyspy import BaileysClient, create_client


@click.group()
@click.option('--session-id', default='cli_bot', help='Session ID for the bot')
@click.option('--config-file', type=click.Path(), help='Configuration file path')
@click.pass_context
def cli(ctx, session_id, config_file):
    """Baileyspy - WhatsApp Bot Command Line Interface"""
    ctx.ensure_object(dict)
    
    # Load configuration
    config = {}
    if config_file and Path(config_file).exists():
        with open(config_file, 'r') as f:
            config = json.load(f)
    
    ctx.obj['config'] = config
    ctx.obj['session_id'] = session_id


@cli.command()
@click.option('--phone', required=True, help='Phone number (with country code)')
@click.option('--message', required=True, help='Message to send')
@click.pass_context
def send(ctx, phone, message):
    """Send a message to a phone number"""
    async def send_message():
        try:
            config = ctx.obj.get('config', {})
            client = create_client(ctx.obj['session_id'], config)
            
            # Connect
            connection_info = await client.connect()
            if connection_info['status'] == 'qr_required':
                click.echo(f"QR Code: {connection_info['qr_code']}")
                click.echo("Please scan the QR code and run the command again.")
                return
            
            # Send message
            # Format phone number to JID
            from baileyspy.utils import Utils
            utils = Utils()
            jid = utils.format_phone_number(phone, add_suffix=True)
            
            result = await client.send_message(jid, message)
            click.echo(f"✅ Message sent successfully to {phone}")
            click.echo(f"Message ID: {result.get('message_id')}")
            
            await client.disconnect()
            
        except Exception as e:
            click.echo(f"❌ Error: {e}", err=True)
            sys.exit(1)
    
    asyncio.run(send_message())


@cli.command()
@click.pass_context
def status(ctx):
    """Show bot connection status"""
    async def show_status():
        try:
            config = ctx.obj.get('config', {})
            client = create_client(ctx.obj['session_id'], config)
            
            connection_info = client.get_connection_info()
            
            click.echo("🤖 Baileyspy Bot Status")
            click.echo("=" * 30)
            click.echo(f"Session ID: {connection_info['session_id']}")
            click.echo(f"Connected: {'✅ Yes' if connection_info['is_connected'] else '❌ No'}")
            if connection_info['phone_number']:
                click.echo(f"Phone Number: {connection_info['phone_number']}")
            
            if connection_info['is_connected']:
                click.echo("Status: 🟢 Online and ready")
            else:
                click.echo("Status: ⚫ Offline")
                
        except Exception as e:
            click.echo(f"❌ Error: {e}", err=True)
            sys.exit(1)
    
    asyncio.run(show_status())


@cli.command()
@click.pass_context
def groups(ctx):
    """List all available groups"""
    async def list_groups():
        try:
            config = ctx.obj.get('config', {})
            client = create_client(ctx.obj['session_id'], config)
            
            # Connect
            connection_info = await client.connect()
            if connection_info['status'] == 'qr_required':
                click.echo(f"QR Code: {connection_info['qr_code']}")
                click.echo("Please scan the QR code and run the command again.")
                return
            
            # Get groups
            groups = await client.get_groups()
            
            click.echo("📋 WhatsApp Groups")
            click.echo("=" * 30)
            
            if groups:
                for i, group in enumerate(groups, 1):
                    click.echo(f"{i}. {group.get('name', 'Unnamed Group')}")
                    click.echo(f"   ID: {group.get('group_id', 'Unknown')}")
                    click.echo(f"   Members: {group.get('member_count', 0)}")
                    click.echo("")
            else:
                click.echo("No groups found.")
            
            await client.disconnect()
            
        except Exception as e:
            click.echo(f"❌ Error: {e}", err=True)
            sys.exit(1)
    
    asyncio.run(list_groups())


@cli.command()
@click.option('--name', required=True, help='Group name')
@click.option('--participants', multiple=True, help='Participant phone numbers')
@click.option('--description', help='Group description')
@click.pass_context
def create_group(ctx, name, participants, description):
    """Create a new WhatsApp group"""
    async def create_new_group():
        try:
            config = ctx.obj.get('config', {})
            client = create_client(ctx.obj['session_id'], config)
            
            # Connect
            connection_info = await client.connect()
            if connection_info['status'] == 'qr_required':
                click.echo(f"QR Code: {connection_info['qr_code']}")
                click.echo("Please scan the QR code and run the command again.")
                return
            
            # Format participant numbers to JIDs
            from baileyspy.utils import Utils
            utils = Utils()
            participant_jids = []
            
            for phone in participants:
                jid = utils.format_phone_number(phone, add_suffix=True)
                participant_jids.append(jid)
            
            # Create group
            group_info = await client.create_group(
                name=name,
                participants=participant_jids,
                description=description
            )
            
            click.echo(f"✅ Group '{name}' created successfully!")
            click.echo(f"Group ID: {group_info['group_id']}")
            click.echo(f"Participants: {len(participant_jids)}")
            
            await client.disconnect()
            
        except Exception as e:
            click.echo(f"❌ Error: {e}", err=True)
            sys.exit(1)
    
    asyncio.run(create_new_group())


@cli.command()
@click.option('--jid', required=True, help='WhatsApp JID')
@click.option('--message', required=True, help='Message content')
@click.option('--caption', help='Media caption (for media messages)')
@click.option('--media-type', type=click.Choice(['image', 'video', 'audio', 'document']), 
              help='Media type')
@click.option('--media-path', type=click.Path(), help='Media file path')
@click.pass_context
def interactive_message(ctx, jid, message, caption, media_type, media_path):
    """Send an interactive message"""
    async def send_interactive():
        try:
            config = ctx.obj.get('config', {})
            client = create_client(ctx.obj['session_id'], config)
            
            # Connect
            connection_info = await client.connect()
            if connection_info['status'] == 'qr_required':
                click.echo(f"QR Code: {connection_info['qr_code']}")
                click.echo("Please scan the QR code and run the command again.")
                return
            
            if media_type and media_path:
                # Send media
                if media_type == 'image':
                    await client.send_image(jid, media_path, caption=caption)
                elif media_type == 'video':
                    await client.send_video(jid, media_path, caption=caption)
                elif media_type == 'audio':
                    await client.send_audio(jid, media_path, caption=caption)
                elif media_type == 'document':
                    await client.send_document(jid, media_path, caption=caption)
                
                click.echo(f"✅ {media_type.capitalize()} sent successfully to {jid}")
            else:
                # Send text message
                await client.send_message(jid, message)
                click.echo(f"✅ Message sent successfully to {jid}")
            
            await client.disconnect()
            
        except Exception as e:
            click.echo(f"❌ Error: {e}", err=True)
            sys.exit(1)
    
    asyncio.run(send_interactive())


@cli.command()
@click.option('--jid', required=True, help='WhatsApp JID to call')
@click.pass_context
def call(ctx, jid):
    """Initiate a voice call"""
    async def make_call():
        try:
            config = ctx.obj.get('config', {})
            client = create_client(ctx.obj['session_id'], config)
            
            # Connect
            connection_info = await client.connect()
            if connection_info['status'] == 'qr_required':
                click.echo(f"QR Code: {connection_info['qr_code']}")
                click.echo("Please scan the QR code and run the command again.")
                return
            
            # Make call
            call_info = await client.offer_call(jid)
            click.echo(f"📞 Call initiated to {jid}")
            click.echo(f"Call ID: {call_info['call_id']}")
            
            await client.disconnect()
            
        except Exception as e:
            click.echo(f"❌ Error: {e}", err=True)
            sys.exit(1)
    
    asyncio.run(make_call())


@cli.command()
@click.option('--phone', required=True, help='Phone number to pair')
@click.option('--code', help='Custom pairing code')
@click.pass_context
def pair(ctx, phone, code):
    """Request a pairing code for device linking"""
    async def request_pairing():
        try:
            config = ctx.obj.get('config', {})
            client = create_client(ctx.obj['session_id'], config)
            
            # Request pairing code
            pairing_info = await client.pairing_manager.request_pairing_code(phone, code)
            click.echo("🔗 Device Pairing Requested")
            click.echo("=" * 30)
            click.echo(f"Phone Number: {phone}")
            click.echo(f"Pairing Code: {pairing_info['pairing_code']}")
            click.echo(f"Pairing ID: {pairing_info['pairing_id']}")
            click.echo("")
            click.echo("Use this pairing code on the target device to link.")
            
        except Exception as e:
            click.echo(f"❌ Error: {e}", err=True)
            sys.exit(1)
    
    asyncio.run(request_pairing())


@cli.command()
@click.option('--image-path', required=True, type=click.Path(), help='Image file path')
@click.pass_context
def set_profile(ctx, image_path):
    """Set profile picture"""
    async def update_profile():
        try:
            config = ctx.obj.get('config', {})
            client = create_client(ctx.obj['session_id'], config)
            
            # Connect
            connection_info = await client.connect()
            if connection_info['status'] == 'qr_required':
                click.echo(f"QR Code: {connection_info['qr_code']}")
                click.echo("Please scan the QR code and run the command again.")
                return
            
            # Set profile picture
            result = await client.set_profile_picture(image_path)
            click.echo("✅ Profile picture updated successfully!")
            click.echo(f"Image: {result['file_name']}")
            click.echo(f"Size: {result['file_size']} bytes")
            
            await client.disconnect()
            
        except Exception as e:
            click.echo(f"❌ Error: {e}", err=True)
            sys.exit(1)
    
    asyncio.run(update_profile())


@cli.command()
@click.pass_context
def interactive(ctx):
    """Start interactive bot mode"""
    async def interactive_mode():
        try:
            config = ctx.obj.get('config', {})
            client = create_client(ctx.obj['session_id'], config)
            
            click.echo("🤖 Baileyspy Interactive Mode")
            click.echo("=" * 35)
            click.echo("Type 'help' for available commands")
            click.echo("Type 'quit' to exit")
            click.echo("")
            
            # Connect
            connection_info = await client.connect()
            if connection_info['status'] == 'qr_required':
                click.echo(f"QR Code: {connection_info['qr_code']}")
                click.echo("Please scan the QR code and run the command again.")
                return
            
            click.echo(f"✅ Connected as: {connection_info['phone_number']}")
            click.echo("")
            
            # Interactive loop
            while True:
                try:
                    user_input = click.prompt("baileyspy> ", default="")
                    user_input = user_input.strip()
                    
                    if not user_input:
                        continue
                    
                    if user_input.lower() in ['quit', 'exit', 'q']:
                        break
                    
                    elif user_input.lower() == 'help':
                        click.echo("""
Available commands:
• status - Show connection status
• groups - List all groups
• quit - Exit interactive mode

Examples:
• send +1234567890 Hello World
• groups
• call +1234567890
                        """)
                    
                    elif user_input.startswith('send '):
                        # Parse send command
                        parts = user_input.split(' ', 2)
                        if len(parts) >= 3:
                            phone = parts[1]
                            message = parts[2]
                            
                            from baileyspy.utils import Utils
                            utils = Utils()
                            jid = utils.format_phone_number(phone, add_suffix=True)
                            
                            await client.send_message(jid, message)
                            click.echo(f"✅ Message sent to {phone}")
                        else:
                            click.echo("Usage: send <phone> <message>")
                    
                    elif user_input.lower() == 'status':
                        info = client.get_connection_info()
                        click.echo(f"Connected: {info['is_connected']}")
                        click.echo(f"Phone: {info['phone_number']}")
                        click.echo(f"Session: {info['session_id']}")
                    
                    elif user_input.lower() == 'groups':
                        groups = await client.get_groups()
                        if groups:
                            for i, group in enumerate(groups, 1):
                                click.echo(f"{i}. {group['name']} ({group['member_count']} members)")
                        else:
                            click.echo("No groups found.")
                    
                    else:
                        click.echo(f"❓ Unknown command: {user_input}")
                        click.echo("Type 'help' for available commands")
                
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    click.echo(f"❌ Error: {e}")
            
            await client.disconnect()
            click.echo("\n👋 Goodbye!")
            
        except Exception as e:
            click.echo(f"❌ Error: {e}", err=True)
            sys.exit(1)
    
    asyncio.run(interactive_mode())


def main():
    """Main entry point for CLI"""
    cli()


if __name__ == '__main__':
    main()