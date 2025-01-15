import sqlite3
import asyncio
import os
import sys
import pandas as pd
import ccxt.async_support as ccxt  # noqa: E402
import datetime
import time
import numpy as np 
import pyodbc

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root + '/python')
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Database connection details
server = 'theosql.database.windows.net'
database = 'arbitrage_db_2024-03-22T23-30Z'
username = 'THEOsql'
password = 'THEOBullRun2024!'

Exchanges = ["Binance", "Bybit", "Hyperliquid", "Bitget", "Gate", "OKX"]
Exchanges_id = ["binance", "bybit", "hyperliquid", "bitget", "gate", "okx"]

# Establish a connection to the database
def connect_to_db():
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    conn = pyodbc.connect(connection_string)
    return conn

# Create the exchange_index table
def create_table():
    conn = connect_to_db()
    cursor = conn.cursor()
    # Check if the table exists
    cursor.execute('''
        IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'exchange_index')
        BEGIN
            CREATE TABLE exchange_index (
                timestamp DATETIME,
                binance_index_price FLOAT,
                bybit_index_price FLOAT,
                hyperliquid_index_price FLOAT,
                bitget_index_price FLOAT,
                gate_index_price FLOAT,
                okx_index_price FLOAT,
            )
        END
    ''')
    conn.commit()
    conn.close()

# Insert data into the exchange_index table
def insert_data(data):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.executemany('''
        INSERT INTO exchange_index (timestamp, open, high, low, close, volume)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', data)
    conn.commit()
    conn.close()

async def get_all_symbols(exchange_ccxt_instance):
    market = await exchange_ccxt_instance.load_markets()
    # only get symbols that is swap/perp contract
    symbols = []
    for symbol, info in market.items():
        if symbol.endswith('/USDT:USDT') and info['type'] = 'swap':
            symbols.append(symbol)
    return symbols

async def get_index () :
    print("start getting data")

    temp_df = pd.DataFrame({"timestamp":[],"open":[],"high":[],"low":[],"close":[]})
    exchange = ccxt.binanceusdm ()

    index_price = None
    name = None

    indexKlines = await exchange.fetchOHLCV ('ADA/USDT', '5m', index_price, name, { 'price': 'index' })
    print (indexKlines)
    # for data in indexKlines:
    #     temp_df["timestamp"] = data[0];
    #     temp_df["open"] = data[1];
    #     temp_df["high"] = data[2];
    #     temp_df["low"] = data[3];
    #     temp_df["close"] = data[4];

    #["timestamp","open","high","low","close","volume"]
    return temp_df



if __name__ == "__main__":
    create_table()
    data = asyncio.run(get_index())
    # insert_data(data)
    # print("data inserted successfully")



