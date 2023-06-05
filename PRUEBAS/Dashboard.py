# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 08:36:35 2023

@author: Moorea_med
"""

# Cargar datos
import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.express as px
import plotly.graph_objects as go
import base64

st.set_page_config(layout="wide") #Se usa todo el ancho de página

# Título principal, h1 denota el estilo del título 1
st.markdown("<h1 style='text-align: center; color: #951F0F;'>Eficacia de los sistemas de incendio en Canadá</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: #CCCCCC;'>Histórico de disparos en Nueva York 🗽💥🔫 </h2>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #666666;'>Histórico de disparos en Nueva York 🗽💥🔫 </h3>", unsafe_allow_html=True)



