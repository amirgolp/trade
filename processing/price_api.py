import requests


def get_polygon_5min_prices(symbol, api_key):
    url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/5/minute/2023-01-01/2023-12-31?apiKey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        prices = data["results"]
        return prices
    else:
        return "Error fetching data"


# Example usage
symbol = "AAPL"  # Stock symbol
api_key = "oRDqJtpUBPFqpg5WVuRuhu3CZkbPEZ3R"  # Replace with your Polygon API key

prices = get_polygon_5min_prices(symbol, api_key)
if prices != "Error fetching data":
    for price in prices:
        print(price)
else:
    print("Error fetching prices")
