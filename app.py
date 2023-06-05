# -*- coding: utf-8 -*-
"""Morales,_Moreno,_Lemus_Trabajo_Final_Segunda_Entrega_Analítica_1 (2).ipynb

FACULTAD DE INGENIERÍA<br>
DEPARTAMENTO DE INGENIERÍA INDUSTRIAL<br>
INTRODUCCIÓN A LA ANALÍTICA DE NEGOCIOS<br>
TRABAJO DEL CURSO - SEGUNDA ENTREGA: 15% <br>
Semestre 2023-01<br>

Equipo de trabajo: Aura Luz Moreno Díaz, Marcelo Lemus, Verónica Andrea Morales González

---
# **Carga de datos**

*Carga de las librerias necesarias para la ejecución del código. En este caso usaremos Pandas y Numpy renombrándolas como pd y np*
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



###Hemos montado los archivos de la base de datos a un hosting para poder trabajar los 3. Modificamos los permisos y se puede acceder a los datos desde cualquier lugar, de esta manera cualquier usuario puede ejecutar la BD desde cualquier parte."""

#Realizamos pruebas para verificar que haya conexión a la base de datos
AH  = pd.read_csv('https://www.4minds.solutions/tarea/final/BDALARMAHUMO.csv', sep=';',  low_memory=False) #Base de datos de Alarmas de Humo
MOR = pd.read_csv('https://www.4minds.solutions/tarea/final/BDMORTALIDAD.csv', sep=';',  low_memory=False) #Base de datos de Mortalidad
ROC = pd.read_csv('https://www.4minds.solutions/tarea/final/BDROCIADORES.csv', sep=';',  low_memory=False) #Base de datos de Rociadores
DES = pd.read_csv('https://www.4minds.solutions/tarea/final/BDGENERALDESASTRES.csv', sep=';',  low_memory=False) #Base de datos de Desastres en general

#Vemos los nombres de las columnas-variables de la base de alarma de humo y cantidad de datos de cada una.
AH.count()

#Vemos los nombres de las columnas-variables de la base de rociadores y cantidad de datos de cada una.
ROC.count()

#Vemos los nombres de las columnas-variables de la base de mortalidad y cantidad de datos de cada una.
MOR.count()

#Vemos los nombres de las columnas-variables de la base general de desastres.
DES.count()

#Se identifican columnas con nombres similares y otras relacionadas en las bases de mortalidad, rociadores y alarma de humo, por ejemplo **casualties** con **incidents** y **casualties**. Así como *Performance of sprinkler system*, *structural fires* y *Performance of smoke alarm device*, *residential fires*  que se refieren al funcionamiento del sistema como tal, por lo tanto se procede a unificar estas variables en las bases.

##Como la tabla general de desastres tiene unas variables totalmente diferentes, se procede a concatenar las otras tres tablas.

## Renombrar algunas columnas

#Antes de concatenar las bases, se renombran algunas columnas para que al concatenar, queden en la misma, dado que se refieren a una misma variable, pero en cada base tienen un nombre diferente.


MOR.rename(columns={'GEO':'GEO','Casualties':'Incidents&Casualties', 'REF_DATE':'YEAR'}, inplace=True)


ROC.rename(columns={'GEO':'GEO','Incidents and casualties':'Incidents&Casualties','Performance of sprinkler system, structural fires':'performance_of_system','REF_DATE':'YEAR'}, inplace=True)


AH.rename(columns={'GEO':'GEO','Incidents and casualties':'Incidents&Casualties','Performance of smoke alarm device, residential fires':'performance_of_system','REF_DATE':'YEAR'},inplace=True)


#DE la base de datos de desastres quitaremos los puntos para poder hacer bien los cálculos numéricos
DES['ESTIMATED TOTAL COST'] = DES['ESTIMATED TOTAL COST'].str.replace('.', '')


#DE la base de datos de desastres quitaremos los puntos para poder hacer bien los cálculos numéricos
DES['NORMALIZED TOTAL COST'] = DES['NORMALIZED TOTAL COST'].astype(str)
DES['NORMALIZED TOTAL COST'] = DES['NORMALIZED TOTAL COST'].str.replace('.', '')


## Concatenar bases

#Una vez renombradas, se procede a concatenar las tres bases con variables similares.


# concatenar las bases
CON = pd.concat([AH, MOR, ROC])


#Revisamos las variables de la nueva base


# **Depuración: Homologación de categorías, tipos de datos**
## A. Volver el nombre de las columnas a minúscula.
## usaremos la función lower para ponerlas todas en minúsculas


