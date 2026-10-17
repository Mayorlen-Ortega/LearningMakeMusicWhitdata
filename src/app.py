"""API for exploring and sonifying the strongest recorded earthquakes."""

from pathlib import Path

import httpx
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

USGS_API_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"
USGS_START_DATE = "1900-01-01"
USGS_MIN_MAGNITUDE = 8.5

app = FastAPI(
    title="Earthquake Sonification Lab",
    description="Explore and sonify USGS earthquake data with Tone.js.",
)

static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/earthquakes")
async def strongest_earthquakes(
    limit: int = Query(default=20, ge=5, le=50),
):
    """Return the strongest USGS earthquakes since the instrumental era began."""
    params = {
        "format": "geojson",
        "starttime": USGS_START_DATE,
        "minmagnitude": USGS_MIN_MAGNITUDE,
        "orderby": "magnitude",
        "limit": limit,
    }

    try:
        async with httpx.AsyncClient(timeout=20.0, follow_redirects=True) as client:
            response = await client.get(USGS_API_URL, params=params)
            response.raise_for_status()
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=502,
            detail="No fue posible consultar el catálogo oficial de USGS.",
        ) from exc

    payload = response.json()
    features = payload.get("features", [])
    features.sort(
        key=lambda feature: feature.get("properties", {}).get("mag") or 0,
        reverse=True,
    )

    return {
        "type": "FeatureCollection",
        "metadata": {
            **payload.get("metadata", {}),
            "catalog": "USGS Earthquake Catalog",
            "start_date": USGS_START_DATE,
            "minimum_magnitude": USGS_MIN_MAGNITUDE,
            "ranking": "Magnitud de momento (Mw), orden descendente",
            "query_url": str(response.request.url),
        },
        "features": features,
    }
