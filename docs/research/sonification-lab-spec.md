# Especificación del laboratorio de sonificación

Estado: diseño previo a implementación  
Evento inicial: Illapel–Coquimbo 2015 (`us20003k7a`)

## Objetivo

Construir un laboratorio, separado de la obra final, que permita escuchar qué
información aporta cada conjunto de datos. El laboratorio no intentará recrear
todavía una escena realista ni elegir una estética definitiva.

La primera versión tendrá tres capas:

1. ruptura geológica;
2. movimiento local en tierra;
3. propagación marina.

Cada capa deberá mostrar su fuente, unidad, transformación, estado de evidencia
y controles artísticos. Ningún control artístico modificará silenciosamente el
significado del dato original.

## Principio de separación

```text
dato original
    ↓ conservación y metadatos
serie interpretada
    ↓ transformación declarada
señal de control
    ↓ decisión compositiva
audio
```

Se conservarán cinco objetos diferentes:

- archivo original descargado;
- metadatos y huella criptográfica;
- valores parseados;
- valores transformados para escucha;
- configuración musical elegida.

## Contrato mínimo de una fuente

Cada conjunto de datos deberá declarar:

```json
{
  "id": "usgs-finite-fault-moment-rate",
  "event_id": "us20003k7a",
  "authority": "USGS",
  "source_url": "https://.../moment_rate.mr",
  "retrieved_at": "ISO-8601",
  "sha256": "...",
  "evidence": "measured_or_modeled",
  "variable": "moment_rate",
  "unit": "unknown",
  "sample_interval_seconds": 0.4,
  "location": null,
  "missing_values": null,
  "notes": "Unidad pendiente de verificar en la fuente; no es una onda audible"
}
```

La unidad no se supondrá. Si no aparece en la fuente o documentación, quedará
como `unknown` hasta verificarla.

## Capa 1: ruptura geológica

### Fuente necesaria

Curva de tasa de momento `moment_rate.mr` del modelo de falla finita de USGS.

### Qué describe

La evolución estimada de la liberación de momento en la superficie de ruptura.
No representa el sonido de la Tierra ni el movimiento experimentado en Ovalle.

### Transformación inicial

1. conservar tiempo y valor originales;
2. eliminar únicamente el relleno nulo posterior, sin borrar pausas internas;
3. calcular una copia normalizada `r(t) / max(r)`;
4. permitir expansión temporal, manteniendo visible el factor aplicado;
5. suavizar solo para control de parámetros y conservar la curva sin suavizar.

### Funciones musicales candidatas

| Señal derivada | Función | Estado |
| --- | --- | --- |
| Tasa normalizada | Macroenvolvente de energía | Experimental |
| Derivada positiva | Activación de nuevos estratos | Experimental |
| Derivada negativa | Liberación/decaimiento | Experimental |
| Picos locales | Articulaciones estructurales | Experimental |

No se asignará automáticamente a altura. Una opción inicial es controlar la
apertura espectral y la densidad de una masa sonora, manteniendo la altura como
decisión compositiva independiente.

### Componentes Tone.js posibles

- `Tone.Noise` continuo como material excitable;
- `Tone.Filter` para ancho y centro espectral;
- `Tone.Gain` automatizado por la envolvente;
- `Tone.Oscillator` grave como estrato opcional;
- `Tone.Signal` para automatizaciones derivadas de la curva;
- `Tone.Limiter` al final de la cadena.

## Capa 2: movimiento local en tierra

### Fuente preferida

Acelerograma de una estación cercana a Ovalle, idealmente con tres componentes,
frecuencia de muestreo, orientación y unidades documentadas.

### Fuentes insuficientes por sí solas

PGA, PGV y MMI son valores agregados. Sirven para calibrar rangos y contrastar
intensidad, pero no contienen la evolución temporal necesaria para reconstruir
una sacudida.

Por lo tanto:

- no se fabricará una forma de onda a partir de PGA/PGV;
- no se presentará ruido aleatorio como registro sísmico;
- si falta el acelerograma, la capa quedará identificada como maqueta artística.

### Procesamiento futuro del registro

1. verificar unidades, orientación y corrección instrumental;
2. conservar las tres componentes;
3. remover offset únicamente mediante método documentado;
4. explorar aceleración, velocidad integrada y envolvente;
5. trasladar o comprimir frecuencias para audición;
6. declarar siempre el factor temporal y cualquier filtrado.

### Escucha multicanal propuesta