#Quitamos los espacios en blanco y pasamos a minusculas de la nueva tabla
CON['GEO'] = CON['GEO'].apply(lambda x: x.lower().strip() if pd.notnull(x) else x )
CON['performance_of_system'] = CON['performance_of_system'].apply(lambda x: x.lower().strip() if pd.notnull(x) else x )
CON['Incidents&Casualties'] = CON['Incidents&Casualties'].apply(lambda x: x.lower().strip() if pd.notnull(x) else x )
CON['Status of casualty'] = CON['Status of casualty'].apply(lambda x: x.lower().strip() if pd.notnull(x) else x )
CON['Type of structure'] = CON['Type of structure'].apply(lambda x: x.lower().strip() if pd.notnull(x) else x )

#Quitamos los espacios en blanco y pasamos a minusculas de la tabla general de desastres
DES['EVENT GROUP'] = DES['EVENT GROUP'].apply(lambda x: x.lower().strip() if pd.notnull(x) else x )
DES['EVENT SUBGROUP'] = DES['EVENT SUBGROUP'].apply(lambda x: x.lower().strip() if pd.notnull(x) else x )
DES['EVENT TYPE'] = DES['EVENT TYPE'].apply(lambda x: x.lower().strip() if pd.notnull(x) else x )
DES['PLACE'] = DES['PLACE'].apply(lambda x: x.lower().strip() if pd.notnull(x) else x )

# guardamos el df con las columnas definidas para ser analizadas de acuerdo con el contenido de las tres bases concatenadas.
CONS = CON.loc[:, ['YEAR', 'GEO', 'performance_of_system', 'Incidents&Casualties', 'VALUE', 'Status of casualty', 'Type of structure']]


# guardamos el df con las columnas definidas para ser analizadas de acuerdo con su contenido - para la base general de incendios
DESA = DES.loc[:, ['EVENT GROUP', 'EVENT SUBGROUP', 'EVENT TYPE', 'EVENT START DATE', 'FATALITIES', 'INJURED / INFECTED', 'ESTIMATED TOTAL COST', 'NORMALIZED TOTAL COST', 'MAGNITUDE', 'PLACE']]


## Homologación de categorías

# ver categorías de GEO con la frecuencia, en la base compilada CONS:
CONS['GEO'].value_counts()

#Encontramos que está Canadá y Fuerza armada Canadiense, por lo que se unen estas dos como Canadá.

# remplazar las categorías en GEO
CONS['GEO'] = CONS['GEO'].replace(['canadian armed forces'], 'canada')

# verificamos las categorías de GEO con la frecuencia:
CONS['GEO'].value_counts()

#ver categorías de performance_of_system con la frecuencia, en la base compilada CONS::
CONS['performance_of_system'].value_counts()

#No hay categorías que se repitan

# ver categorías de type of structure con la frecuencia, en la base compilada CONS:
CONS['Type of structure'].value_counts()

#No hay categorías que se repitan"""

# Revisamos ahora las categorías en la base general de desastres DESA, iniciamos con EVENT GROUP
DESA['EVENT GROUP'].value_counts()

#Se tienen algunos datos sin sentido como las categorías 0, 1, 2, 47 y 93, por lo tanto se procede a cambiarlas y ponerlas como SIN que significa sin información."""

# reemplazar las categorías en EVENT GROUP
DESA['EVENT GROUP'] = DESA['EVENT GROUP'].replace(['0', '1', '2', '47', '93'], 'SIN')

# Revisamos ahora la categoría EVENT SUBGROUP
DESA['EVENT SUBGROUP'].value_counts()

#Se tienen algunos datos sin sentido como las categorías 0, 25, 45, 6, por lo tanto se procede a cambiarlas y ponerlas como s.i. que significa sin información. Y se tiene la categoría fire y arson que se refieren a fuego, por lo cual se reunen en una como fire.  Se tiene también civil incident y hijacking que traduce secuestro, por lo que puede estar dentro de la categoría de incidente civil.

# remplazar las categorías en EVENT SUBGROUP
DESA['EVENT SUBGROUP'] = DESA['EVENT SUBGROUP'].replace(['0', '25', '45', '6'], 'SIN')
DESA['EVENT SUBGROUP'] = DESA['EVENT SUBGROUP'].replace(['arson'], 'fire')
DESA['EVENT SUBGROUP'] = DESA['EVENT SUBGROUP'].replace(['hijacking'], 'civil incident')


