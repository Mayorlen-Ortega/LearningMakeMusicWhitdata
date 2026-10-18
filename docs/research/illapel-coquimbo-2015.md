# Expediente sonoro: terremoto de Illapel–Coquimbo de 2015

Estado: borrador de investigación v0.1  
Evento USGS: `us20003k7a`  
Fecha de consulta: 17 de octubre de 2026

## Propósito

Este documento reúne la evidencia que puede sostener una reconstrucción sonora
contextual del terremoto y tsunami de 2015. No describe una grabación real ni
prescribe todavía una composición. Su objetivo es mantener separados los datos
medidos, la documentación histórica, los testimonios, las inferencias y las
decisiones artísticas.

## Convenciones de evidencia

| Código | Categoría | Significado |
| --- | --- | --- |
| M | Medido/modelado | Producto instrumental o modelo científico con unidades |
| D | Documentado | Informe institucional o registro histórico |
| T | Testimonio | Recuerdo situado de una persona, no generalizable |
| I | Inferido | Hipótesis contextual que requiere justificación |
| A | Artístico | Decisión compositiva explícita, sin pretensión factual |

## Identidad del evento

| Campo | Valor | Evidencia |
| --- | --- | --- |
| Fecha | 16 de septiembre de 2015 | M — USGS |
| Hora de origen | 22:54:32.860 UTC; aproximadamente 19:54:32 en Chile | M — USGS |
| Magnitud | Mww 8,3 | M — USGS |
| Epicentro | 31,5729° S, 71,6744° O; 48 km al oeste de Illapel | M — USGS |
| Profundidad | 22,44 km | M — USGS |
| Mecanismo | Falla inversa en la interfaz de subducción Nazca–Sudamérica | M/D — USGS |
| Momento sísmico | 3,19 × 10²¹ Nm | M — USGS Moment Tensor |
| Respuestas DYFI | 1.216; intensidad máxima reportada IX | M/T agregada — USGS |

El resumen tectónico de USGS sitúa el evento en la interfaz de subducción y
señala una convergencia aproximada de 74 mm/año entre las placas de Nazca y
Sudamericana. Una falla de esta escala debe representarse como una superficie
de ruptura, no como un punto aislado.

## Ruptura y temporalidad

El modelo de fuente finita de USGS informa:

- Modelo de falla de aproximadamente 300 × 158,4 km.
- Un segmento con rumbo cercano a 6° y buzamiento cercano a 19°.
- Deslizamiento máximo modelado de aproximadamente 3,2 m.
- Tiempo medio de ascenso de aproximadamente 5,55 s.
- Velocidad media de ruptura publicada como 1,47 en el producto; la unidad debe
  confirmarse en la documentación antes de usarla.

Análisis local de la curva `moment_rate.mr` de USGS:

| Rasgo | Tiempo aproximado |
| --- | ---: |
| Primer valor no nulo | 2,8 s |
| Máximo de tasa de momento | 36,8 s |
| Actividad sobre 5 % del máximo | 6,8–130,4 s |
| Actividad sobre 1 % del máximo | 4,4–160,0 s |
| Último valor no nulo del modelo | 209,6 s |

Estos umbrales son cálculos derivados, no duraciones oficiales. Tampoco son
equivalentes a la duración del movimiento fuerte en una ciudad. Para la obra se
mantendrán tres relojes diferentes:

1. liberación de momento en la falla;
2. movimiento instrumental en cada punto;
3. duración subjetiva o testimonial.

## Intensidad territorial

Valores aproximados extraídos del punto de grilla ShakeMap más cercano a cada
ciudad. PGA está expresada como porcentaje de `g`; PGV, en cm/s.

| Localidad | MMI ShakeMap | PGA (%g) | PGV (cm/s) | MMI PAGER de ciudad |
| --- | ---: | ---: | ---: | ---: |
| Illapel | 8,2 | 43,51 | 37,96 | 8,02 |
| Ovalle | 7,7 | 45,89 | 39,12 | 7,63 |
| Coquimbo | 6,9 | 31,77 | 21,60 | 6,84 |
| La Serena | 6,4 | 24,05 | 18,19 | 6,56 |

El texto de impacto de USGS registra intensidades observadas IX en Illapel y
VIII en Coquimbo, La Serena y Ovalle. Las diferencias respecto de ShakeMap y
PAGER se conservarán: proceden de productos y metodologías distintas.

No se traducirá la magnitud global directamente a volumen. Para una ubicación,
MMI, PGA, PGV y el registro de estación son parámetros más pertinentes.

## Tsunami

USGS documenta un tsunami trans-Pacífico. Amplitudes máximas seleccionadas en
estaciones mareográficas:

| Estación | Amplitud máxima documentada |
| --- | ---: |
| Coquimbo | 4,75 m |
| Quintero | 1,86 m |
| Valparaíso | 1,78 m |
| Talcahuano | 1,28 m |
| Juan Fernández | 1,21 m |
| Caldera | 1,14 m |
| Chañaral | 1,09 m |
| San Antonio | 1,04 m |
| Hilo, Hawái | 0,90 m |
| Isla de Pascua | 0,83 m |

