# -*- coding: utf-8 -*-
"""

FACULTAD DE INGENIERÍA<br>
DEPARTAMENTO DE INGENIERÍA INDUSTRIAL<br>
INTRODUCCIÓN A LA ANALÍTICA DE NEGOCIOS<br>
TRABAJO DEL CURSO - SEGUNDA ENTREGA: 15% <br>
Semestre 2023-01<br>

Equipo de trabajo: Aura Luz Moreno Díaz, Marcelo Lemus, Verónica Andrea Morales González

---
#Carga de las librerias necesarias para la ejecución del código. En este caso usaremos Pandas y Numpy renombrándolas como pd y np
"""

#Carga de las librerias necesarias para la ejecución del código
import streamlit as st
import pandas as pd
import pydeck as pdk #Mapas avanzados
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import base64
import numpy as np
import geopy
from geopy.geocoders import Nominatim


#BASES DE DATOS CRUDAS
AH  = pd.read_csv('https://www.4minds.solutions/tarea/final/BDALARMAHUMO.csv', sep=';',  low_memory=False) #Base de datos de Alarmas de Humo
MOR = pd.read_csv('https://www.4minds.solutions/tarea/final/BDMORTALIDAD.csv', sep=';',  low_memory=False) #Base de datos de Mortalidad
ROC = pd.read_csv('https://www.4minds.solutions/tarea/final/BDROCIADORES.csv', sep=';',  low_memory=False) #Base de datos de Rociadores
DES = pd.read_csv('https://www.4minds.solutions/tarea/final/BDGENERALDESASTRES.csv', sep=';',  low_memory=False) #Base de datos de Desastres en general

#BASES DE DATOS YA LIMPIAS
DESA = pd.read_csv('https://www.4minds.solutions/tarea/final/DESA.csv', sep=';',  low_memory=False) #Base de datos de Desastres en general
CONS = pd.read_csv('https://www.4minds.solutions/tarea/final/CONS.csv', sep=';',  low_memory=False) #Base de datos de Desastres en general


st.set_page_config(layout="wide")

#ENCABEZADO DEL TRABAJO Y EQUIPO
st.markdown("<h5 style='text-align: center; color: #666666; font-family:helvetica;'>UNIVERSIDAD DE ANTIOQUIA <br> FACULTAD DE INGENIERÍA <br> DEPARTAMENTO DE INGENIERÍA INDUSTRIAL <br> INTRODUCCIÓN A LA ANALÍTICA DE NEGOCIOS</h5>", unsafe_allow_html=True)
st.markdown("<h6 style='text-align: center; color: #666666; font-family: helvetica;'>Equipo de trabajo: Aura Luz Moreno Díaz, Marcelo Lemus, Verónica Andrea Morales González</h6>", unsafe_allow_html=True)
st.markdown("<h6 style='text-align: center; color: #666666; font-family: helvetica;'>Semestre: 2023-1</h6>", unsafe_allow_html=True)

#IMAGEN DECORATIVA
image_path = "Bandera.jpg"
html_code = f"""
<div style="display: flex; justify-content: center;">
    <img src="data:image/jpeg;base64,{base64.b64encode(open(image_path, "rb").read()).decode()}" width=100px>
</div>
"""
st.markdown(html_code, unsafe_allow_html=True)

# TITULO PRINCIPAL
st.markdown("<h1 style='text-align: center; color: #990000; font-family: helvetica; margin-top: 20px;'>Eficacia de los sistemas de incendio en Canadá</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #666666; font-family: helvetica;'>Comparativo entre aspersores y alarmas de humo</h3>", unsafe_allow_html=True)

#Abstract
st.markdown("<h6 style='text-align: left; color: #525252; font-family: monospace;'>Este trabajo de investigación examina la eficacia de los sistemas de prevención de incendios en Canadá, centrándose específicamente en los detectores de humo y los sistemas de rociadores en incidentes de incendios estructurales. El estudio comienza proporcionando una visión general del número total de desastres, incluyendo varios tipos, que han ocurrido en Canadá, según se informa en las bases de datos abiertas disponibles. A partir de ahí, el análisis se reduce para explorar los tipos específicos de incidentes de incendios, específicamente incendios forestales e incendios estructurales. Finalmente, la investigación se enfoca aún más en evaluar la eficacia de los sistemas de rociadores y detectores de humo en la mitigación de los daños causados por los incendios estructurales..</h6>", unsafe_allow_html=True)

