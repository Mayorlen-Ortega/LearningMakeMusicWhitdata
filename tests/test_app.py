import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from src.app import app


SAMPLE_USGS_RESPONSE = {
    "type": "FeatureCollection",
    "metadata": {"count": 2, "title": "USGS earthquakes"},
    "features": [
        {
            "type": "Feature",
            "properties": {
                "mag": 9.2,
                "place": "Southern Alaska",
                "time": -181859400000,
                "url": "https://earthquake.usgs.gov/earthquakes/eventpage/example-92",
            },
            "geometry": {"type": "Point", "coordinates": [-147.3, 60.9, 25]},
        },
        {
            "type": "Feature",
            "properties": {
                "mag": 9.5,
                "place": "Valdivia, Chile",
                "time": -303588000000,
                "url": "https://earthquake.usgs.gov/earthquakes/eventpage/example-95",
            },
            "geometry": {"type": "Point", "coordinates": [-73.4, -38.1, 25]},
        },
    ],
}


class FakeRequest:
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson"


class FakeResponse:
    request = FakeRequest()

    def raise_for_status(self):
        return None

    def json(self):
        return SAMPLE_USGS_RESPONSE


class FakeAsyncClient:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        return None

    async def get(self, url, params):
        self.url = url
        self.params = params
        return FakeResponse()


class EarthquakeApiTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_home_redirects_to_map(self):
        response = self.client.get("/", follow_redirects=False)
        self.assertEqual(response.status_code, 307)
        self.assertEqual(response.headers["location"], "/static/index.html")

    @patch("src.app.httpx.AsyncClient", FakeAsyncClient)
    def test_earthquakes_are_ranked_by_magnitude(self):
        response = self.client.get("/earthquakes?limit=20")

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual([item["properties"]["mag"] for item in data["features"]], [9.5, 9.2])
        self.assertEqual(data["metadata"]["catalog"], "USGS Earthquake Catalog")
        self.assertEqual(data["metadata"]["start_date"], "1900-01-01")

    def test_limit_is_validated(self):
        response = self.client.get("/earthquakes?limit=2")
        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()
