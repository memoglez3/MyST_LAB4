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