#     1

#VISIÓN GENERAL DE DESASTRES EN CANADA

st.markdown("<h4 style='text-align: left; color: #990000; font-family: helvetica;'>Visión general de los desastres ocurridos en Canadá desde 1900 hasta 2022</h4>", unsafe_allow_html=True)

#GRAFICA DE BARRAS  GENERAL DE DESASTRES
desastre = DESA['EVENT TYPE'].value_counts()
desastre_df = pd.DataFrame({'EVENT TYPE': desastre.index, 'Cantidad desastres': desastre.values})
figd = px.bar(desastre_df, x='EVENT TYPE', y='Cantidad desastres', labels={'EVENT TYPE': 'Tipo de desastre', 'desastre_df': 'Tipo de desastre'})
st.plotly_chart(figd, use_container_width=True)

#EXPLICACIÓN
st.markdown("<h6 style='text-align: left; color: #525252; font-family: monospace;'>Existe una amplia variedad de tipos de desastres, pero al observar la frecuencia de ocurrencia, se destaca que las inundaciones son el tipo de desastre más común, seguido de las tormentas y, en tercer lugar, los incendios. Por lo tanto, es pertinente poner énfasis en estos tipos de desastres debido a su relevancia en términos de frecuencia.</h6>", unsafe_allow_html=True)





st.markdown("<hr>", unsafe_allow_html=True)


st.markdown("<h6 style='text-align: left; color: #525252; font-family: monospace;'>Teniendo en cuenta el top 3 en ocurrencias y fatalidades, presentamos un gráfico de torta para ver la relación entre las tres según el número de fatalidades.</h6>", unsafe_allow_html=True)


#GRAFICO DE CANTIDAD DE MUERTES POR EVENTO TOP 3
DESA['NORMALIZED TOTAL COST'] = DESA['NORMALIZED TOTAL COST'].astype(str)
DESA['NORMALIZED TOTAL COST'] = DESA['NORMALIZED TOTAL COST'].str.replace('.', '')
DESA['NORMALIZED TOTAL COST'] = pd.to_numeric(DESA['NORMALIZED TOTAL COST'], errors='coerce')
eventos = ['fire', 'storm', 'flood']
filtro_eventos = DESA['EVENT TYPE'].isin(eventos)
datos_filtrados = DESA[filtro_eventos]
datos_filtrados['FATALITIES'] = pd.to_numeric(datos_filtrados['FATALITIES'], errors='coerce')
datos_filtrados = datos_filtrados.dropna(subset=['FATALITIES'])
muertes = datos_filtrados.groupby('EVENT TYPE')['FATALITIES'].sum().reset_index()
df_muertes = pd.DataFrame({'Tipo de evento': muertes['EVENT TYPE'], 'Cantidad de muertes': muertes['FATALITIES']})
fig = px.pie(df_muertes, values='Cantidad de muertes', names='Tipo de evento', 
             labels={'Cantidad de muertes': 'Cantidad de muertes', 'Tipo de evento': 'Tipo de evento'},
             title='Cantidad de muertes por tipo de evento')
st.plotly_chart(fig)




#SECCIÓN DE LOS TOP 3 DE MUERTES POR DESASTRE
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<h6 style='text-align: left; color: #990000; font-family: helvetica;'>Top 3 de Muertes por desastre</h6>", unsafe_allow_html=True)

im2, im3, im1 = st.columns((1,1,1)) 

im1_image= "inundaciones.jpg"
im1.image(im1_image, width=200, use_column_width=None, clamp=False, channels="RGB", output_format="auto")

im2_image= "tormentas.jpg"
im2.image(im2_image, width=200, use_column_width=None, clamp=False, channels="RGB", output_format="auto")

im3_image= "incendiosCanada.jpg"
im3.image(im3_image,width=200, use_column_width=None, clamp=False, channels="RGB", output_format="auto")


c2, c3, c1 = st.columns((1,1,1)) 

#--------------- Top inundaciones
c1.markdown("<h3 style='text-align: left; color: gray;'> INUNDACIONES </h3>", unsafe_allow_html=True)

