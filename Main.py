from typing import Final
import os
import discord
from dotenv import load_dotenv
from discord import Intents, Client, Message, FFmpegPCMAudio, VoiceClient
from Response import get_response
import yt_dlp as youtube_dl

load_dotenv()
TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")
print(TOKEN)

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'noplaylist': True,
    'quiet': True,
}

ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'  # No video, audio only
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options) 

# Dictionary to keep track of voice clients per guild
VOICE_CLIENTS = {}

intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)

# List of allowed channel IDs where the bot is allowed to respond
ALLOWED_CHANNELS = [123456789012345678, 987654321098765432, 1296687168634224711]  # Replace with actual channel IDs

async def send_message(message: Message, user_message: str , username: str) -> None:
    if not user_message:
        print("Message was empty because Intents were not enabled properly")
        return
    
    is_private = user_message[0] == '?'
    if is_private:
        user_message = user_message[1:]

    try:
        response: str = get_response(user_message,username=username)
        if is_private:
            await message.author.send(response)
        else:
            await message.channel.send(response)
    except Exception as e:
        print(e)

@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running')

async def play_audio(ctx: Message, url: str) -> None:
    voice_channel = ctx.author.voice.channel

    if not voice_channel:
        await ctx.channel.send("You need to be in a voice channel to play audio.")
        return
    
    # Check if already connected to a voice channel
    if ctx.guild.id in VOICE_CLIENTS and VOICE_CLIENTS[ctx.guild.id].is_connected():
        voice_client = VOICE_CLIENTS[ctx.guild.id]
    else:
        # Connect to the voice channel
        voice_client: VoiceClient = await voice_channel.connect()
        VOICE_CLIENTS[ctx.guild.id] = voice_client

    # Use youtube_dl to extract audio info
    try:
        # Extract audio info from the provided URL
        info = ytdl.extract_info(url, download=False)

        # Extract the audio URL from the available formats
        audio_url = info['url'] if 'url' in info else info['formats'][0]['url']

        # Play the audio
        source = FFmpegPCMAudio(audio_url, **ffmpeg_options)
        if not voice_client.is_playing():
            voice_client.play(source)
            await ctx.channel.send(f"Now playing: {info['title']}")
        else:
            await ctx.channel.send("Already playing audio. Use //stop to stop the current audio.")
    except Exception as e:
        await ctx.channel.send(f"An error occurred: {e}")
        print(e)

@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    # Check if the message is from a DM or a server
    if message.guild is None:
        # Handle DM
        print(f"Received message in DM from {message.author}: {message.content}")
        await send_message(message=message, user_message=message.content, username=str(message.author))
    else:
        # Handle server messages
        if message.channel.id not in ALLOWED_CHANNELS:
            print(f"Ignored message from unauthorized channel: {message.channel}")
            return

        username: str = str(message.author)
        user_message: str = str(message.content)
        channel: str = str(message.channel)

        print(f"[{channel}] :: {username}: {user_message}")

        if user_message.startswith('//play '):
            url = user_message[len('//play '):]
            await play_audio(message, url)
        elif user_message.startswith('//stop'):
            voice_client = discord.utils.get(client.voice_clients, guild=message.guild)
            if voice_client and voice_client.is_playing():
                voice_client.stop()
                await message.channel.send("Stopped playing the audio.")
            else:
                await message.channel.send("No audio is currently playing.")

        # Send response for other messages
        await send_message(message=message, user_message=user_message, username=username)  # Correctly passing username

def main() -> None:
    client.run(TOKEN)

if __name__ == '__main__':
    main()
