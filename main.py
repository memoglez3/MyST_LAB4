import data, functions, visualizations

def descarga(exchange_id, run_time: int, symbol: str):
    """
    La función "descarga" nos devuelve el libro de órdenes para la cripto escogida
    """
    
    ob = data.async_client(exchange_id, run_time, symbol)
    
    return ob