DESA['EVENT TYPE'] = DESA['EVENT TYPE'].str.strip()
filtro_inundaciones = DESA['EVENT TYPE'] == 'flood'
datos_inundaciones = DESA[filtro_inundaciones]
datos_limpios = datos_inundaciones[datos_inundaciones['FATALITIES'] != 'SIN']
datos_limpios['FATALITIES'] = pd.to_numeric(datos_limpios['FATALITIES'])
muertes_inundaciones = datos_limpios['FATALITIES'].sum()
c1.text("Total: {}".format(muertes_inundaciones))

#--------------- Top Tormentas
c2.markdown("<h3 style='text-align: left; color: gray;'> TORMENTAS </h3>", unsafe_allow_html=True)

DESA['EVENT TYPE'] = DESA['EVENT TYPE'].str.strip()
filtro_tormentas = DESA['EVENT TYPE'] == 'storm'
datos_tormentas = DESA[filtro_tormentas]
datos_limpios_tormentas = datos_tormentas[datos_tormentas['FATALITIES'] != 'SIN']
datos_limpios_tormentas['FATALITIES'] = pd.to_numeric(datos_limpios_tormentas['FATALITIES'])
muertes_tormentas = datos_limpios_tormentas['FATALITIES'].sum()
c2.text("Total: {}".format(muertes_tormentas))

#--------------- Top incendios
c3.markdown("<h3 style='text-align: left; color: gray;'> INCENDIOS </h3>", unsafe_allow_html=True)

DESA['EVENT TYPE'] = DESA['EVENT TYPE'].str.strip()
filtro_incendios = DESA['EVENT TYPE'] == 'fire'
datos_incendios = DESA[filtro_incendios]
datos_limpios_incendios = datos_incendios[datos_incendios['FATALITIES'] != 'SIN']
datos_limpios_incendios['FATALITIES'] = pd.to_numeric(datos_limpios_incendios['FATALITIES'])
muertes_incendios = datos_limpios_incendios['FATALITIES'].sum()
c3.text("Total: {}".format(muertes_incendios))



st.markdown("<h6 style='text-align: left; color: #525252; font-family: monospace;'>Como podemos ver, la tasa de mortalidad la encabezan las tormentas con 1.725 muertes. Este tipo de tormentas incluyen las tormentas de nieve que son comunes en Canadá y se agravan por ser el segundo país más frío del mundo. En segundo lugar están los incendios, que incluyen los estructurales (o de construcciones humanas) y los forestales con  388 muertes y finalmente las inundaciones.</h6>", unsafe_allow_html=True)


st.markdown("<hr>", unsafe_allow_html=True)




#TOP 3 DE PÉRDIDAS ECONÓMICAS POR DESASTRE
st.markdown("<h6 style='text-align: left; color: #990000; font-family: helvetica;'>Top 3 de pérdidas económicas por desastre</h6>", unsafe_allow_html=True)


DESA['NORMALIZED TOTAL COST'] = DESA['NORMALIZED TOTAL COST'].astype(str)
DESA['NORMALIZED TOTAL COST'] = DESA['NORMALIZED TOTAL COST'].str.replace(',', '')
DESA['NORMALIZED TOTAL COST'] = pd.to_numeric(DESA['NORMALIZED TOTAL COST'], errors='coerce')
eventos = ['fire', 'storm', 'flood']
filtro_eventos = DESA['EVENT TYPE'].isin(eventos)
datos_filtrados = DESA[filtro_eventos]
datos_filtrados = datos_filtrados.dropna(subset=['NORMALIZED TOTAL COST'])
costos = datos_filtrados.groupby('EVENT TYPE')['NORMALIZED TOTAL COST'].sum().reset_index()
df_costos = pd.DataFrame({'Tipo de evento': costos['EVENT TYPE'], 'Costo económico': costos['NORMALIZED TOTAL COST']})
fig = px.pie(df_costos, values='Costo económico', names='Tipo de evento',
             labels={'Costo económico': 'Costo económico', 'Tipo de evento': 'Tipo de evento'},
             title='Costo económico por tipo de evento')

st.plotly_chart(fig)




pe2, pe1, pe3 = st.columns((1,1,1)) # Dividir el ancho en  columnas de igual tamaño


