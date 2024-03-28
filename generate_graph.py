import requests
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta

# Define the API endpoint
endpoint = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"

# Calculate the start and end timestamps for the past 24 hours
end_time = int(datetime.now().timestamp())
start_time = int((datetime.now() - timedelta(days=1)).timestamp())

# Define the query parameters
params = {
    "vs_currency": "gbp",
    "from": start_time,
    "to": end_time,
    "days": 1,
}

# Make the API request
response = requests.get(endpoint, params=params)
data = response.json()

# Extract the timestamp and prices from the response if 'prices' key exists
if 'prices' in data:
    timestamps = [datetime.fromtimestamp(entry[0] / 1000).strftime('%Y-%m-%d %H:%M:%S') for entry in data['prices']]
    prices = [entry[1] for entry in data['prices']]

    # Save data to CSV file with filename containing the dates
    filename = f'bitcoin_prices_{datetime.now().strftime("%Y-%m-%d")}.csv'
    df = pd.DataFrame({"Timestamp": timestamps, "Price": prices})
    
    # Format timestamp if it's not already datetime-like
    if not pd.api.types.is_datetime64_any_dtype(df['Timestamp']):
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    
    df['Timestamp'] = df['Timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')  # Format timestamp
    df['Price_from'] = df['Price'].shift(1)  # Add previous price as 'Price_from'
    df['Price_to'] = df['Price']  # Add current price as 'Price_to'
    df.to_csv(filename, index=False)

    # Ensure 'Timestamp' column is in datetime format
    if not pd.api.types.is_datetime64_any_dtype(df['Timestamp']):
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    
    # Plot the data
    plt.figure(figsize=(10, 6))
    plt.plot(df['Timestamp'], df['Price'], marker='o', linestyle='-')
    
    # Formatting
    plt.title('Bitcoin Price in GBP in the Last 24 Hours')
    plt.xlabel('Time')
    plt.ylabel('Price (GBP)')
    plt.grid(True)
    
    # Set ticks for every hour
#    tick_positions = df['Timestamp'].dt.strftime('%Y-%m-%d 00:00')
    
#    plt.xticks(tick_positions, rotation=45)
    
    # Save plot as image
    plt.tight_layout()
    plt.savefig('bitcoin_price.png')

else:
    print("No price data available for the past 24 hours.")
