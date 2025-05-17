import os
from typing import Final
import discord
from discord import Intents, Client, Message, FFmpegPCMAudio, VoiceClient
from dotenv import load_dotenv
import yt_dlp as youtube_dl

from Response import get_response  # Your response logic
# Note: Make sure Response.py is in the same directory or accessible

# Load environment variables
load_dotenv()
TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")
ALPHA_API_KEY: Final[str] = os.getenv("ALPHA_VANTAGE_API_KEY")

print(f"Bot Token Loaded: {'Yes' if TOKEN else 'No'}")
print(f"Alpha Vantage Key Loaded: {'Yes' if ALPHA_API_KEY else 'No'}")

# Set up yt-dlp and FFmpeg options for audio streaming
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'noplaylist': True,
    'quiet': True,
}
ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

# Allowed text channels where the bot can respond to commands
ALLOWED_CHANNELS = [1297097286710595615,1372825892111519825]  # Replace with real IDs

# Store voice clients per guild
VOICE_CLIENTS = {}

# Initialize Discord client with intents
intents = Intents.default()
intents.message_content = True
client = Client(intents=intents)


async def send_message(message: Message, user_message: str, username: str) -> None:
    """Process a user message and send back the bot response."""
    if not user_message:
        print("Empty message (likely due to missing intents)")
        return

    is_private = user_message.startswith('?')
    if is_private:
        user_message = user_message[1:]

    try:
        response: str = get_response(user_message, username=username, alpha_key=ALPHA_API_KEY)
        if is_private:
            await message.author.send(response)
        else:
            await message.channel.send(response)
    except Exception as e:
        print(f"Error while sending message: {e}")


@client.event
async def on_ready() -> None:
    print(f"{client.user} is now running!")


async def play_audio(ctx: Message, url: str) -> None:
    """Join the user's voice channel and play audio from a YouTube URL."""
    try:
        if not ctx.author.voice:
            await ctx.channel.send("🔇 You must be in a voice channel to use this command.")
            return

        voice_channel = ctx.author.voice.channel

        voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)
        if not voice_client or not voice_client.is_connected():
            voice_client: VoiceClient = await voice_channel.connect()
            VOICE_CLIENTS[ctx.guild.id] = voice_client
        else:
            if voice_client.channel != voice_channel:
                await ctx.channel.send("🔁 Bot is already connected to another channel.")
                return

        # Extract audio info and URL without downloading
        info = ytdl.extract_info(url, download=False)
        audio_url = info.get('url') or info['formats'][0]['url']
        print(f"Playing audio URL: {audio_url}")  # Debug output

        source = FFmpegPCMAudio(
            audio_url,
            before_options=ffmpeg_options['before_options'],
            options=ffmpeg_options['options']
        )

        # Stop any current playing audio
        if voice_client.is_playing():
            voice_client.stop()

        voice_client.play(source)
        await ctx.channel.send(f"🎶 Now playing: **{info.get('title', 'Unknown')}**")

    except Exception as e:
        await ctx.channel.send(f"❌ Error playing audio: {str(e)}")
        print(f"Error in play_audio: {e}")

@client.event
async def on_message(message: Message) -> None:
    # Ignore messages from the bot itself
    if message.author == client.user:
        return

    # Handle messages sent in DMs (no guild)
    if message.guild is None:
        # Only allow non-voice commands in DMs
        await send_message(message, message.content, str(message.author))
        return

    # Only respond to messages in allowed channels on servers
    if message.channel.id not in ALLOWED_CHANNELS:
        print(f"Ignored message from unauthorized channel: {message.channel}")
        return

    username = str(message.author)
    user_message = message.content.strip()
    lower_msg = user_message.lower()

    print(f"[{message.channel}] {username}: {user_message}")

    # Music commands
    if lower_msg.startswith('//play'):
        parts = user_message.split(maxsplit=1)
        if len(parts) < 2:
            await message.channel.send("❗ Please provide a YouTube link. Usage: `//play <YouTube URL>`")
            return

        # Check if author is in a voice channel in the server
        if not message.author.voice or not message.author.voice.channel:
            await message.channel.send("🔇 You must be in a voice channel to use this command.")
            return

        await play_audio(message, parts[1])
        return

    if lower_msg.startswith('//stop'):
        vc = discord.utils.get(client.voice_clients, guild=message.guild)
        if vc and vc.is_playing():
            vc.stop()
            await message.channel.send("⏹️ Stopped audio.")
        else:
            await message.channel.send("❌ Nothing is playing.")
        return

    # Fallback to default response for other messages
    await send_message(message, user_message, username)


def main() -> None:
    if TOKEN:
        client.run(TOKEN)
    else:
        print("DISCORD_TOKEN not found in environment.")


if __name__ == "__main__":
    main()