#--------------- Top inundaciones
pe1.markdown("<h3 style='text-align: left; color: gray;'> INUNDACIONES </h3>", unsafe_allow_html=True)


DESA['EVENT TYPE'] = DESA['EVENT TYPE'].str.strip()
pe1_filtro_inundaciones = DESA['EVENT TYPE'] == 'flood'
pe1_datos_inundaciones = DESA[pe1_filtro_inundaciones]
pe1_datos_limpios = pe1_datos_inundaciones[pe1_datos_inundaciones['ESTIMATED TOTAL COST'] != 'SIN']
pe1_datos_limpios['ESTIMATED TOTAL COST'] = pd.to_numeric(pe1_datos_limpios['ESTIMATED TOTAL COST'])
pe1_perdidas_economicas = pe1_datos_limpios['ESTIMATED TOTAL COST'].sum()
pe1_perdidas_formateadas = "${:,.2f}".format(pe1_perdidas_economicas)
pe1.text("Total: {}".format(pe1_perdidas_formateadas))



#--------------- Top tormentas
pe2.markdown("<h3 style='text-align: left; color: gray;'> TORMENTAS </h3>", unsafe_allow_html=True)


DESA['EVENT TYPE'] = DESA['EVENT TYPE'].str.strip()
pe2_filtro_tormentas = DESA['EVENT TYPE'] == 'storm'
pe2_datos_tormentas = DESA[pe2_filtro_tormentas]
pe2_datos_limpios = pe2_datos_tormentas[pe2_datos_tormentas['ESTIMATED TOTAL COST'] != 'SIN']
pe2_datos_limpios['ESTIMATED TOTAL COST'] = pd.to_numeric(pe2_datos_limpios['ESTIMATED TOTAL COST'])
pe2_perdidas_economicas = pe2_datos_limpios['ESTIMATED TOTAL COST'].sum()
pe2_perdidas_formateadas = "${:,.2f}".format(pe2_perdidas_economicas)
pe2.text("Total: {}".format(pe2_perdidas_formateadas))


#--------------- Top incendios
pe3.markdown("<h3 style='text-align: left; color: gray;'> INCENDIOS </h3>", unsafe_allow_html=True)


DESA['EVENT TYPE'] = DESA['EVENT TYPE'].str.strip()
pe3_filtro_incendios = DESA['EVENT TYPE'] == 'fire'
pe3_datos_incendios = DESA[pe3_filtro_incendios]
pe3_datos_limpios = pe3_datos_incendios[pe3_datos_incendios['ESTIMATED TOTAL COST'] != 'SIN']
pe3_datos_limpios['ESTIMATED TOTAL COST'] = pd.to_numeric(pe3_datos_limpios['ESTIMATED TOTAL COST'])
pe3_perdidas_economicas = pe3_datos_limpios['ESTIMATED TOTAL COST'].sum()
pe3_perdidas_formateadas = "${:,.2f}".format(pe3_perdidas_economicas)
pe3.text("Total: {}".format(pe3_perdidas_formateadas))

st.markdown("<h6 style='text-align: left; color: #525252; font-family: monospace;'>En este caso podemos observar las tormentas como las mayores generadoras de pérdidas, en segundo lugar las inundaciones y finalmente los incendios ya que las pérdidas ecológicas no tienen una escala económica cuantificable y solo se toman las pérdidas en incendios estructurales.</h6>", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)














#Ahora graficamos la evolucion de las muertes por año para cada tipo de desastre (top 3)
st.markdown("<h2 style='text-align: center; color: #930000;'>Evolución de las muertes causadas por los tres tipos de desastres mas comunes</h2>", unsafe_allow_html=True)
 


muertes_por_anio = datos_filtrados.groupby(['YEAR' ,'EVENT TYPE'])['FATALITIES'].sum().reset_index()


# Generar gráfica
fig = px.line(muertes_por_anio, x='YEAR', y='FATALITIES', color = 'EVENT TYPE', width=1000, height=450, title="Evoluion de muertes causadas por tipo de evento")
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
            orientation="v",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1.5))
st.plotly_chart(fig)


# AGREGAMOS UNA IMAGEN
imageT= "tormentas.jpg"

