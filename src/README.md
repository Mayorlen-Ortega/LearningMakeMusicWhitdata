# Atlas sísmico sonoro

Aplicación de práctica que consulta el catálogo oficial de terremotos de
[USGS](https://earthquake.usgs.gov/fdsnws/event/1/), ubica en un mapa los
eventos de mayor magnitud desde 1900 y convierte sus datos en sonido con
Tone.js.

El ranking se genera con una consulta reproducible al catálogo de USGS,
ordenada por la magnitud preferida del organismo. En los grandes terremotos
esta suele pertenecer a la familia de magnitud de momento (por ejemplo `mw`,
`mww` o `mwc`), más adecuada que la escala local de Richter para comparar
eventos de este tamaño.

## Sonificación

- Latitud: selecciona una nota de una escala pentatónica.
- Profundidad: selecciona el registro; un foco más profundo produce notas más
  graves.
- Magnitud: controla el volumen y la duración.
- Longitud: controla el paneo estéreo.

Estas reglas son una interpretación artística de los datos, no una
reconstrucción del sonido físico de un terremoto.

## Ejecución

Desde la raíz del repositorio:

```bash
source /workspace/.venvs/LearningMakeMusicWhitdata/bin/activate
python -m uvicorn src.app:app --reload --reload-include 'src/static/*'
```

La interfaz queda disponible en `http://localhost:8000/` y la consulta
normalizada en `http://localhost:8000/earthquakes`.

## Pruebas

Las pruebas no dependen de la red: simulan una respuesta oficial con la misma
estructura GeoJSON.

```bash
python -m unittest discover -s tests -v
```
