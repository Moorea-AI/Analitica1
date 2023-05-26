Introducción a la Analítica de Negocios
Tablón
Trabajo de clase
Personas
Introducción a la Analítica de Negocios
Próximas entregas
¡Yuju! ¡No tienes que entregar nada pronto!

Anuncia algo a tu clase
Tarea: "Tercera Entrega - Trabajo Final"
LAURA MARIA YARCE GOMEZ ha publicado una nueva tarea: Tercera Entrega - Trabajo Final
Fecha de creación: 23 may23 may

Anuncio: "Semana 14 - Dashboards"
LAURA MARIA YARCE GOMEZ
Fecha de creación: 12 may12 may (Última modificación: 23 may)
Semana 14 - Dashboards

historico.csv
Valores separados por comas

actual.csv
Valores separados por comas

Procfile
Archivo binario

requirements.txt
Texto

setup.sh
Texto

app.py
Texto

Tarea: "Seguimiento 4"
LAURA MARIA YARCE GOMEZ ha publicado una nueva tarea: Seguimiento 4
Fecha de creación: 28 abr28 abr

Anuncio: "Semana 13 - Visualización de datos…"
LAURA MARIA YARCE GOMEZ
Fecha de creación: 28 abr28 abr
Semana 13 - Visualización de datos (completa)

Visualización_de_datos.ipynb
Archivo binario


Anuncio: "Semana 13 - Visualización de datos…"
LAURA MARIA YARCE GOMEZ
Fecha de creación: 21 abr21 abr
Semana 13 - Visualización de datos (Primera parte)

Visualización_de_datos_estudiante.ipynb
Archivo binario


Anuncio: "Semana 12 - Tratar datos faltantes y…"
LAURA MARIA YARCE GOMEZ
Fecha de creación: 21 abr21 abr
Semana 12 - Tratar datos faltantes y duplicados

Tratar datos faltantes o duplicados.ipynb
Archivo binario


Anuncio: "Semana 11 - Series de tiempo"
LAURA MARIA YARCE GOMEZ
Fecha de creación: 20 abr20 abr
Semana 11 - Series de tiempo

Series de tiempo.ipynb
Archivo binario

Tarea: "Taller 2 - Python"
LAURA MARIA YARCE GOMEZ ha publicado una nueva tarea: Taller 2 - Python
Fecha de creación: 16 abr16 abr (Última modificación: 11 may)
Tarea: "Segunda Entrega - Trabajo Final"
LAURA MARIA YARCE GOMEZ ha publicado una nueva tarea: Segunda Entrega - Trabajo Final
Fecha de creación: 16 abr16 abr (Última modificación: 19 may)

Anuncio: "Semana 10 - Relacionar y resumir tablas"
LAURA MARIA YARCE GOMEZ
Fecha de creación: 15 abr15 abr
Semana 10 - Relacionar y resumir tablas

Relacionar_y_resumir_tablas.ipynb
Archivo binario

Tablón
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 12 17:28:25 2023

