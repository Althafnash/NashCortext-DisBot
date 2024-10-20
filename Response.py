import random 
from Knowledge_base import knowledge_base
from datetime import datetime
from dotenv import load_dotenv
import os
import requests

load_dotenv()

def Alpha(FROM: str, TO: str):
    print("Alpha function working")
    Alpha_API = os.getenv("ALPHA_API")

    url = f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={FROM}&to_currency={TO}&apikey={Alpha_API}'
    r = requests.get(url)

    # Check for successful response
    if r.status_code != 200:
        return f"Failed to retrieve data: {r.status_code}"

    data = r.json()

    # Check if the expected data is available in the response
    if "Realtime Currency Exchange Rate" in data:
        rate_info = data["Realtime Currency Exchange Rate"]
        from_currency_name = rate_info["2. From_Currency Name"]
        to_currency_name = rate_info["4. To_Currency Name"]
        exchange_rate = rate_info["5. Exchange Rate"]

        return f"The exchange rate from {from_currency_name} to {to_currency_name} is {exchange_rate}."
    else:
        return "Failed to retrieve currency exchange rate."
    
    data = r.json()
    
    # Checking if the response contains the expected data
    if "Realtime Currency Exchange Rate" in data:
        exchange_rate = data["Realtime Currency Exchange Rate"]["5. Exchange Rate"]
        return f"The exchange rate from {FROM} to {TO} is {exchange_rate}."
    else:
        return "Could not find the exchange rate. Please check the currency codes and try again."
def get_response(user_message: str, username: str) -> str:
    user_message = user_message.lower()
    log_message(username, user_message)

    if "/stock" in user_message:
        user_message_parts = user_message.split()

        if len(user_message_parts) != 4:
            return "Usage: /stock {API Name} {FROM currency} {TO currency}"

        stock_API = user_message_parts[1].lower()
        from_currency = user_message_parts[2].upper()
        to_currency = user_message_parts[3].upper()

        print(f"API Name: {stock_API}")
        print(f"From Currency: {from_currency}")
        print(f"To Currency: {to_currency}")

        if stock_API == "tradeview":
            return Alpha(FROM=from_currency, TO=to_currency)
        else:
            return "Invalid API name. Currently supported: TradeView."

    else:
        return "Sorry, I don't understand that. Can you try asking something else? 🤔"

def log_message(username: str, user_message: str):
    with open("user_messages.log", "a") as log_file:
        log_file.write(f"{username}: {user_message}\n")
