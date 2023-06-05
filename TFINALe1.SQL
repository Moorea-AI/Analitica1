/* 
***************************************************************************
TRABAJO FINAL ANALITICA 1 -  Moreno Aura, Morales Verónica, Lemus Marcelo
PREGUNTA 1

¿Cuál es el número de desastres ocurridos por año y tipo de desastre? 

Para esta pregunta, la base de datos NO traia el tipo de dato TimeStamp 
sino como un string, tuvimos que convertir el supuesto TimeStamp en string 
para extraer los datos que estaban después del segundo "/" que correspondia 
al año y luego quitar los datos nulos, vacios o que no crrespondian al año. 
Y luego, filtrado por todos los menores al año actual (por posibles errores 
de digitación)
***************************************************************************
*/

SELECT count(EVENT_CATEGORY) as Cantidad, EVENT_TYPE as Desastre, REGEXP_EXTRACT(SUBSTR(EVENT_START_DATE, INSTR(EVENT_START_DATE, '/', INSTR(EVENT_START_DATE, '/') + 1) + 1), r'\d{4}') as FECHA
FROM `trabajofinalanalitica-380822.BDMORTALIDAD.TCDD`

WHERE CAST(REGEXP_EXTRACT(SUBSTR(EVENT_START_DATE, INSTR(EVENT_START_DATE, '/', INSTR(EVENT_START_DATE, '/') + 1) + 1), r'\d{4}') AS INT64) < EXTRACT(YEAR FROM CURRENT_DATE())

group by desastre, FECHA
order by Cantidad DESC


/* 
***************************************************************************
TRABAJO FINAL ANALITICA 1 -  Moreno Aura, Morales Verónica, Lemus Marcelo
PREGUNTA 2

¿Cuál es la tasa de mortalidad de los incendios? total de incendios con 
muertos/ Total de incendios 

Para esta pregunta, tomamos el total de incidentes con muertes dividido el 
total de filas con el condicional de que el tipo de incidente fuera 
incendios. Como la pregunta era una TASA, lo convertimos a porcentaje 
multiplicando * 100 y agregando dos decimales.
***************************************************************************
*/

SELECT CONCAT(ROUND(COUNTIF(FATALITIES >= 1) / NULLIF(COUNT(*), 0) * 100, 2), '%') as TASAMORTALIDAD  
FROM `trabajofinalanalitica-380822.BDMORTALIDAD.TCDD`
WHERE UPPER(EVENT_SUBGROUP)="FIRE"

/* 
***************************************************************************
TRABAJO FINAL ANALITICA 1 -  Moreno Aura, Morales Verónica, Lemus Marcelo
PREGUNTA 3

¿Cuál es el porcentaje de incendios en los que funcionaron efectivamente 
los aspersores? Total de incendios apagados por aspersores/total de incendios 

La tasa de efectividad la obtenemos cuando el campo indica que los 
aspersores funcionaron, es decir: "sprinkler operated", entonces tomamos
los campos que tienen esa frase y lo dividimos sobre el total de filas.
Como nos están pidiendo una tasa, entonces lo multipliacamos *100
***************************************************************************
*/

SELECT CONCAT(ROUND(COUNTIF(Performance_of_sprinkler_system__structural_fires = 'Sprinkler operated') / COUNT(*) * 100, 2), '%') as TASAEFECTIVIDAD
FROM `trabajofinalanalitica-380822.BDMORTALIDAD.TSPRINKLER`

/* 
***************************************************************************
TRABAJO FINAL ANALITICA 1 -  Moreno Aura, Morales Verónica, Lemus Marcelo
PREGUNTA 04

Cuál es la cantidad de incendios por año? 

Para esta pregunta, se toma la cantidad y el año, filtrado por "fire".
***************************************************************************
*/

