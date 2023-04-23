import plotly.graph_objects as go
from plotly.subplots import make_subplots

def graficos_plotly(ob, symbol: str):
    
    figs = []
    
    for exchange_id in ob.keys():
        fig = make_subplots(specs=[[{"secondary_y": False}]])
        
        fig.add_trace(go.Scatter(x = ob[exchange_id].index, y = ob[exchange_id]["Level"], name = exchange_id), 
                       secondary_y = False,)
        fig.update_layout(title = "Level: " + symbol,  yaxis_title = "Niveles", xaxis_title = "Fecha")
        
        fig.add_trace(go.Scatter(x = ob[exchange_id].index, y = ob[exchange_id]["Ask Volume"], name = exchange_id), 
                       secondary_y = False,)
        fig.update_layout(title = "Ask Volume: " + symbol,  yaxis_title = "Volumen", xaxis_title = "Fecha")
        
        fig.add_trace(go.Scatter(x = ob[exchange_id].index, y = ob[exchange_id]["Bid Volume"], name = exchange_id), 
                       secondary_y = False,)
        fig.update_layout(title = "Bid Volume: " + symbol,  yaxis_title = "Volumen", xaxis_title = "Fecha")
        
        fig.add_trace(go.Scatter(x = ob[exchange_id].index, y = ob[exchange_id]["Total Volume"], name = exchange_id), 
                       secondary_y = False,)
        fig.update_layout(title = "Total Volume: " + symbol,  yaxis_title = "Volumen", xaxis_title = "Fecha")
        
        fig.add_trace(go.Scatter(x = ob[exchange_id].index, y = ob[exchange_id]["Mid Price"], name = exchange_id), 
                       secondary_y = False,)
        fig.update_layout(title = "Mid Price: " + symbol,  yaxis_title = "Precio Dólares", xaxis_title = "Fecha")
        
        fig.add_trace(go.Scatter(x = ob[exchange_id].index, y = ob[exchange_id]["VWAP"], name = exchange_id), 
                       secondary_y = False,)
        fig.update_layout(title = "VWAP: " + symbol,  yaxis_title = "Precio Dólares", xaxis_title = "Fecha")
        
        figs.append(fig)
    
    return figs
