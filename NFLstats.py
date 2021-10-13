import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.title('Estadisticas de jugadores de la NFL')

st.markdown("""
Esta app hace **webscraping** a las estadisticas de jugadores de la NFL.

* **Contexto: **Se enfoca en las jugadas llamadas "rushing" las cuales consisten en una acción tomada por el equipo a la defensiva 
                eso significa que para cargar hacia el mariscal de campo o pateador a través de la línea de golpeo. 
                El propósito es el tackleo, derribar al mariscal de campo, o el bloqueo o la interrupción de un pase o una patada.

* **Dataset: ** https://www.pro-football-reference.com/years/
""")

st.sidebar.header('Filtros')
selected_year = st.sidebar.selectbox('Año', list(reversed(range(1990,2021))))

# Web scraping a registros de la NFL
@st.cache
def load_data(year):
    url = "https://www.pro-football-reference.com/years/" + str(year) + "/rushing.htm"
    html = pd.read_html(url, header = 1)
    df = html[0]
    raw = df.drop(df[df.Age == 'Age'].index) # Deletes repeating headers in content
    raw = raw.fillna(0)
    playerstats = raw.drop(['Rk'], axis=1)
    return playerstats
playerstats = load_data(selected_year)

# Sidebar - Seleccion de equipo
sorted_unique_team = sorted(playerstats.Tm.unique())
selected_team = st.sidebar.multiselect('Equipo', sorted_unique_team, sorted_unique_team)

# Sidebar - Seleccion de posicion 
unique_pos = ['RB','QB','WR','FB','TE']
selected_pos = st.sidebar.multiselect('Posicion', unique_pos, unique_pos)

# Filtra Datos
df_selected_team = playerstats[(playerstats.Tm.isin(selected_team)) & (playerstats.Pos.isin(selected_pos))]

st.header('Desplegar estadisticas de los equipos seleccionados')
st.write('Dimension de datos: ' + str(df_selected_team.shape[0]) + ' filas y ' + str(df_selected_team.shape[1]) + ' columnas.')
st.dataframe(df_selected_team)

# Descargar los datos en forma de archivos CSV

def descarga_csv(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href

st.markdown(descarga_csv(df_selected_team), unsafe_allow_html=True)

# Mapa de calor 
if st.button('Mapa de calor de correlaciones'):
    st.header('Matriz del mapa de calor de correlaciones')
    df_selected_team.to_csv('output.csv',index=False)
    df = pd.read_csv('output.csv')

    corr = df.corr()
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True
    with sns.axes_style("white"):
        f, ax = plt.subplots(figsize=(7, 5))
        ax = sns.heatmap(corr, mask=mask, vmax=1, square=True)
    st.pyplot(f)