st.image(imageT, caption="Tormentas. Tomado de: https://www.istockphoto.com/es/foto/tormenta-entrante-sobre-el-r%C3%ADo-bow-en-calgary-gm1327119477-411576407?phrase=tormentas%20en%20canada", width=None, use_column_width=150, clamp=False, channels="RGB", output_format="auto")

#3
st.markdown("<h2 style='text-align: center; color: #930000;'>Costo promedio de la normalización por tipo de desastre</h2>", unsafe_allow_html=True)


import pandas as pd
import numpy as np

#Convertimos a tipo string y removemos separador de miles y la convertimos a tipo numerico haciendo coerción en los errores para que los valores no numéricos se conviertan en NaN.
DESA['NORMALIZED TOTAL COST'] = DESA['NORMALIZED TOTAL COST'].astype(str)
DESA['NORMALIZED TOTAL COST'] = DESA['NORMALIZED TOTAL COST'].str.replace('.', '')
DESA['NORMALIZED TOTAL COST'] = pd.to_numeric(DESA['NORMALIZED TOTAL COST'], errors='coerce')

eventosC = ['fire', 'storm', 'flood']
filtroC = DESA['EVENT TYPE'].isin(eventosC)
datos_filtradosC = DESA[filtroC]
costo = datos_filtradosC.groupby('EVENT TYPE')['NORMALIZED TOTAL COST'].mean().reset_index()
df_costos = pd.DataFrame({'Tipo de evento': costo['EVENT TYPE'], 'Costo': costo['NORMALIZED TOTAL COST']})
figC = px.bar(df_costos, x='Tipo de evento', y='Costo',labels={'Tipo de evento': 'Tipo de evento', 'Costo': 'Costo'},title='costo por tipo de evento')

st.plotly_chart(figC)

###
st.markdown("<h6 style='text-align: center; color: #525252;'>Se tiene que el tipo de desastre que implica mayores costos para la normalización entre los tres definidos, es el desastre por incendio, ocupando a nivel general, el segundo lugar entre todos los tipos de desastres. Los incendios pueden acabar con todo a su paso si no son controlados y su costo promedio de normalización está en $39,595,179,216,216, luego están las tormentas que son incontrolables y las inundaciones que pueden acabar también con  los enseres y estructuras muy fácilmente.</h2>", unsafe_allow_html=True)
# AGREGAMOS UNA IMAGEN
imagein= "incendio.jpg"

st.image(imagein, caption="Incendios. Tomado de: https://www.istockphoto.com/es/foto/bombero-de-retenci%C3%B3n-de-la-manguera-se%C3%B1alando-corriente-de-agua-en-fuego-gm157442677-9126810?phrase=incendio%20en%20canada", width=None, use_column_width=150, clamp=False, channels="RGB", output_format="auto")
            
#4
st.markdown("<h2 style='text-align: center; color: #930000;'>Porcentaje de incendios con respecto al resto de desastres</h2>", unsafe_allow_html=True)

import plotly.express as px
import pandas as pd

#Calculamos el número de incendios y el número total de desastres
num_incendios = DESA[DESA['EVENT TYPE'] == 'fire'].shape[0]
num_total_desastres = DESA.shape[0]

# Calculamos el número de desastres que no son incendios para poder configurar bien la torta
num_desastres_no_incendios = num_total_desastres - num_incendios
porcentaje_incendios = (num_incendios / num_total_desastres) * 100
porcentaje_no_incendios = 100 - porcentaje_incendios

data = pd.DataFrame({'Tipo de Desastre': ['Incendios', 'Otros Desastres'], 'Porcentaje': [porcentaje_incendios, porcentaje_no_incendios]})

figPP = px.pie(data, values='Porcentaje', names='Tipo de Desastre', hole=0.5)
st.plotly_chart(figPP)

###
st.markdown("<h6 style='text-align: center; color: #525252;'>Se tiene que el 8.97% del total de desastres están dados por incendios, lo cual es un número importante si se tiene en cuenta que dentro de la base hay 32 tipos de desastres en total, y que una distribución promedio sería de 3,1% para cada desastre.</h2>", unsafe_allow_html=True)

#5
st.markdown("<h2 style='text-align: center; color: #930000;'>Cantidad de incendios por año</h2>", unsafe_allow_html=True)


