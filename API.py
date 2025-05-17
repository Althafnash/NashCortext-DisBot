import requests

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