Estos valores son amplitudes registradas, no deben llamarse automáticamente
“altura de inundación” ni “altura de ola en tierra”. Faltan las series
mareográficas y los tiempos de llegada de SHOA/NOAA.

La generación del tsunami comienza vinculada al desplazamiento submarino de la
ruptura, aunque su llegada a la costa sea posterior. La composición puede hacer
audible esta coexistencia sin presentar el mar como parte de un testimonio
interior en Ovalle.

## Daños y fenómenos secundarios

El texto de impacto de USGS documenta daños humanos y materiales en Coquimbo,
Valparaíso y la Región Metropolitana, además de un deslizamiento en Canela. Los
productos globales de falla del terreno clasifican el peligro agregado de
deslizamientos como naranja y el de licuefacción como amarillo.

Estas categorías son modelos regionales. No autorizan a insertar derrumbes,
explosiones o licuefacción en cualquier localidad. Los daños humanos se
documentarán por respeto histórico, pero nunca se transformarán directamente
en amplitud, densidad o espectacularidad sonora.

## Aporte testimonial al modelo

El testimonio disponible se usará como conocimiento perceptivo, no como trama
autobiográfica. Los detalles familiares y privados quedan fuera del modelo y de
la obra.

Rasgos utilizables como hipótesis compositivas:

| Rasgo testimonial | Alcance permitido |
| --- | --- |
| Inicio pendular y suave | Morfología perceptiva a contrastar con registros |
| Crecimiento hasta movimiento fuerte | Curva subjetiva, separada de la instrumental |
| Rugido aparentemente omnidireccional | Hipótesis espacial y espectral |
| Caída de vidrio, libros y objetos | Respuesta material plausible en MMI alta |
| Alarmas y choque de cables al salir | Cambio entre espacio interior y exterior |
| Corte eléctrico prolongado | Estado tecnológico posterior, pendiente de fuentes |
| Mezcla de shock y normalidad | Idea formal, no medición histórica |

El tsunami se conoció indirectamente y no pertenece a la escucha testimonial.
Se incorporará mediante mediciones y documentación costera.

## Hipótesis para una futura matriz musical

Estas relaciones son candidatas a experimentación, no decisiones cerradas:

| Evidencia | Función musical posible | Riesgo que debe evitarse |
| --- | --- | --- |
| Tasa de momento | Macroenvolvente de la capa geológica | Confundirla con audio audible |
| PGA | Densidad de transitorios y activación de objetos | Usarla como simple volumen |
| PGV | Energía de movimiento continuo | Confundir velocidad física con tempo |
| MMI local | Probabilidad de capas materiales | Convertir daño en espectáculo |
| Registro de estación | Modulación, excitación o audio acelerado | Ocultar el procesamiento |
| Modelo de deslizamiento | Distribución espacial de fuentes | Tratar el epicentro como único foco |
| Mareógrafos | Forma temporal de la capa marina | Confundir amplitud con inundación |
| Testimonios | Morfología perceptiva | Presentarlos como mediciones |

## Fuentes verificadas

1. USGS, [página del evento `us20003k7a`](https://earthquake.usgs.gov/earthquakes/eventpage/us20003k7a/executive).
2. USGS, [GeoJSON detallado del evento](https://earthquake.usgs.gov/earthquakes/feed/v1.0/detail/us20003k7a.geojson).
3. USGS ShakeMap Atlas, [`grid.xml`](https://earthquake.usgs.gov/product/shakemap/us20003k7a/atlas/1594162150247/download/grid.xml).
4. USGS Finite Fault, [`moment_rate.mr`](https://earthquake.usgs.gov/product/finite-fault/us20003k7a/us/1539809967421/moment_rate.mr).
5. USGS Finite Fault, [`FFM.geojson`](https://earthquake.usgs.gov/product/finite-fault/us20003k7a/us/1539809967421/FFM.geojson).
6. USGS PAGER, [`cities.json`](https://earthquake.usgs.gov/product/losspager/us20003k7a/us/1502483271861/json/cities.json).
7. USGS, Tectonic Summary incluido en el producto `general-text` del evento.
8. USGS, Impact Text incluido en el producto `impact-text` del evento.

## Fuentes pendientes

- Centro Sismológico Nacional: parámetros nacionales y registros de estaciones.
- SHOA: boletines, mareogramas, tiempos de llegada y amplitudes.
- SENAPRED/ONEMI: cronología de alertas, evacuación e infraestructura.
- Center for Engineering Strong Motion Data: acelerogramas disponibles.
- NOAA/NCEI: catálogo y observaciones trans-Pacíficas del tsunami.
- Estudios revisados por pares sobre ruptura, duración y tsunami.

Hasta completar estas fuentes no se fijarán tiempos de llegada del tsunami,
sonidos específicos de daños por localidad ni una curva definitiva de
movimiento en Ovalle.

## Próximo experimento recomendado

Construir un laboratorio aislado con tres capas y controles visibles:

1. una macroenvolvente basada en la tasa de momento;
2. una capa terrestre local controlada por un registro o por PGA/PGV;
3. una capa marina controlada por una serie mareográfica.

Cada control deberá indicar la fuente, unidad, transformación y categoría de
evidencia. El objetivo inicial no será componer la obra final, sino escuchar qué
información aporta realmente cada conjunto de datos.
