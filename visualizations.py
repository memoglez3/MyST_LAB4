import plotly.graph_objects as go
import plotly.subplots as sp
import pandas as pd

def timeseries_facet_plot(df: pd.DataFrame):
    # Agrupar por exchange
    exchange_groups = df.groupby("exchange")

    # Crear una subfigura para cada columna de interés
    fig = sp.make_subplots(rows=2, cols=3, subplot_titles=("Ask_Volume", "Bid_Volume", "Total_Volume", "Mid_Price", "VWAP", "Spread"))

    # Tracer las series de tiempo de cada columna de interés en una subfigura separada para cada exchange
    for col_idx, col_name in enumerate(["Ask_Volume", "Bid_Volume", "Total_Volume", "Mid_Price", "VWAP", "Spread"]):
        row_idx = col_idx // 3 + 1
        col_idx = col_idx % 3 + 1
        
        for exchange, group in exchange_groups:
            fig.add_trace(go.Scatter(x=group["timeStamp"], y=group[col_name], name=exchange), row=row_idx, col=col_idx)

    # Configurar el diseño de la figura y mostrarla
    fig.update_layout(height=800, width=1000, title="Series de Tiempo por Exchange")
    return fig
