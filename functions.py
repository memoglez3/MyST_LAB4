import ccxt, datetime, numpy as np, pandas as pd, time 

def procesar_orden_book(ob):
    
    microestructura_datos = {}
    
    for exchange_id in ob.keys():
        data_frames = []
        
        for timestamp, order_book in ob[exchange_id].items():
            asks = order_book["libro_ordenes"]["asks"]
            bids = order_book["libro_ordenes"]["bids"]
            
            level = len(asks)
            ask_size = sum(x[1] for x in asks)
            bid_size = sum(x[1] for x in bids)
            total_volume = sum(order_book.get(side, {}).get("volume", 0) for side in ("bids", "asks"))
            mid_price = (asks[0][0] + bids[0][0]) / 2
            ask_weights = np.array([x[0] * x[1] for x in asks])
            bid_weights = np.array([x[0] * x[1] for x in bids])
            vwap = (sum(ask_weights) + sum(bid_weights)) / total_volume if total_volume != 0 else np.nan
            
            data_frames.append({
                "Timestamp": timestamp,
                "Level": level,
                "Ask Size": ask_size,
                "Bid Size": bid_size,
                "Total Volume": total_volume,
                "Mid Price": mid_price,
                "VWAP": vwap
            })
        
        data_frame = pd.DataFrame(data_frames).set_index("Timestamp")
        microestructura_datos[exchange_id] = data_frame
    
    return microestructura_datos

def OB_ts(data: pd.DataFrame)->pd.DataFrame:
    """
    Esta función toma un objeto DataFrame de Pandas que contiene
      información de libros de órdenes y devuelve un nuevo objeto 
      DataFrame que contiene información resumida de los libros de órdenes.
    """
    # código de la función
    def ob_consume(ob: dict) -> list:
        levels = len(np.unique(np.concatenate((np.array(ob["ask"]), np.array(ob["bid"])))))
        ask_volume = np.sum(ob["ask_size"])
        bid_volume = np.sum(ob["bid_size"])
        total_volume = ask_volume + bid_volume
        mid_price = np.sum(np.mean(ob["ask"])+np.mean(ob["bid"]))/2
        mid_price_serie = np.array(ob["ask"]) + np.array(ob["bid"])/2
        volume_serie = np.array(np.array(ob["ask_size"])+np.array(ob["bid_size"]))
        vwap = np.sum(mid_price_serie*volume_serie)/total_volume
        spread = np.array(ob["spread"]).mean()
        return [levels,bid_volume,ask_volume,total_volume,mid_price,vwap,spread]
    
    ts_df = pd.DataFrame(columns=["exchange","timeStamp","level","Ask_Volume",
                                  "Bid_Volume","Total_Volume","Mid_Price","VWAP","Spread"])
    ts_df["exchange"] = data["exchange"]
    ts_df["timeStamp"] = data["datetime"]
    for i in range(len(ts_df)):
        ob = ast.literal_eval(data["orderbook"][i])
        ob_list = ob_consume(ob)
        ts_df["level"][i] = ob_list[0]
        ts_df["Ask_Volume"][i] = ob_list[1]
        ts_df["Bid_Volume"][i] = ob_list[2]
        ts_df["Total_Volume"][i] = ob_list[3]
        ts_df["Mid_Price"][i] = ob_list[4]
        ts_df["VWAP"][i] = ob_list[5]
        ts_df["Spread"][i] = ob_list[6]
    return ts_df

def micro_modelling(data: pd.DataFrame) -> pd.DataFrame:
    """
    Esta función toma un DataFrame de microestructura de un libro de órdenes
    (order book) y calcula el spread efectivo en función del precio medio y la
    ventana de tiempo especificada.
    """
    order_book = data.reset_index()
    last_timestamp = order_book.loc[:, "timeStamp"].values[-1]
    lagged_timestamp = pd.to_datetime(last_timestamp) - datetime.timedelta(seconds=60)
    lagged_index = sum(pd.to_datetime(order_book["timeStamp"]) <= lagged_timestamp)
    window = len(order_book) - lagged_index
    
    mid_prices = order_book.loc[:, "Mid_Price"].astype(float)
    effective_spreads = []
    
    for i in range(len(mid_prices) - (window * 2)):
        covariance = np.cov(mid_prices[i:window + i], mid_prices[window + i:window * 2 + i])[0][1]
        effective_spreads.append(np.abs(covariance) ** 0.5)
    
    order_book = order_book.iloc[len(order_book) - len(effective_spreads):, :]
    order_book["Effective Spread"] = effective_spreads
    order_book = order_book[["timeStamp", "Mid_Price", "Spread", "Effective Spread"]]
    order_book.rename(columns={"Mid_Price": "Close"}, inplace=True)
    order_book.set_index("timeStamp", inplace=True)
    
    return order_book