SELECT count(EVENT_CATEGORY) as Cantidad, REGEXP_EXTRACT(SUBSTR(EVENT_START_DATE, INSTR(EVENT_START_DATE, '/', INSTR(EVENT_START_DATE, '/') + 1) + 1), r'\d{4}') as FECHA
FROM `trabajofinalanalitica-380822.BDMORTALIDAD.TCDD`

WHERE CAST(REGEXP_EXTRACT(SUBSTR(EVENT_START_DATE, INSTR(EVENT_START_DATE, '/', INSTR(EVENT_START_DATE, '/') + 1) + 1), r'\d{4}') AS INT64) < EXTRACT(YEAR FROM CURRENT_DATE()) 
AND UPPER(EVENT_TYPE) =  "FIRE"

group by FECHA
order by Cantidad DESC

/* 
***************************************************************************
TRABAJO FINAL ANALITICA 1 -  Moreno Aura, Morales Verónica, Lemus Marcelo
PREGUNTA 05

Cuál es el TOTAL de incendios estructurales?

Para esto se toma todos los campos que coincidan con "structural" en la
columna "Type_of_Structure" asi sabemos cuales son estructurales y cuales
no.
***************************************************************************
*/
SELECT  COUNTIF(contains_substr(UPPER(Type_of_structure), 'structural')) as Estructurales,
COUNTIF(UPPER(Type_of_structure) NOT LIKE '%structural%') as NoEstructurales
FROM `trabajofinalanalitica-380822.BDMORTALIDAD.TMORTALIDAD`

/* 
***************************************************************************
TRABAJO FINAL ANALITICA 1 -  Moreno Aura, Morales Verónica, Lemus Marcelo
PREGUNTA 06

Qué dia de la semana hay mayor ocurrencia de incendios? 

Para esto primero organizamos la fecha, ya que el tiempo no está biien 
estructurado como dat fecha, por ende hay que extraerlo y limpiar la
fecha. Luego de esto, concatenamos y sacamos el dia de la semana
***************************************************************************
*/



SELECT 
UPPER(FORMAT_DATE('%A', PARSE_DATE('%m/%d/%Y',CONCAT(FORMAT_DATE('%m', PARSE_TIMESTAMP('%m/%d/%Y %I:%M:%S %p', EVENT_START_DATE)),'/',FORMAT_DATE('%d', PARSE_TIMESTAMP('%m/%d/%Y %I:%M:%S %p', EVENT_START_DATE)),'/',FORMAT_DATE('%Y', PARSE_TIMESTAMP('%m/%d/%Y %I:%M:%S %p', EVENT_START_DATE)))))) AS DIA, COUNT(*) as ocurrencias

FROM `trabajofinalanalitica-380822.BDMORTALIDAD.TCDD`    

WHERE 
EVENT_START_DATE IS NOT NULL AND
SAFE.PARSE_TIMESTAMP('%m/%d/%Y %I:%M:%S %p', EVENT_START_DATE) IS NOT NULL 

GROUP BY 
DIA
ORDER BY 
  COUNT(*) DESC; 