#Se tienen algunos datos sin sentido como las categorías 3000, 10000, 1400, 4900, 3200, 65000, 500, 560, 0 Y 2000 por lo tanto se procede a cambiarlas y ponerlas como s.i. que significa sin información.

#Se tienen las categorías storms and severe thunderstorms, winter storm, hurricane / typhoon / tropical storm, storm - unspecified / other, geomagnetic storm que se refieren a tormentas, por lo cual se reunen en una como storm.

#Se tienen las categorías air, tornado, que se reunen en una como air.
#Se tienen las categorías wildfire, fire, que se reunen en una como fire.
#Se tienen las categorías vehicle, vehicle release, transportation que se reunen en una como vehicle.
#Se tienen las categorías rioting, disturbance / demonstrations que se reunen en una como disturbance / demonstrations.
#Se tienen las categorías pandemic, infestation, epidemic que se reunen en una como infestation/epidemic/pandemic.

# remplazar las categorías en EVENT TYPE
DESA['EVENT TYPE'] = DESA['EVENT TYPE'].replace(['3000', '10000', '1400', '4900', '3200', '65000', '500', '560', '0', '2000'], 'SIN')
DESA['EVENT TYPE'] = DESA['EVENT TYPE'].replace(['storms and severe thunderstorms', 'winter storm', 'hurricane / typhoon / tropical storm', 'storm - unspecified / other', 'geomagnetic storm'], 'storm')
DESA['EVENT TYPE'] = DESA['EVENT TYPE'].replace(['tornado'], 'air')
DESA['EVENT TYPE'] = DESA['EVENT TYPE'].replace(['wildfire'], 'fire')
DESA['EVENT TYPE'] = DESA['EVENT TYPE'].replace(['heat event','drought' ], 'head event/drought')
DESA['EVENT TYPE'] = DESA['EVENT TYPE'].replace(['vehicle','vehicle release', 'transportation'], 'vehicle')
DESA['EVENT TYPE'] = DESA['EVENT TYPE'].replace(['rioting'], 'disturbance / demonstrations')
DESA['EVENT TYPE'] = DESA['EVENT TYPE'].replace(['pandemic', 'infestation', 'epidemic'], 'infestation/epidemic/pandemic')

#Tratamiento de datos nulos

#Para performance_of_system, value, status of casualty y type of structure agruparemos los nulos en "n.i." que significa que no hay información para que queden allá todos los no identificados
CONS['performance_of_system'] = CONS['performance_of_system'].fillna('SIN')
CONS['VALUE'] = CONS['VALUE'].fillna('SIN')
CONS['Status of casualty'] = CONS['Status of casualty'].fillna('SIN')
CONS['Type of structure'] = CONS['Type of structure'].fillna('SIN')

#Se encuentran datos nulos en todas las columnas, los cuales se reemplazarán por n.i. que significa que no hay información."""

DESA['EVENT GROUP'] = DESA['EVENT GROUP'].fillna('SIN')
DESA['EVENT SUBGROUP'] = DESA['EVENT SUBGROUP'].fillna('SIN')
DESA['EVENT TYPE'] = DESA['EVENT TYPE'].fillna('SIN')
DESA['EVENT START DATE'] = DESA['EVENT START DATE'].fillna('SIN')
DESA['FATALITIES'] = DESA['FATALITIES'].fillna('SIN')
DESA['INJURED / INFECTED'] = DESA['INJURED / INFECTED'].fillna('SIN')
DESA['MAGNITUDE'] = DESA['MAGNITUDE'].fillna('SIN')

# **Generación de bodegas de datos**


#Una vez depuradas las bases tenemos las siguientes dos bodegas de datos

# **Transformaciones: Aplicación de funciones para la creación de nuevas variables**

#Aquí ponemos extraer el año, creando una nueva variable en la base "DESA" con la variable EVENT START DATE

#Convertimos la columna "EVENT START DATE" a formato de datetime
DESA['EVENT START DATE']=pd.to_datetime(DESA['EVENT START DATE'],errors='coerce')

# Creamos las nuevas variables YEAR , MONTH , DAY 
DESA.insert(0,'YEAR', DESA.loc[DESA['EVENT START DATE'].notnull(), 'EVENT START DATE'].dt.year)
DESA.insert(1,'MONTH', DESA.loc[DESA['EVENT START DATE'].notnull(), 'EVENT START DATE'].dt.month)
DESA.insert(2,'DAY', DESA.loc[DESA['EVENT START DATE'].notnull(), 'EVENT START DATE'].dt.day)

