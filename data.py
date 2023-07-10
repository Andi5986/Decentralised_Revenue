import pandas as pd
import numpy as np
from datetime import timedelta, date
import requests
import math

def fetch_ether_to_usd(size):
    url = "https://api.coingecko.com/api/v3/coins/ethereum/market_chart"
    params = {"vs_currency": "usd", "days": size}  
    response = requests.get(url, params=params)
    data = response.json()

    df = pd.DataFrame(data['prices'], columns=['time', 'price'])
    df['time'] = pd.to_datetime(df['time'], unit='ms')

    return df['price']

def logistic(x, x0, k, L):
    """
    The logistic function. 
    Parameters:
    - x: the input
    - x0: the midpoint of the transition,
    - k: the steepness of the transition
    - L: the maximum value
    """
    return L / (1 + np.exp(-k * (x - x0)))

def generate_data(start_date, end_date):
    d1 = date.fromisoformat(start_date)  
    d2 = date.fromisoformat(end_date)  
    
    delta = d2 - d1         
    days = delta.days + 1

    date_range = pd.date_range(start=start_date, end=end_date)
    x = np.arange(days)
    
    df = pd.DataFrame(date_range, columns=['date'])

    # Logistic growth for tasks and users with cyclic behaviour
    df['Total Tasks'] = (1 + 0.5 * np.sin(2 * math.pi * x / 365) + 0.3 * np.sin(2 * math.pi * x / 120)) * logistic(x, days / 3, 0.1, 10000000) + np.random.normal(0, 1000, days)
    df['Users'] = (1 + 0.4 * np.sin(2 * math.pi * x / 320) + 0.3 * np.sin(2 * math.pi * x / 180)) * logistic(x, days / 2, 0.1, 100000) + np.random.normal(0, 50, days)

    # Ensuring tasks and users are non-negative and integer
    df[['Total Tasks', 'Users']] = df[['Total Tasks', 'Users']].clip(lower=0).astype(int)

    df['New Tasks'] = df['Total Tasks'].diff().fillna(df['Total Tasks']).clip(lower=0)
    df['Solved Tasks'] = (df['New Tasks'] * np.random.uniform(0, 1, size=(days,))).astype(int).clip(lower=0)
    df['Active Users'] = (df['Users'] * np.random.uniform(0.1, 1, size=(days,))).astype(int)
    df['Ether to USD'] = fetch_ether_to_usd(days)
    
    return df

if __name__ == "__main__":
    df = generate_data('2020-01-01', '2022-12-31')
    df.to_csv('random_data.csv', index=False)
