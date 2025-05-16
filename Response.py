import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def Alpha(FROM: str, TO: str, API_KEY: str) -> str:
    """Fetch currency exchange rate from Alpha Vantage API."""
    if not API_KEY:
        return "⚠️ Alpha Vantage API key is missing."

    url = (
        f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE"
        f"&from_currency={FROM}&to_currency={TO}&apikey={API_KEY}"
    )

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if "Realtime Currency Exchange Rate" in data:
            rate_info = data["Realtime Currency Exchange Rate"]
            from_currency_name = rate_info.get("2. From_Currency Name", FROM)
            to_currency_name = rate_info.get("4. To_Currency Name", TO)
            exchange_rate = rate_info.get("5. Exchange Rate", "N/A")

            return (
                f"💱 Exchange rate from {from_currency_name} to {to_currency_name} "
                f"is {exchange_rate}."
            )
        else:
            return "⚠️ Could not retrieve currency exchange data. Please check your input or try again later."

    except requests.RequestException as e:
        return f"❌ Network error occurred: {e}"


def get_response(user_message: str, username: str, alpha_key: str = None) -> str:
    """Process user messages and return appropriate responses."""

    user_message = user_message.strip().lower()
    log_message(username, user_message)

    if user_message.startswith("/stock"):
        parts = user_message.split()

        # Expecting format: /stock tradeview USD INR
        if len(parts) != 4:
            return "⚠️ Usage: `/stock tradeview USD INR` (replace USD and INR with valid currency codes)."

        api_name = parts[1].lower()
        from_currency = parts[2].upper()
        to_currency = parts[3].upper()

        if api_name == "tradeview":
            return Alpha(FROM=from_currency, TO=to_currency, API_KEY=alpha_key)
        else:
            return "⚠️ Invalid API name. Supported API: `tradeview`."

    elif user_message.startswith("//play"):
        parts = user_message.split()
        if len(parts) == 2 and parts[1].startswith("http"):
            return f"🎵 Loading and playing: {parts[1]}"
        else:
            return "🎵 Usage: `//play <YouTube URL>`"

    # Default fallback
    return "🤖 Sorry, I don't understand that. Try `/stock tradeview USD EUR` to get a currency exchange rate."


def log_message(username: str, user_message: str) -> None:
    """Append user messages to a log file with timestamps."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("user_messages.log", "a", encoding="utf-8") as log_file:
        log_file.write(f"[{timestamp}] {username}: {user_message}\n")
