import data, functions, visualizations

def descarga(exchange_id, run_time: int, symbol: str):
    """
    La función "descarga" nos devuelve el libro de órdenes para la cripto escogida
    """
    
    ob = data.async_client(exchange_id, run_time, symbol)
    
    return ob

def microestructura_v(ob, symbol: int):
    """
    La función "microestructura_v" manda llamar los gráficos que se generaron después de obtener los datos en functions
    """
    microestructura_datos = functions.procesar_orden_book(ob)
    figs = visualizations.graficos_plotly(microestructura_datos, symbol)
    
    return microestructura_datos, figs