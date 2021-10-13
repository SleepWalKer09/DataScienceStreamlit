import yfinance as yf
import streamlit as st
import pandas as pd

st.write("""
#Simple stock Price App

Datos de la ex API de **Yahoo! Finance**, usando la libreria "yfinance"

Se muestran los stock "closing price" y "volume"  de google 
""")

#define the ticker symbol
tickerSymbol = 'GOOGL'
#get data on this ticker
tickerData =  yf.Ticker(tickerSymbol)
#get the historical prices for this ticket
ticketDf = tickerData.history(period = '1d', start = '2010-5-31', end = '2020-5-31')

#datos que se mostraran en graficas
st.line_chart(ticketDf.Close)
st.line_chart(ticketDf.Volume)