#Filtramos los registros que corresponden a incendios
incendios = DESA[DESA['EVENT TYPE'] == 'fire']

#calculamos la cantidad de incendios por año
cantidad_incendios_por_año = incendios['YEAR'].value_counts().sort_index()

data = pd.DataFrame({'Año': cantidad_incendios_por_año.index, 'Cantidad de Incendios': cantidad_incendios_por_año.values})

data.plot( 'Año' , 'Cantidad de Incendios' )

###
st.markdown("<h6 style='text-align: center; color: #525252;'>Puede observarse en el gráfico, que la mayor cantidad de incendios se han venido presentando en los últimos 40 años, ya que entre los años 1900 y 1980 se presentaron solo 15 incendios, mientras que después de 1980 y hasta el 2020, se presentaron 115 incendios. Esto también se puede presentar cuando no existe información disponible o bien se empezó a tomar oficialmente después de un año en particular, cuando ya se tenía establecido todo el sistema para prevención de desastres.</h2>", unsafe_allow_html=True)
            
#6
st.markdown("<h2 style='text-align: center; color: #930000;'>Tasa de mortalidad de los incendios por año</h2>", unsafe_allow_html=True)

# Convertimos las columnas a tipo numerico
DESA['FATALITIES'] = pd.to_numeric(DESA['FATALITIES'], errors='coerce')
DESA['YEAR'] = pd.to_numeric(DESA['YEAR'], errors='coerce')

#Sacamos solo los que digan Fire y calculamos el total por año y cuales con muertos
incendios = DESA[DESA['EVENT TYPE'] == 'fire']
total_incendios = incendios.groupby('YEAR').size()
incendios_muertos = incendios.groupby('YEAR')['FATALITIES'].count()

#Ahora si calculamos la tasa de mortalidad y creamos el dataframe*1
tasa_mortalidad = round(((incendios_muertos / total_incendios)*100),2)
tasa_mortalidad_df = pd.DataFrame({'YEAR': tasa_mortalidad.index, 'tasa de Mortalidad (%)': tasa_mortalidad.values})
figm = px.bar(tasa_mortalidad_df, x='YEAR', y='tasa de Mortalidad (%)', labels={'Año': 'Año', 'tasa_mortalidad_df': 'tasa de Mortalidad (%)'})

st.plotly_chart(figm)

###
st.markdown("<h6 style='text-align: center; color: #525252;'>Se observa que la tasa de mortalidad en generales alta en los incendios ocurridos durante 1900 y 1998, sin embargo, para los 22 años siguientes,  la mortalidad en cada evento varió entre el 20% y el 100%.</h2>", unsafe_allow_html=True)


#7
st.markdown("<h2 style='text-align: center; color: #930000;'>Distribución de ocurrencia de incendios por día de la semana</h2>", unsafe_allow_html=True)

import plotly.express as px

# Convertir las columnas 'YEAR', 'MONTH' y 'DAY' a tipo fecha para poder concatenar la fecha y sacar el dia de la semana específico
DESA['YEAR'] = pd.to_datetime(DESA['YEAR'], format='%Y', errors='coerce')
DESA['MONTH'] = pd.to_datetime(DESA['MONTH'], format='%m', errors='coerce')
DESA['DAY'] = pd.to_datetime(DESA['DAY'], format='%d', errors='coerce')

#Creamos la columna weekday para determinar el dia de la semana y filtramos por incendios
DESA['WEEKDAY'] = DESA['DAY'].dt.day_name()
incendios = DESA[DESA['EVENT TYPE'] == 'fire']
ocurrencia_incendios = incendios['WEEKDAY'].value_counts()

df_ocurrencia_incendios = pd.DataFrame({'Día de la semana': ocurrencia_incendios.index, 'Ocurrencia': ocurrencia_incendios.values})
dias_semana_ordenados = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
df_ocurrencia_incendios['Día de la semana'] = pd.Categorical(df_ocurrencia_incendios['Día de la semana'], categories=dias_semana_ordenados, ordered=True)
df_ocurrencia_incendios = df_ocurrencia_incendios.sort_values('Día de la semana')
figS = px.bar(df_ocurrencia_incendios, x='Día de la semana', y='Ocurrencia', color='Día de la semana',title='Ocurrencia de Incendios por Día de la Semana', )
st.plotly_chart(figS)

