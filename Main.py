from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from Response import get_response

load_dotenv()
TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")
print(TOKEN)

intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)

# List of allowed channel IDs where the bot is allowed to respond
ALLOWED_CHANNELS = [123456789012345678, 987654321098765432]  # Replace with actual channel IDs

async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print("Message was empty because Intents were not enabled properly")
        return
    
    is_private = user_message[0] == '?'
    if is_private:
        user_message = user_message[1:]

    try:
        response: str = get_response(user_message)
        if is_private:
            await message.author.send(response)
        else:
            await message.channel.send(response)
    except Exception as e:
        print(e)

@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running')

@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    # Check if the message is from a DM or a server
    if message.guild is None:
        # Handle DM
        print(f"Received message in DM from {message.author}: {message.content}")
        await send_message(message=message, user_message=message.content)
    else:
        # Handle server messages
        if message.channel.id not in ALLOWED_CHANNELS:
            print(f"Ignored message from unauthorized channel: {message.channel}")
            return

        username: str = str(message.author)
        user_message: str = str(message.content)
        channel: str = str(message.channel)

        print(f"[{channel}] :: {username}: {user_message}")
        await send_message(message=message, user_message=user_message)

def main() -> None:
    client.run(TOKEN)

if __name__ == '__main__':
    main()