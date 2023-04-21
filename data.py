import ccxt, datetime, numpy as np, pandas as pd, time 

def criptoactiva(ticker):
    
    def criptoex_ccxt(criptoex):
        
        if criptoex == "coinmate":
            cripto = ccxt.coinmate()
        
        elif criptoex == "ftx":
            cripto = ccxt.ftx()
        
        else:
            cripto = ccxt.cex()
        
        return cripto