#Las columnas YEAR , MONTH , DAY quedaron como flotantes, por haber valores null en las fechas. Convertimos los valores null de estos nuevos campos al valor entero 0.
DESA['YEAR']=DESA['YEAR'].fillna(0).astype(int)
DESA['MONTH']=DESA['MONTH'].fillna(0).astype(int)
DESA['DAY']=DESA['DAY'].fillna(0).astype(int)

#Ahora convertimos los campos a valor entero.
DESA['YEAR']=DESA['YEAR'].astype(int)
DESA['MONTH']=DESA['MONTH'].astype(int)
DESA['DAY']=DESA['DAY'].astype(int)

#Queremos que en el campo MONTH aparezca el nombre del mes y no un numero entero. 
import calendar
DESA['MONTH'] = DESA['MONTH'].apply(lambda x: calendar.month_abbr[x] if x != 0 else '')

#EVENT START DATE contiene valores nulos, ya que fue una columna que fue desglosada, procedemos a eliminarla.
DESA = DESA.drop('EVENT START DATE', axis=1)

### HASTA AQUÍ TODA LA PARTE DE LIMPIEZA Y TRANSFORMACIÓN DE LOS DATOS














#INICIAMOS CON LOS ENCABEZADOS
st.set_page_config(layout="wide")

st.markdown("<h5 style='text-align: center; color: #50668a;'>UNIVERSIDAD DE ANTIOQUIA <br> FACULTAD DE INGENIERÍA <br> DEPARTAMENTO DE INGENIERÍA INDUSTRIAL <br> INTRODUCCIÓN A LA ANALÍTICA DE NEGOCIOS</h5>", unsafe_allow_html=True)

st.markdown("<h6 style='text-align: center; color: #50668a;'>Equipo de trabajo: Aura Luz Moreno Díaz, Marcelo Lemus, Verónica Andrea Morales González</h6>", unsafe_allow_html=True)
st.markdown("<h6 style='text-align: center; color: #50668a;'>Semestre: 2023-1</h6>", unsafe_allow_html=True)

# Ruta de la imagen
image_path = "canada.jpg"

html_code = f"""
<div style="display: flex; justify-content: center;">
    <img src="data:image/jpeg;base64,{base64.b64encode(open(image_path, "rb").read()).decode()}">
</div>
"""
st.markdown(html_code, unsafe_allow_html=True)

# Título principal, h1 denota el estilo del título 1
st.markdown("<h1 style='text-align: center; color: #0066FF; font-family: system-ui; margin-top: 20px;'>Eficacia de los sistemas de incendio en Canadá</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #666666;'>Comparativo entre aspersores y alarmas de humo</h2>", unsafe_allow_html=True)

#1
###
#Se revisa a nivel general, cómo es la distribución de la cantidad de desastres por cada tipo y cuál es el que tiene mayor ocurrencia en el periodo.
st.markdown("<h6 style='text-align: center; color: #525252;'>Existe una gran cantidad de tipos de desastres, cuando se mira por la cantidad de ocurrencias, se tiene que el desastre de mayor ocurrencia es el de inundaciones, en segundo lugar las tormentas y en tercer lugar los incendios, por lo tanto hacer énfases en estos tipos de desastres vale la pena.</h6>", unsafe_allow_html=True)

desastre=DESA['EVENT TYPE'].value_counts()
desastre_df = pd.DataFrame({'EVENT TYPE': desastre.index, 'Cantidad desastres': desastre.values})
figd = px.bar(desastre_df, x='EVENT TYPE', y='Cantidad desastres', labels={'EVENT TYPE': 'Tipo de desastre', 'desastre_df': 'Tipo de desastre'})

st.plotly_chart(figd)

# AGREGAMOS UNA IMAGEN
imageI= "inundaciones.jpg"

st.image(imageI, caption="Inundaciones. Tomado de: https://media.istockphoto.com/id/1356603199/es/foto/inundaci%C3%B3n-y-humo-negro-del-fuego-en-la-ciudad-y-las-tierras-de-cultivo-despu%C3%A9s-de-la-tormenta.jpg?s=612x612&w=0&k=20&c=Ep9sSC__XJVVePWa1eXCU7fyVLGjb8qBZVO2nuZ1mGc=", width=None, use_column_width=150, clamp=False, channels="RGB", output_format="auto")



#2
st.markdown("<h2 style='text-align: center; color: #930000;'>Cantidad de muertes generadas por los tres principales tipos de desastre</h2>", unsafe_allow_html=True)


import pandas as pd
import numpy as np

