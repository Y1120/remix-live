import asyncio
import ccxt.async_support as ccxt

Exchanges_id = ["binance", "bybit", "hyperliquid", "bitget", "gate", "okx"]

async def get_all_symbols(exchange_ccxt_instance):
    market = await exchange_ccxt_instance.load_markets()
    # only get symbols that is swap/perp contract
    symbols = []
    for symbol, info in market.items():
        print(symbol)
        print(info)
        if symbol.endswith('/USDT') and info['type'] == 'spot':
            symbols.append(symbol)
    return symbols

async def cctx_index_price(exchange, symbol):
    try:
        ticker = await exchange.fetch_ticker(symbol)
        print("start getting {} index price".format(str(exchange)))
        timestamp = ticker["datetime"]
        index_price = ticker['indexPrice']
        print("timestamp: {}, index price: {}".format(timestamp, index_price))
        await exchange.close()
        return timestamp, index_price
        
    finally:
        await exchange.close()

# async def cctx_prices(symbols):
#     binance = ccxt.binanceusdm()
#     bybit = ccxt.bybit()
#     hyperliquid = ccxt.hyperliquid()
#     bitget = ccxt.bitget()
#     gate = ccxt.gate()
#     okx = ccxt.okx()

#     try:
#         while True:
#             ticker_binance = await binance.fetch_ticker(symbols)
#             ticker_bybit = await bybit.fetch_ticker(symbols)
#             ticker_gate = await gate.fetch_ticker(symbols)
#             ticker_bitget = await bitget.fetch_ticker(symbols)
#             ticker_okx = await okx.fetch_ticker(symbols)
#             ticker_hyperliquid = await hyperliquid.fetch_ticker(symbols)
            
#             print(ticker_binance)
#             timestamp = ticker_binance["datetime"]
            
#             binance_index_price = ticker_binance['last']
#             bybit_index_price = ticker_bybit['last']
#             gate_index_price = ticker_gate['last']
#             bitget_index_price = ticker_bitget['last']
#             okx_index_price = ticker_okx['last']
#             hyperliquid_index_price = ticker_hyperliquid['last']
#     finally:
#         await binance.close()
#         await bybit.close()
#         await hyperliquid.close()
#         await bitget.close()
#         await gate.close()
#         await okx.close()

async def main():
    binance = ccxt.binance()
    symbols_binance = await get_all_symbols(binance)
    print("symbols_binance",symbols_binance)
    # bybit = ccxt.bybit()
    # symbols_bybit = await get_all_symbols(bybit)
    # hyperliquid = ccxt.hyperliquid()
    # symbols_hyperliquid = await get_all_symbols(hyperliquid)
    # bitget = ccxt.bitget()
    # symbols_bitget = await get_all_symbols(bitget)
    # gate = ccxt.gate()
    # symbols_gate = await get_all_symbols(gate)
    # okx = ccxt.okx()
    # symbols_okx = await get_all_symbols(okx)
    # exchange_list = [binance, bybit, hyperliquid, bitget, gate, okx]
    exchange_list = [binance]

    for exchange in exchange_list:
        # symbols = symbols_binance if str(exchange) == "binance" else symbols_bybit if str(exchange) == "bybit" else symbols_hyperliquid if str(exchange) == "hyperliquid" else symbols_bitget if str(exchange) == "bitget" else symbols_gate if str(exchange) == "gate" else symbols_okx
        symbols = symbols_binance
        for symbol in symbols:
            await cctx_index_price(exchange, symbol)
            await asyncio.sleep(1)
            await exchange.close()


if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())