###
st.markdown("<h6 style='text-align: center; color: #525252;'>Se observa que hay mayor incidencia de incendios el Lunes, seguido del Martes y luego el Miércoles.</h2>", unsafe_allow_html=True)

#8

st.markdown("<h2 style='text-align: center; color: #930000;'>Número de incendios por localidad</h2>", unsafe_allow_html=True)


incendios_por_localidad = CONS['GEO'].value_counts()
df_incendios = pd.DataFrame({'Localidad': incendios_por_localidad.index, 'Número de Incendios': incendios_por_localidad.values})
# Definir una lista de colores para las barras
colores = ['Yellow', 'orange', 'red', 'purple', 'blue', 'green']  # Puedes agregar más colores si es necesario

figL = px.bar(df_incendios, x='Localidad', y='Número de Incendios', title='Número de Incendios por Localidad', color='Localidad', color_discrete_sequence=colores)

st.plotly_chart(figL)

###
st.markdown("<h6 style='text-align: center; color: #525252;'>Se observa que extrañamente la localidad de Canadá es la única con datos diferentes al resto de localidades, las cuales tienen un número similar de eventos correspondiente a 4440.</h2>", unsafe_allow_html=True)

#----------------------------------------
#9

st.markdown("<h5 style='text-align: center; color: #930000;'>Distribución de los incendios (residenciales/no residenciales)</h5>", unsafe_allow_html=True)

#count_fire = DESA[DESA['EVENT SUBGROUP'] == 'fire']['EVENT SUBGROUP'].value_counts()
#count_fire

event_types = DESA['EVENT SUBGROUP'].unique()

event_types = DESA['EVENT TYPE'].unique()

fire_rows = DESA[(DESA['EVENT TYPE'] == 'residential') & (DESA['EVENT SUBGROUP'] == 'fire')]

residenciales = DESA[DESA['EVENT TYPE'] == 'residential'][DESA['EVENT SUBGROUP'] == 'fire']
cantidad_residenciales = len(residenciales)
no_residenciales = DESA[DESA['EVENT TYPE'] == 'non-residential'][DESA['EVENT SUBGROUP'] != 'fire']
cantidad_no_residenciales = len(no_residenciales)
df_incendios = pd.DataFrame({'Tipo de Incendio': ['Residenciales', 'No Residenciales'], 'Cantidad': [cantidad_residenciales, cantidad_no_residenciales]})

figR = px.pie(df_incendios, values='Cantidad', names='Tipo de Incendio',
               width=400, height=400)

figR.update_layout(template = 'simple_white',
                  paper_bgcolor='rgba(0,0,0,0)',
                  plot_bgcolor='rgba(0,0,0,0)',
                  legend=dict(orientation="h",
                              yanchor="bottom",
                              y=-0.4,
                              xanchor="center",
                              x=0.5))



st.plotly_chart(figR)

###
st.markdown("<h6 style='text-align: center; color: #525252;'>Se tiene que los incendios no residenciales son los que más se presentan con un 53.9% en comparación con los incendios residenciales.</h6>", unsafe_allow_html=True)








#miremos esta bellecita

# Filtrar los datos por muertes relacionadas con incendios
filtro_incendios = MOR['Casualties'] == 'Fire-related deaths'
muertes_incendios = MOR[filtro_incendios]

# Agrupar por lugar (DGUID) y obtener la cantidad de muertes
muertes_por_lugar = muertes_incendios.groupby('DGUID').size().reset_index(name='Deaths')

# Crear el mapa
st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=pdk.ViewState(
        latitude=56.1304,
        longitude=-106.3468,
        zoom=3,
        pitch=0,
    ),
    layers=[
        pdk.Layer(
            'ScatterplotLayer',
            data=muertes_por_lugar,
            get_position=['COORDINATE'],
            get_radius=1000,
            get_fill_color=[255, 0, 0, 255],
            pickable=True,
        ),
    ],
))

ocurrencias_por_geo = MOR.groupby('GEO')['Casualties'].count().reset_index()

# Mostrar la tabla en Streamlit
st.table(ocurrencias_por_geo)
