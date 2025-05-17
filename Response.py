import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from Knowledge_base import knowledge_base
from typing import Final
from API import Alpha
from Commands import handle_math_commands , calculate_expression

load_dotenv()

def get_response(user_message: str, username: str, alpha_key: str = None) -> str:
    user_message = user_message.strip().lower()
    log_message(username, user_message)

    # 1. Stock command
    if user_message.startswith("/stock"):
        parts = user_message.split()
        if len(parts) != 4:
            return "⚠️ Usage: `/stock tradeview USD INR` (replace USD and INR with valid currency codes)."

        api_name = parts[1].lower()
        from_currency = parts[2].upper()
        to_currency = parts[3].upper()

        if api_name == "tradeview":
            return Alpha(FROM=from_currency, TO=to_currency, API_KEY=alpha_key)
        else:
            return "⚠️ Invalid API name. Supported API: `tradeview`."

    # 2. Music play command
    if user_message.startswith("//play"):
        parts = user_message.split()
        if len(parts) == 2 and parts[1].startswith("http"):
            return f"🎵 Loading and playing: {parts[1]}"
        else:
            return "🎵 Usage: `//play <YouTube URL>`"

    # 3. Math commands (e.g., /add 5 3)
    math_result = handle_math_commands(user_message)
    if math_result:
        return math_result

    # 4. Knowledge base lookup
    for key in knowledge_base:
        if key.lower() in user_message:
            return knowledge_base[key]

    # 5. Fallback
    return "🤖 Sorry, I don't understand that. Try `/stock tradeview USD EUR` to get a currency exchange rate."

def log_message(username: str, user_message: str) -> None:
    """Append user messages to a log file with timestamps."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("user_messages.log", "a", encoding="utf-8") as log_file:
        log_file.write(f"[{timestamp}] {username}: {user_message}\n")