#Convertimos a tipo string y removemos separador de miles y la convertimos a tipo numerico haciendo coerción en los errores para que los valores no numéricos se conviertan en NaN.
DESA['NORMALIZED TOTAL COST'] = DESA['NORMALIZED TOTAL COST'].astype(str)
DESA['NORMALIZED TOTAL COST'] = DESA['NORMALIZED TOTAL COST'].str.replace('.', '')
DESA['NORMALIZED TOTAL COST'] = pd.to_numeric(DESA['NORMALIZED TOTAL COST'], errors='coerce')
eventos = ['fire', 'storm', 'flood']
filtro_eventos = DESA['EVENT TYPE'].isin(eventos)
datos_filtrados = DESA[filtro_eventos]
muertes = datos_filtrados.groupby('EVENT TYPE')['FATALITIES'].sum().reset_index()
df_muertes = pd.DataFrame({'Tipo de evento': muertes['EVENT TYPE'], 'Cantidad de muertes': muertes['FATALITIES']})
fig = px.bar(df_muertes, x='Tipo de evento', y='Cantidad de muertes',labels={'Tipo de evento': 'Tipo de evento', 'Cantidad de muertes': 'Cantidad de muertes'},title='Cantidad de muertes por tipo de evento')
st.plotly_chart(fig)


###
st.markdown("<h6 style='text-align: center; color: #525252;'>Se tiene como resultado que las tormentas son las que tienen mayor número de muertes con 1725 casos, luego sigue incendios con 388 casos y finalmente las inundaciones a pesar de que tienen mayor ocurrencia como se vio anteriormente, tienen la menor cantidad de muertes en estos tres tipos de desastre con 124 casos.</h2>", unsafe_allow_html=True)

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

#10

c4, c5= st.columns((1,1))

c4.markdown("<h5 style='text-align: center; color: #930000;'>Porcentaje de incendios en los que funcionaron efectivamente los rociadores</h5>", unsafe_allow_html=True)

conteo_eventos = ROC['performance_of_system'].value_counts()

conteo_performance = ROC['performance_of_system'].value_counts()
incendios_con_rociadores = conteo_performance['Sprinkler operated']
total_incendios = ROC.shape[0]
porcentaje_efectividad = (incendios_con_rociadores / total_incendios) * 100

conteo_performance = ROC['performance_of_system'].value_counts()
incendios_con_rociadores = conteo_performance['Sprinkler operated']
incendios_sin_rociadores = total_incendios - incendios_con_rociadores
data = {'Resultado': ['No funcionaron', 'Si funcionaron'],'Cantidad': [incendios_con_rociadores, incendios_sin_rociadores]}

df = pd.DataFrame(data)

figrr = px.pie(df, values='Cantidad', names='Resultado',
               width=280, height=280)

figrr.update_layout(template = 'simple_white',
                  paper_bgcolor='rgba(0,0,0,0)',
                  plot_bgcolor='rgba(0,0,0,0)',
                  legend=dict(orientation="h",
                              yanchor="bottom",
                              y=-0.4,
                              xanchor="center",
                              x=0.5))




c4.plotly_chart(figrr)


###
c4.markdown("<h6 style='text-align: center; color: #525252;'>El porcentaje o tasa de efectividad  de funcionamiento de los rociadores es del 20%.</h6>", unsafe_allow_html=True)



#11

c5.markdown("<h5 style='text-align: center; color: #930000;'>Porcentaje de incendios en los que funcionaron efectivamente  las alarmas de humo</h5>", unsafe_allow_html=True)

conteo_eventos = AH['performance_of_system'].value_counts()
conteo_performance = AH['performance_of_system'].value_counts()
incendios_con_alarma = conteo_performance['Alarm activated']
incendios_sin_alarma = total_incendios - incendios_con_alarma
data = {'Resultado': ['Alarmas Activadas', 'Alarmas No Activadas'],'Cantidad': [incendios_con_alarma, incendios_sin_alarma]}

df = pd.DataFrame(data)

figah = px.pie(df, values='Cantidad', names='Resultado',
               width=280, height=280)

figah.update_layout(template = 'simple_white',
                  paper_bgcolor='rgba(0,0,0,0)',
                  plot_bgcolor='rgba(0,0,0,0)',
                  legend=dict(orientation="h",
                              yanchor="bottom",
                              y=-0.4,
                              xanchor="center",
                              x=0.5))

#enviar a streamlit
c5.plotly_chart(figah)

###
c5.markdown("<h6 style='text-align: center; color: #525252;'>El porcentaje o tasa de efectividad  de funcionamiento de las alarmas de humo es del 20%.</h6>", unsafe_allow_html=True)
