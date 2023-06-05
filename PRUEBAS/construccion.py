# -*- coding: utf-8 -*-
"""
Created on Fri May 12 16:29:04 2023

@author: Aura
"""

# Cargar datos
import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.express as px
import plotly.graph_objects as go
import base64


# Utilizar la página completa en lugar de una columna central estrecha
st.set_page_config(layout="wide")

# Título principal, h1 denota el estilo del título 1
st.markdown("<h1 style='text-align: center; color: #951F0F;'>Histórico de disparos en Nueva York 🗽💥🔫 </h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: #CCCCCC;'>Histórico de disparos en Nueva York 🗽💥🔫 </h2>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #666666;'>Histórico de disparos en Nueva York 🗽💥🔫 </h3>", unsafe_allow_html=True)


st.write('Hola Mundo')

st.write('''Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum''')

df0 = pd.read_csv('historico.csv') # base historico
df0 = df0.drop('STATISTICAL_MURDER_FLAG', axis = 1)
df1 = pd.read_csv('actual.csv') # base actual
df1 = df1.drop('STATISTICAL_MURDER_FLAG', axis = 1)
df = pd.concat([df0, df1]) # concatenar las bases

df['OCCUR_DATE'] = pd.to_datetime(df['OCCUR_DATE']) # convertir fecha a formato fecha
df['OCCUR_TIME'] = pd.to_datetime(df['OCCUR_TIME'], format='%H:%M:%S') # convertir hora a formato fecha
df['YEAR'] = df['OCCUR_DATE'].dt.year # sacar columna con año
df['HOUR'] = df['OCCUR_TIME'].dt.hour # sacar columna con hora
df['YEARMONTH'] = df['OCCUR_DATE'].dt.strftime('%y%m') # sacar columna con año/mes
df.columns = df.columns.map(str.lower) # convertir columnas a minúscula

#st.write(df0)
#df = load_data('historico.csv', 'actual.csv')

# Dividir el layout en cuatro partes
c1, c2= st.columns((1,1)) # Entre paréntesis se indica el tamaño de las columnas


# Hacer código de la primera columna (Mapa sencillo):
c1.markdown("<h3 style='text-align: center; color: black;'> ¿Dónde han ocurrido disparos en Nueva York? </h3>", unsafe_allow_html=True)
year = c1.slider('Año en el que se presento el suceso', 2006, 2023) # Crear variable que me almacene el año seleccionado
c1.map(df[df['year']==year][['latitude', 'longitude']].dropna()) # Generar mapa
#c1.map([['latitude', 'longitude']])

# Hacer código de la segunda columna:
c2.markdown("<h3 style='text-align: center; color: black;'> ¿A qué horas ocurren disparos en Nueva York? </h3>", unsafe_allow_html=True)
hora = c2.slider('Hora en la que se presento el suceso', 0, 23) # Crear variable que me almacene la hora seleccionada

df2 = df[df['hour']==hora].dropna(subset=['latitude', 'longitude']) # Filtrar DataFrame

c2.write(pdk.Deck( # Código para crear el mapa
    
    # Set up del mapa
    map_style='mapbox://styles/mapbox/dark-v10',
    initial_view_state={
        'latitude' : df['latitude'].mean(),
        'longitude': df['longitude'].mean(),
        'zoom' : 9.5,
        'pitch': 50
        },
    
    # Capa con información
    layers = [pdk.Layer(
        'HexagonLayer',
        data = df2[['incident_key','latitude','longitude']],
        get_position = ['longitude','latitude'],
        radius = 100,
        extruded = True,
        elevation_scale = 4,
        elevation_range = [0,1000])]
    ))