/* 
***************************************************************************
TRABAJO FINAL ANALITICA 1 -  Moreno Aura, Morales Verónica, Lemus Marcelo
PREGUNTA 07

¿Cuál es la localidad con mayor numero de desastres naturales? 

Para esta consulta se suma la cantidad de incendios por cada Localidad y se ordena de mayor a menor. Se visualiza solo el primer resultado. 
***************************************************************************
*/
--select MAX (Total_incendios) as Max_Incendios
--from ( 
  
  /*select PLACE as Localidad, count(*) as Total_desastres
  from `trabajofinalanalitica-380822.BDMORTALIDAD.TCDD`
  where EVENT_CATEGORY = "Disaster" AND EVENT_GROUP = "Natural" 
  group by Localidad
  order by Total_desastres desc
  Limit 1
*/
SELECT Localidad, total_incendios
FROM (
  SELECT PLACE as Localidad, COUNT(*) AS total_incendios
  FROM `trabajofinalanalitica-380822.BDMORTALIDAD.TCDD`
  WHERE EVENT_CATEGORY = "Disaster" AND EVENT_GROUP = "Natural" 
  GROUP BY Localidad
) t1
WHERE total_incendios = (
  SELECT MAX(total_incendios) AS max_total_incendios
  FROM (
    SELECT PLACE AS Localidad, COUNT(*) AS total_incendios
    FROM `trabajofinalanalitica-380822.BDMORTALIDAD.TCDD`
    WHERE EVENT_CATEGORY = "Disaster" AND EVENT_GROUP = "Natural"
    GROUP BY Localidad
  ) t2
) 


/* 
***************************************************************************
TRABAJO FINAL ANALITICA 1 -  Moreno Aura, Morales Verónica, Lemus Marcelo
PREGUNTA 08

¿Cuál se el nuemro de muertos y heridos promedio por evento? 

Para estra consulta se promedian las muertes y heridos agrupando por Grupo de Desastre y tipo de desastre. 
***************************************************************************
*/

SELECT EVENT_SUBGROUP AS Grupo_Desastre, EVENT_TYPE as Tipo_Desastre,  IFNULL(cast(avg(FATALITIES) as integer ),0) as Muertes_Promedio, IFNULL(cast(avg(INJURED___INFECTED) as integer ),0) as Heridos_Promedio 
FROM `trabajofinalanalitica-380822.BDMORTALIDAD.TCDD`
group by Grupo_Desastre, Tipo_Desastre 


/* 
***************************************************************************
TRABAJO FINAL ANALITICA 1 -  Moreno Aura, Morales Verónica, Lemus Marcelo
PREGUNTA 09

¿Cuál es el número de muertes por año en donde la causa haya sido incendio?

Para esto primero organizamos la fecha, ya que el tiempo no está biien 
estructurado como dato fecha, por ende hay que extraerlo y limpiar la
fecha. Luego de esto, concatenamos y sacamos el año y el número de ocurrencias
por cada año y se suman.
***************************************************************************
*/


SELECT 
EXTRACT(YEAR FROM (PARSE_DATE('%m/%d/%Y',CONCAT(FORMAT_DATE('%m', PARSE_TIMESTAMP('%m/%d/%Y %I:%M:%S %p', EVENT_START_DATE)),'/',FORMAT_DATE('%d', PARSE_TIMESTAMP('%m/%d/%Y %I:%M:%S %p', EVENT_START_DATE)),'/',FORMAT_DATE('%Y', PARSE_TIMESTAMP('%m/%d/%Y %I:%M:%S %p', EVENT_START_DATE)))))) AS YEAR, SUM(FATALITIES) AS MUERTES

FROM `trabajofinalanalitica-380822.BDMORTALIDAD.TCDD`

WHERE EVENT_START_DATE IS NOT NULL AND
SAFE.PARSE_TIMESTAMP('%m/%d/%Y %I:%M:%S %p', EVENT_START_DATE) IS NOT NULL AND
UPPER(EVENT_SUBGROUP)="FIRE" AND CAST(FATALITIES AS NUMERIC)>0 

GROUP BY YEAR

ORDER BY YEAR ASC

/* 
***************************************************************************
TRABAJO FINAL ANALITICA 1 -  Moreno Aura, Morales Verónica, Lemus Marcelo
PREGUNTA 10

¿Cuá se el promedio de fallecimientos por lugar? 

Se calcula el promedio de muertes-fallecimientos y se agrupa por lugar. Se redonda por tratarse de muertes , cantidad discreta.
***************************************************************************
*/

Select PLACE as Localidad , ifnull(cast(avg(Fatalities) AS INTEGER),0) as Promedio_muertes 
from  `trabajofinalanalitica-380822.BDMORTALIDAD.TCDD`
group by Localidad


/*
*************************************************************************** 
TRABAJO FINAL ANALITICA 1 -  Moreno Aura, Morales Verónica, Lemus Marcelo 
PREGUNTA 11 
¿Cuál es el porcentaje de incendios estructurales en los que funcionaron efectivamente los aspersores por ciudad?  
*************************************************************************** 
*/

SELECT GEO as CIUDAD, CONCAT(ROUND((COUNTIF(Performance_of_sprinkler_system__structural_fires = 'Sprinkler operated' AND  Incidents_and_casualties='Fire incidents, structural' ) / COUNT(*)) * 100, 2), '%') as TASAEFECTIVIDAD 

FROM `trabajofinalanalitica-380822.BDMORTALIDAD.TSPRINKLER` 

GROUP BY GEO


/* 
***************************************************************************
TRABAJO FINAL ANALITICA 1 -  Moreno Aura, Morales Verónica, Lemus Marcelo
PREGUNTA 12

¿Cuántos muertos hay en incendios residenciales al año? 

Se ordena por el año en que hubo más muertes en residencias. 

***************************************************************************
*/


SELECT 
EXTRACT(YEAR FROM (PARSE_DATE('%m/%d/%Y',CONCAT(FORMAT_DATE('%m', PARSE_TIMESTAMP('%m/%d/%Y %I:%M:%S %p', EVENT_START_DATE)),'/',FORMAT_DATE('%d', PARSE_TIMESTAMP('%m/%d/%Y %I:%M:%S %p', EVENT_START_DATE)),'/',FORMAT_DATE('%Y', PARSE_TIMESTAMP('%m/%d/%Y %I:%M:%S %p', EVENT_START_DATE)))))) AS YEAR, SUM(FATALITIES) AS MUERTES, EVENT_TYPE

FROM `trabajofinalanalitica-380822.BDMORTALIDAD.TCDD`

WHERE EVENT_START_DATE IS NOT NULL AND
SAFE.PARSE_TIMESTAMP('%m/%d/%Y %I:%M:%S %p', EVENT_START_DATE) IS NOT NULL AND
UPPER(EVENT_SUBGROUP)="FIRE" AND CAST(FATALITIES AS NUMERIC)>0 
AND UPPER(EVENT_TYPE)="RESIDENTIAL"

GROUP BY YEAR, EVENT_TYPE

ORDER BY MUERTES DESC


/* 
***************************************************************************
TRABAJO FINAL ANALITICA 1 -  Moreno Aura, Morales Verónica, Lemus Marcelo
PREGUNTA 13

¿Cuántos AFECTADOS hay en incendios POR TIPO DE CONSTRUCCION al año ? 

Se ordena por el total de afectados
***************************************************************************
*/

SELECT REF_DATE, Type_of_structure, sum(VALUE) as TOTAL_AFECTADOS
FROM `trabajofinalanalitica-380822.BDMORTALIDAD.TMORTALIDAD`
WHERE Casualties="Fire-related deaths"
GROUP BY Type_of_structure, REF_DATE, Casualties
order by TOTAL_AFECTADOS DESC

/*
*************************************************************************** 

TRABAJO FINAL ANALITICA 1 - Moreno Aura, Morales Verónica, Lemus Marcelo 

PREGUNTA 14 

¿Cuál es el máximo y el mínimo número de evacuados por grupo de evento?? 

*************************************************************************** 
*/

SELECT EVENT_GROUP, MAX(EVACUATED) AS Maximo_n_evacuados, MIN(EVACUATED) as Minimo_n_evacuados 

FROM `BDMORTALIDAD.TCDD` 

WHERE EVENT_GROUP IS NOT NULL 

GROUP BY EVENT_GROUP 

/*
*************************************************************************** 
TRABAJO FINAL ANALITICA 1 - Moreno Aura, Morales Verónica, Lemus Marcelo 
PREGUNTA 15 
¿Cuál es el promedio de heridos por subgrupo de evento? 
*************************************************************************** 
*/

SELECT EVENT_SUBGROUP, AVG(INJURED___INFECTED) AS Promedio_Heridos_afectados
FROM `BDMORTALIDAD.TCDD`
WHERE EVENT_SUBGROUP IS NOT NULL AND INJURED___INFECTED IS NOT NULL
GROUP BY EVENT_SUBGROUP

/*
*************************************************************************** 
TRABAJO FINAL ANALITICA 1 - Moreno Aura, Morales Verónica, Lemus Marcelo 
PREGUNTA 16 
¿Que porcentaje de incendios hay con respecto al total de desastres a nivel
general? 
*************************************************************************** 
*/

SELECT CONCAT(ROUND(COUNTIF(EVENT_TYPE = 'Fire' OR EVENT_TYPE= 'Wildfire') / COUNT(*) * 100, 2), '%') as PORCENTAJE_DESASTRESporINCENDIOS 
FROM `BDMORTALIDAD.TCDD`

/* 
***************************************************************************
TRABAJO FINAL ANALITICA 1 -  Moreno Aura, Morales Verónica, Lemus Marcelo
PREGUNTA 17

¿Cuál es el lugar con mayor número de desastres?
  
En este caso pueden haber varios lugares con igual numero de desastres,
sin embargo se presenta un listado descendente y se limita al primero 
para obtener el que tenga mayor numero de ocurrencias.
***************************************************************************
*/

SELECT PLACE as LUGAR, count(*) as OCURRENCIAS  
FROM `trabajofinalanalitica-380822.BDMORTALIDAD.TCDD`
GROUP BY PLACE
ORDER BY OCURRENCIAS desc
limit 1

/* 
***************************************************************************
TRABAJO FINAL ANALITICA 1 -  Moreno Aura, Morales Verónica, Lemus Marcelo
PREGUNTA 18

¿Cuántos bomberos heridos hay en incendios no-residenciales por año?

***************************************************************************
*/

SELECT REF_DATE, Type_of_structure, sum(VALUE) as TOTAL_AFECTADOS
FROM `trabajofinalanalitica-380822.BDMORTALIDAD.TMORTALIDAD`
WHERE Casualties="Fire-related injuries" AND Status_of_casualty="Firefighter" AND Type_of_structure !="Residential fires"
GROUP BY REF_DATE, Type_of_structure, Casualties
order by REF_DATE DESC

/* 
***************************************************************************
TRABAJO FINAL ANALITICA 1 -  Moreno Aura, Morales Verónica, Lemus Marcelo
PREGUNTA 19

¿Cuál es el costo promedio de la normalización por evento?   
  
En esta pregunta se hace una consulta promediando el costo total normalizdo 
por categoria de desastre y tipo de desastre. Se agrupa por categoria y 
tipo de desastre. Se redondea a 2 cifras decimales y se ordena en forma descendente por Costo_promedio. Los resultados null en el Costo_promedio se convieten a 0.0

***************************************************************************
*/

SELECT IFNULL(round(avg(NORMALIZED_TOTAL_COST),2),0)  as Costo_promedio, EVENT_CATEGORY AS Desastre, EVENT_TYPE as Tipo_Desastre  
FROM `trabajofinalanalitica-380822.BDMORTALIDAD.TCDD`
group by Desastre, Tipo_Desastre 
order by Costo_promedio desc
/* 
***************************************************************************
TRABAJO FINAL ANALITICA 1 -  Moreno Aura, Morales Verónica, Lemus Marcelo
PREGUNTA 20

¿Cuál es la cantidad promedio de personas evacuadas por desastre?   
  
En esta pregunta se hace una consulta promediando las personas evacuadas 
por categoria de desastre y tipo de desastre. Se agrupa por categoria y 
tipo de desastre. Se redonde a cero cifras decimales (entero) pues se trata 
de personas evacuadas.  

***************************************************************************
*/ 

SELECT ifnull(cast(avg(EVACUATED) AS INTEGER),0)  as Promedio_evacuados, EVENT_CATEGORY AS Desastre, EVENT_TYPE as Tipo_Desastre  
FROM `trabajofinalanalitica-380822.BDMORTALIDAD.TCDD`


group by Desastre, Tipo_Desastre 



-- PREGUNTA 21 :
-- ¿Qué localidad ha tenido desastres tipo incendio ya sea por falla o no de sistemas de aspersores en cualquier tipo de estructura?
-- Esta consulta equvalle a mostrar cuales son las ciudades en comun en las tres base de datos. 

-- Creamos primero un catalogo de localidades unico desde la tabla general de desastres, la cual llamamo t1. Enseguida creamos una tabla de las localidades unicas de la tabla de sistemas de rociadores , seguida de la tabla de localidades unicas de la base de datos de muertes por incendiso segun tipo de estructura. Con un inner join unimos las tablas por la ciudad que se repite en todas y listamos dichas ciudades. 


with t1 as (select PLACE as ciudades from `BDMORTALIDAD.TCDD`  
group by ciudades
),

 t2 as ( 
  select GEO as ciudades from `BDMORTALIDAD.TSPRINKLER`
  group by ciudades
),

t3 as (
  select GEO as ciudades from `BDMORTALIDAD.TMORTALIDAD`
  group by ciudades
)

select t1.ciudades 
from t1 
inner join t2 on t1.ciudades=t2.ciudades
inner join t3 on t2.ciudades=t3.ciudades

-- PREGUNTA 22
--¿Entre todos los desastres registrados , cual fue la cantidad  total de ellos, la cantidad debido a mal funcionamiento de sistemas aspersores donde hubo muertes y  cual fue la proporcion de estos incidentes que corresponden a falla en aspersores (no funcionando) por año y localidad?

-- Para resolver esta pregunta , contamos por año y ciudad todos los incidentes de incendios en la tabla general de desastres. Luego contampos por año y localidad, todos los incidentes de incendios debidos a fallas en el sistema de aspersores (no funcionando). Con esto tenemos registros unicos en cada tabla temporal. Ensegudia creamos una consulta, donde listamos la proporcion requerida , dividiendo la cantidad de la segunda tabla entre la cantidad de la primera tabla, por año y localidad. 

with t1 as (
  select ifnull(sum (fatalities),0) as Cantidad, (CAST(FORMAT_DATE('%Y', PARSE_TIMESTAMP('%m/%d/%Y %I:%M:%S %p', EVENT_START_DATE)) AS STRING )) AS YEAR, PLACE AS Localidad 

  FROM `BDMORTALIDAD.TCDD`
  WHERE  
  EVENT_START_DATE IS NOT NULL
  AND SAFE.PARSE_TIMESTAMP('%m/%d/%Y %I:%M:%S %p', EVENT_START_DATE) IS NOT NULL
  GROUP BY YEAR , Localidad
  ORDER BY YEAR
), 

t2 as (
  select ifnull(sum(VALUE),0) AS Cantidad,CAST(REF_DATE AS STRING ) as year, GEO as Lugar 
  from `BDMORTALIDAD.TSPRINKLER`
  WHERE Performance_of_sprinkler_system__structural_fires="Sprinkler did not operate" AND Incidents_and_casualties="Fire-related deaths, structural"
  Group by year , Lugar
  ORDER BY year desc
  
)

select t1.YEAR as Year, t1.Localidad as Localidad, t1.Cantidad as Incendios_G, t2.Cantidad as Incendios_R, CONCAT((t2.Cantidad/ t1.Cantidad)*100,"%") as Proporcion
from t1 inner join t2 on t1.YEAR=t2.year
WHERE NULLIF(t1.Cantidad,0) is not null 
group by Year, Localidad,Incendios_G , Incendios_R
order by t1.YEAR desc
