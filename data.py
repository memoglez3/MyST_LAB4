import ccxt, asyncio, datetime, numpy as np, pandas as pd, time 
import ccxt.async_support as ccxta

async def async_client(exchange_id, run_time: int, symbol: str):
    orderbook = None
    exchange = getattr(ccxta, exchange_id)()
    time_1 = time.time()
    time_f = 0
    ob = []
    while time_f <= run_time:
        try:
            await exchange.load_markets()
            market = exchange.market(symbol)
            orderbook = await exchange.fetch_order_book(market["symbol"])
            datetime = exchange.iso8601(exchange.milliseconds())
            # Unpack values
            ask_price, ask_size = np.array(list(zip(*orderbook["asks"]))[0:2])
            bid_price, bid_size = np.array(list(zip(*orderbook["bids"]))[0:2])
            spread = np.round(ask_price - bid_price, 4)
            # Final data format for the results
            ob.append(
                {
                    "exchange": exchange_id,
                    "datetime": datetime,
                    "orderbook": {
                        "ask_size": ask_size.tolist(),
                        "ask": ask_price.tolist(),
                        "bid": bid_price.tolist(),
                        "bid_size": bid_size.tolist(),
                        "spread": spread.tolist(),
                    },
                }
            )
            # End time
            time_2 = time.time()
            time_f = round(time_2 - time_1, 4)
        except Exception as e:
            time_2 = time.time()
            time_f = round(time_2 - time_1, 4)
            print(type(e).__name__, str(e))
    await exchange.close()
    return ob
    
async def multi_orderbooks(exchanges, run_time: int, symbol: str):
    input_coroutines = [
        async_client(exchange, run_time, symbol) for exchange in exchanges
    ]   
    orderbooks = await asyncio.gather(*input_coroutines, return_exceptions=True)
    return orderbooks

# if __name__ == "__main__":
#     exchanges = ["kucoin", "bittrex", "bitfinex", "poloniex", "huobipro"]
#     run_time = 10  # seconds
#     symbol = "ETH/BTC"

#     data = asyncio.run(multi_orderbooks(exchanges, run_time=run_time, symbol=symbol))
#     data = [item for sublist in data for item in sublist]
#     data = pd.DataFrame(data)

#     print(data.head())