| Componente | Primera función espacial a probar |
| --- | --- |
| Norte–sur | Eje frontal/posterior o paneo horizontal |
| Este–oeste | Segundo eje horizontal |
| Vertical | Elevación virtual o estrato tímbrico independiente |

La asignación espacial será una convención artística, no una reproducción
literal de cómo una persona oyó el movimiento.

## Capa 3: propagación marina

### Fuente necesaria

Serie mareográfica de Coquimbo con hora, intervalo de muestreo, datum y unidad.
Se incorporarán después otras estaciones para mostrar la propagación por el
Pacífico.

### Procesamiento previsto

1. conservar la serie original;
2. separar marea astronómica y anomalía solo con un método citado;
3. fijar `t = 0` en el origen sísmico, conservando la hora absoluta;
4. identificar llegada y máximos sin confundir amplitud con inundación;
5. aplicar compresión temporal visible para llevar horas a minutos de escucha.

### Funciones musicales candidatas

| Dato | Función posible | Precaución |
| --- | --- | --- |
| Anomalía del nivel | Envolvente lenta | No llamarla altura en tierra |
| Pendiente | Dirección/intensidad del flujo musical | No implica velocidad real del agua |
| Tiempo de llegada | Entrada de la capa marina | Depende de cada estación |
| Diferencia entre estaciones | Desplazamiento espacial | Requiere relojes comparables |

El timbre marino podrá usar síntesis o grabaciones, pero la forma temporal debe
poder escucharse también con un sonido neutro para evaluar el dato sin paisaje.

## Modos de escucha

El laboratorio ofrecerá tres modos claramente rotulados:

1. **Dato:** señal neutra y transformación mínima.
2. **Mapeo:** dato controlando parámetros elegidos.
3. **Composición:** libertad tímbrica y formal, manteniendo la trazabilidad.

Esto permitirá comparar qué parte del resultado pertenece al fenómeno y cuál a
la composición.

## Controles comunes

| Control | Tipo | Requisito de interfaz |
| --- | --- | --- |
| Reproducir/pausar | Transporte | Acción de usuario para iniciar audio |
| Posición temporal | Navegación | Mostrar tiempo original y transformado |
| Factor temporal | Transformación | Mostrar relación, por ejemplo `1 s = 10 s` |
| Ganancia de escucha | Artístico/técnico | No modificar ni renombrar el dato fuente |
| Silenciar/solo | Mezcla | Disponible por capa |
| Modo dato/mapeo/composición | Interpretación | Etiqueta siempre visible |
| Restablecer | Reproducibilidad | Volver a parámetros documentados |

No habrá inicialmente controles de “magnitud”, “daño” o “drama”.

## Seguridad de audio

- `Tone.start()` únicamente después de una interacción del usuario.
- Limitador final con margen de seguridad.
- Ganancia inicial conservadora.
- Evitar contenido subgrave a niveles físicamente agresivos.
- Indicador visual de nivel y botón de silencio inmediato.
- Advertencia antes de voces o sonidos de rotura en versiones posteriores.

## Interfaz de trazabilidad

Cada capa mostrará una ficha desplegable:

```text
Fuente: USGS Finite Fault
Variable: tasa de momento
Unidad: pendiente de verificación
Resolución: 0,4 s
Transformación: normalización + expansión temporal ×4
Función musical: apertura de filtro y densidad
Categoría: medido/modelado
```

Si una pieza de información falta, la interfaz deberá decir `no disponible`; no
se reemplazará silenciosamente por un valor generado.

## Orden de implementación

1. Obtener y verificar los tres archivos fuente.
2. Crear sus metadatos y huellas SHA-256.
3. Escribir parsers con pruebas unitarias.
4. Graficar las series antes de producir audio.
5. Implementar transporte y sincronización común.
6. Implementar modo Dato para una sola capa.
7. Añadir modos Mapeo y Composición.
8. Incorporar capas restantes una por una.
9. Probar niveles, accesibilidad y reproducibilidad.

## Criterio de éxito del MVP técnico

El laboratorio será válido cuando otra persona pueda:

- identificar de dónde procede cada serie;
- reproducir la transformación;
- distinguir dato de decisión musical;
- escuchar las capas aisladas y sincronizadas;
- cambiar un mapeo sin alterar los valores originales;
- obtener el mismo resultado al restablecer la configuración.

La belleza o expresividad de la obra no será criterio de éxito de esta primera
herramienta; se evaluará en una etapa compositiva posterior.