@author: lyarce
"""

# Cargar datos
import streamlit as st
import pandas as pd
import pydeck as pdk #Mapas avanzados
import plotly.express as px
import plotly.graph_objects as go
import base64

# Función para descargar base de datos
def get_table_download_link(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="datos.csv">Descargar archivo csv</a>'
    return href

# Utilizar la página completa en lugar de una columna central estrecha
st.set_page_config(layout="wide")


# Título principal, h1 denota el estilo del título 1
st.markdown("<h1 style='text-align: center; color: #951F0F;'>Histórico de disparos en Nueva York 🗽💥🔫 </h1>", unsafe_allow_html=True)

# Cargar datos
@st.cache(persist=True) # Código para que quede almacenada la información en el cache
def load_data(url1, url2):
    df0 = pd.read_csv(url1) # base historico
    df1 = pd.read_csv(url2) # base actual
    df = pd.concat([df0, df1]) # concatenar las bases
    df['OCCUR_DATE'] = pd.to_datetime(df['OCCUR_DATE']) # convertir fecha a formato fecha
    df['OCCUR_TIME'] = pd.to_datetime(df['OCCUR_TIME'], format='%H:%M:%S') # convertir hora a formato fecha
    df['YEAR'] = df['OCCUR_DATE'].dt.year # sacar columna con año
    df['HOUR'] = df['OCCUR_TIME'].dt.hour # sacar columna con hora
    df['YEARMONTH'] = df['OCCUR_DATE'].dt.strftime('%y%m') # sacar columna con año/mes
    df.columns = df.columns.map(str.lower) # convertir columnas a minúscula
    return df

df = load_data('historico.csv', 'actual.csv')


#----------------------------------------
c1, c2, c3, c4, c5= st.columns((1,1,1,1,1)) # Dividir el ancho en 5 columnas de igual tamaño

#--------------- Top sexo
c1.markdown("<h3 style='text-align: left; color: gray;'> Top Sexo </h3>", unsafe_allow_html=True)

top_perp_name = (df['perp_sex'].value_counts().index[0])
top_perp_num = (round(df['perp_sex'].value_counts()/df['perp_sex'].value_counts().sum(),2)*100)[0]
top_vic_name = (df['vic_sex'].value_counts().index[0])
top_vic_num = (round(df['vic_sex'].value_counts()/df['vic_sex'].value_counts().sum(),2)*100)[0]

c1.text('Atacante: '+str(top_perp_name)+', '+str(top_perp_num)+'%')
c1.text('Víctima: '+str(top_vic_name)+', '+str(top_vic_num)+'%')

#--------------- Top raza
c2.markdown("<h3 style='text-align: left; color: gray;'> Top Raza </h3>", unsafe_allow_html=True)

top_perp_name = (df['perp_race'].value_counts().index[0]).capitalize()
top_perp_num = (round(df['perp_race'].value_counts()/df['perp_race'].value_counts().sum(),2)*100)[0]
top_vic_name = (df['vic_race'].value_counts().index[0]).capitalize()
top_vic_num = (round(df['vic_race'].value_counts()/df['vic_race'].value_counts().sum(),2)*100)[0]

c2.text('Atacante: '+str(top_perp_name)+', '+str(top_perp_num)+'%')
c2.text('Víctima: '+str(top_vic_name)+', '+str(top_vic_num)+'%')

#--------------- Top edad
c3.markdown("<h3 style='text-align: left; color: gray;'> Top Edad </h3>", unsafe_allow_html=True)

top_perp_name = (df['perp_age_group'].value_counts().index[0])
top_perp_num = (round(df['perp_age_group'].value_counts()/df['perp_age_group'].value_counts().sum(),2)*100)[0]
top_vic_name = (df['vic_age_group'].value_counts().index[0])
top_vic_num = (round(df['vic_age_group'].value_counts()/df['vic_age_group'].value_counts().sum(),2)*100)[0]

c3.text('Atacante: '+str(top_perp_name)+', '+str(top_perp_num)+'%')
c3.text('Víctima: '+str(top_vic_name)+', '+str(top_vic_num)+'%')

#--------------- Top barrio
c4.markdown("<h3 style='text-align: left; color: gray;'> Top Barrio </h3>", unsafe_allow_html=True)

top_perp_name = (df['boro'].value_counts().index[0]).capitalize()
top_perp_num = (round(df['boro'].value_counts()/df['boro'].value_counts().sum(),2)*100)[0]

c4.text('Barrio: '+str(top_perp_name)+', '+str(top_perp_num)+'%')

#--------------- Top hora
c5.markdown("<h3 style='text-align: left; color: gray;'> Top Hora  </h3>", unsafe_allow_html=True)

top_perp_name = (df['hour'].value_counts().index[0])
top_perp_num = (round(df['hour'].value_counts()/df['hour'].value_counts().sum(),2)*100)[0]

c5.text('Hora: '+str(top_perp_name)+', '+str(top_perp_num)+'%')


#---------------------------------------------------------------------

c1, c2= st.columns(2) 

# Hacer código de la primera columna (Mapa sencillo):
c1.markdown("<h3 style='text-align: center; color: black;'> ¿Dónde han ocurrido disparos en Nueva York? </h3>", unsafe_allow_html=True)
anio = c1.slider('Año en el que se presento el suceso', 2006, 2023) # Crear variable que me almacene el año seleccionado
c1.map(df[df['year']==anio][['latitude', 'longitude']].dropna()) # Generar mapa
  
# Hacer código de la segunda columna:
c2.markdown("<h3 style='text-align: center; color: black;'> ¿A qué horas ocurren disparos en Nueva York? </h3>", unsafe_allow_html=True)
hora = c2.slider('Hora en la que se presento el suceso', 0, 23) # Crear variable que me almacene la hora seleccionada
df2 = df[df['hour']==hora].dropna(subset =['latitude','longitude']) # Filtrar DataFrame

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
        data = df2[['latitude','longitude']],
        get_position = ['longitude','latitude'],
        radius = 100,
        extruded = True,
        elevation_scale = 4,
        elevation_range = [0,1000])]
    ))

#---------------------------------------------------------------------
# Título de la siguiente sección
st.markdown("<h3 style='text-align: center; color: black;'> ¿Cómo ha sido la evolución de disparos por barrio? </h3>", unsafe_allow_html=True)

# Organizar DataFrame
df2 = df.groupby(['yearmonth','boro'])[['incident_key']].count().reset_index().rename(columns = {'incident_key':'disparos'})

# Generar gráfica
fig = px.line(df2, x='yearmonth', y='disparos', color = 'boro', width=1500, height=450)
# Editar gráfica
fig.update_layout(
        title_x=0.5,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        template = 'simple_white',
        xaxis_title="<b>Año<b>",
        yaxis_title='<b>Cantidad de incidentes<b>',
        legend_title_text='',
        
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=0.7))
st.plotly_chart(fig)

#---------------------------------------------------------------------

c4, c5, c6, c7= st.columns((1,1,1,1))

################ ---- Primera Gráfica

# Definir título
c4.markdown("<h3 style='text-align: center; color: black;'> ¿Qué edad tienen los atacantes? </h3>", unsafe_allow_html=True)


# Organizar DataFrame
df2 = df.groupby(['perp_age_group'])[['incident_key']].count().reset_index().rename(columns = {'incident_key':'disparos'})

df2['perp_age_group'] = df2['perp_age_group'].replace({'940':'N/A',
                              '224':'N/A','1020':'N/A', '1028':'N/A', '(null)':'N/A','UNKNOWN':'N/A'})

df2 = df2.groupby(['perp_age_group'])[['disparos']].sum().reset_index()


# Crear categoría para organizar el orden de las edades
df2['perp_age_group2'] = df2['perp_age_group'].replace({'<18':'1',
                              '18-24':'2',
                              '25-44':'3',
                              '45-64':'4',
                              '65+':'5',
                              'N/A': '6'})

# Aplicar orden al DataFrame
df2= df2.sort_values('perp_age_group2',ascending = False)

# Hacer gráfica
fig = px.bar(df2, x="disparos", y="perp_age_group", orientation='h', width=370,  height=370)
fig.update_layout(xaxis_title="<b>Cant. Atacantes<b>",
                  yaxis_title="<b>Rango Edad<b>", template = 'simple_white',
                  paper_bgcolor='rgba(0,0,0,0)',
                  plot_bgcolor='rgba(0,0,0,0)')

# Enviar gráfica a streamlit
c4.plotly_chart(fig)

################ ---- Segunda Gráfica

# Definir título
c5.markdown("<h3 style='text-align: center; color: black;'> ¿Qué edad tienen las victimas? </h3>", unsafe_allow_html=True)


# Organizar DataFrame
df2 = df.groupby(['vic_age_group'])[['incident_key']].count().reset_index().rename(columns = {'incident_key':'disparos'})

df2['vic_age_group'] = df2['vic_age_group'].replace({'940':'N/A',
                              '224':'N/A','1020':'N/A', '1028':'N/A', '(null)':'N/A','UNKNOWN':'N/A',
                              '1022':'N/A'})

df2 = df2.groupby(['vic_age_group'])[['disparos']].sum().reset_index()


# Crear categoría para organizar el orden de las edades
df2['vic_age_group2'] = df2['vic_age_group'].replace({'<18':'1',
                              '18-24':'2',
                              '25-44':'3',
                              '45-64':'4',
                              '65+':'5',
                              'N/A': '6'})

# Aplicar orden al DataFrame
df2= df2.sort_values('vic_age_group2',ascending = False)

# Hacer gráfica
fig = px.bar(df2, x="disparos", y="vic_age_group", orientation='h', width=370,  height=370)
fig.update_layout(xaxis_title="<b>Cant. Victimas<b>",
                  yaxis_title="<b>Rango Edad<b>", template = 'simple_white',
                  paper_bgcolor='rgba(0,0,0,0)',
                  plot_bgcolor='rgba(0,0,0,0)')

# Enviar gráfica a streamlit
c5.plotly_chart(fig)

################ ---- Tercera Gráfica

# Definir título
c6.markdown("<h3 style='text-align: center; color: Black;'> ¿Cuál es el sexo del atacante? </h3>", unsafe_allow_html=True)

# Organizar DataFrame
df2 = df.groupby('perp_sex')[['incident_key']].count().reset_index().sort_values('incident_key', ascending = False)

df2['perp_sex'] = df2['perp_sex'].replace({'(null)':'U'})

# Organizar DataFrame
df2 = df2.groupby('perp_sex')[['incident_key']].sum().reset_index().sort_values('incident_key', ascending = False)


# Hacer gráfica
fig = px.pie(df2, values = 'incident_key', names="perp_sex",
             width=370, height=370)

fig.update_layout(template = 'simple_white',
                  paper_bgcolor='rgba(0,0,0,0)',
                  plot_bgcolor='rgba(0,0,0,0)',
                  legend=dict(orientation="h",
                              yanchor="bottom",
                              y=-0.4,
                              xanchor="center",
                              x=0.5))

# Enviar gráfica a streamlit
c6.plotly_chart(fig)

################ ---- Cuarta Gráfica

# Definir título
c7.markdown("<h3 style='text-align: center; color: Black;'> ¿Cuál es el sexo de la víctima? </h3>", unsafe_allow_html=True)

# Organizar DataFrame
df2 = df.groupby('vic_sex')[['incident_key']].count().reset_index().sort_values('incident_key', ascending = False)

# Hacer gráfica
fig = px.pie(df2, values = 'incident_key', names="vic_sex",
             width=370, height=370,   
             color_discrete_map={
                "M": "red",
                "F": "green",
                "U": "blue"})

fig.update_layout(template = 'simple_white',
                  paper_bgcolor='rgba(0,0,0,0)',
                  legend=dict(orientation="h",
                              yanchor="bottom",
                              y=-0.4,
                              xanchor="center",
                              x=0.5))

# Enviar gráfica a streamlit
c7.plotly_chart(fig)

#---------------------------------------------------------------------

# Definir título
st.markdown("<h3 style='text-align: center; color: Black;'> Evolución de disparos por año en las horas con más y menos sucesos </h3>", unsafe_allow_html=True)

# Organizar DataFrame
df2 = df[df['hour'].isin([23,9])].groupby(['year','hour'])[['incident_key']].count().sort_values('incident_key', ascending = False).reset_index() 

df2['hour'] = df2['hour'].astype('category')


# Hacer gráfica
fig = px.bar(df2, x='year', y='incident_key', color ='hour', barmode='group', width=1500, height=450)
fig.update_layout(
        title_x=0.5,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        template = 'simple_white',
        legend_title_text = '<b>Hora<b>',
        xaxis_title="<b>Año<b>",
        yaxis_title="<b>Cantidad de incidentes<b>")

# Enviar gráfica a streamlit
st.plotly_chart(fig)

#---------------------------------------------------------------------


# Hacer un checkbox
if st.checkbox('Obtener datos por fecha y barrio', False):
    
    # Código para generar el DataFrame
    df2 = df.groupby(['occur_date','boro'])[['incident_key']].count().reset_index().rename(columns ={'boro':'Barrio','occur_date':'Fecha','incident_key':'Cantidad'})
    df2['Fecha'] = df2['Fecha'].dt.date
    
    # Código para convertir el DataFrame en una tabla plotly resumen
    fig = go.Figure(data=[go.Table(
        header=dict(values=list(df2.columns),
        fill_color='lightgrey',
        line_color='darkslategray'),
        cells=dict(values=[df2.Fecha, df2.Barrio, df2.Cantidad],fill_color='white',line_color='lightgrey'))
       ])
    fig.update_layout(width=500, height=450)

# Enviar tabla a streamlit
    st.write(fig)

    
# Generar link de descarga
    st.markdown(get_table_download_link(df2), unsafe_allow_html=True)

app.py
Mostrando app.py.