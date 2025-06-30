from django.test import TestCase
from unittest.mock import AsyncMock, patch
import responses
import httpx

from libs.jcdecauxclient import JCDecauxClient, JCDecauxClientAsync, API_BASE_URL


class JCDecauxClientTests(TestCase):
    @responses.activate
    def test_get_contracts(self):
        url = f"{API_BASE_URL}/vls/v3/contracts"
        data = [
            {"name": "test", "commercial_name": "Test", "country_code": "TC", "cities": ["City1"]}
        ]
        responses.add(responses.GET, url, json=data, status=200)

        client = JCDecauxClient(api_key="dummy")
        contracts = client.get_contracts()

        self.assertEqual(len(contracts), 1)
        self.assertEqual(contracts[0].name, "test")

    @responses.activate
    def test_get_station(self):
        url = f"{API_BASE_URL}/vls/v3/stations/1"
        station_data = {
            "number": 1,
            "contractName": "test",
            "name": "Station 1",
            "address": "Somewhere",
            "position": {"latitude": 1.0, "longitude": 2.0},
            "banking": True,
            "bonus": False,
            "status": "OPEN",
            "lastUpdate": "2023-01-01T00:00:00",
            "connected": True,
            "overflow": False,
            "totalStands": {
                "availabilities": {
                    "bikes": 1,
                    "stands": 2,
                    "mechanicalBikes": 1,
                    "electricalBikes": 0,
                    "electricalInternalBatteryBikes": 0,
                    "electricalRemovableBatteryBikes": 0,
                },
                "capacity": 2,
            },
            "mainStands": {
                "availabilities": {
                    "bikes": 1,
                    "stands": 2,
                    "mechanicalBikes": 1,
                    "electricalBikes": 0,
                    "electricalInternalBatteryBikes": 0,
                    "electricalRemovableBatteryBikes": 0,
                },
                "capacity": 2,
            },
        }
        responses.add(responses.GET, url, json=station_data, status=200)

        client = JCDecauxClient(api_key="dummy")
        station = client.get_station(1, "test")

        self.assertEqual(station.number, 1)
        self.assertEqual(station.contractName, "test")
        self.assertEqual(station.position.latitude, 1.0)

    @responses.activate
    def test_get_station_404(self):
        url = f"{API_BASE_URL}/vls/v3/stations/1"
        responses.add(responses.GET, url, status=404)

        client = JCDecauxClient(api_key="dummy")
        with self.assertRaises(ValueError):
            client.get_station(1, "test")


class JCDecauxAsyncClientTests(TestCase):
    async def test_get_contracts(self):
        url = f"{API_BASE_URL}/vls/v3/contracts"
        data = [
            {"name": "test", "commercial_name": "Test", "country_code": "TC", "cities": ["City1"]}
        ]
        response = httpx.Response(200, json=data, request=httpx.Request("GET", url))
        with patch(
            "libs.jcdecauxclient.async_client.httpx.AsyncClient.get",
            new=AsyncMock(return_value=response),
        ):
            client = JCDecauxClientAsync(api_key="dummy")
            contracts = await client.get_contracts()
            await client.close()
        self.assertEqual(len(contracts), 1)
        self.assertEqual(contracts[0].name, "test")

    async def test_get_station_404(self):
        url = f"{API_BASE_URL}/vls/v3/stations/1"
        response = httpx.Response(404, request=httpx.Request("GET", url))
        with patch(
            "libs.jcdecauxclient.async_client.httpx.AsyncClient.get",
            new=AsyncMock(return_value=response),
        ):
            client = JCDecauxClientAsync(api_key="dummy")
            with self.assertRaises(ValueError):
                await client.get_station(1, "test")
            await client.close()
