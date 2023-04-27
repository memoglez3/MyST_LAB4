import data, functions, visualizations
import pandas as pd

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

# Creación de Dataframes de análisis
series_de_tiempo_1 = functions.OB_ts(pd.read_csv("files/orderbooks1.csv"))
series_de_tiempo_2 = functions.OB_ts(pd.read_csv("files/orderbooks2.csv"))
microestructura_1 = functions.micro_modelling(series_de_tiempo_1)
microestructura_2 = functions.micro_modelling(series_de_tiempo_2)

# Visualización

facetas_sdt_1 = visualizations.timeseries_facet_plot(series_de_tiempo_1)
facetas_sdt_2 = visualizations.timeseries_facet_plot(series_de_tiempo_2)