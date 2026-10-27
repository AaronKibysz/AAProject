"""
Tests de paginación para el backend automovilismo-app.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import os
import pytest
from fastapi.testclient import TestClient


class TestPaginationCategories:
    """Tests de paginación para categorías."""

    def test_pagination_default_limit(self, client: TestClient, sample_categories):
        """El límite por defecto debe ser 10."""
        response = client.get("/api/v1/categories")
        data = response.json()
        assert data["limit"] == 10
        assert data["page"] == 1

    def test_pagination_custom_limit(self, client: TestClient, sample_categories):
        """Debe aceptar límite personalizado."""
        response = client.get("/api/v1/categories?include_ficticio=true&limit=1")
        data = response.json()
        assert data["limit"] == 1
        assert len(data["items"]) == 1
        assert data["total"] == 3
        assert data["pages"] == 3

    def test_pagination_page_out_of_range(self, client: TestClient, sample_categories):
        """Página fuera de rango debe retornar lista vacía."""
        response = client.get("/api/v1/categories?include_ficticio=true&page=100&limit=1")
        data = response.json()
        assert data["items"] == []
        assert data["total"] == 3


class TestPaginationPilots:
    """Tests de paginación para pilotos."""

    def test_pagination_pilots(self, client: TestClient, sample_pilots):
        """Debe paginar pilotos correctamente."""
        response = client.get("/api/v1/pilots?include_ficticio=true&page=1&limit=2")
        data = response.json()
        assert len(data["items"]) == 2
        assert data["total"] == 3
        assert data["pages"] == 2

    def test_pagination_pilots_include_ficticio(self, client: TestClient, sample_pilots):
        """Debe paginar solo pilotos no ficticios por defecto."""
        response = client.get("/api/v1/pilots?include_ficticio=false")
        data = response.json()
        assert len(data["items"]) == 2
        for p in data["items"]:
            assert p["is_ficticio"] is False


class TestPaginationCircuits:
    """Tests de paginación para circuitos."""

    def test_pagination_circuits(self, client: TestClient, sample_circuits):
        """Debe paginar circuitos correctamente."""
        response = client.get("/api/v1/circuits?include_ficticio=true&page=1&limit=2")
        data = response.json()
        assert len(data["items"]) == 2
        assert data["total"] == 3
        assert data["pages"] == 2


class TestPaginationSeasons:
    """Tests de paginación para temporadas."""

    def test_pagination_seasons(self, client: TestClient, sample_seasons):
        """Debe paginar temporadas correctamente."""
        response = client.get("/api/v1/seasons?include_ficticio=true&page=1&limit=2")
        data = response.json()
        assert len(data["items"]) == 2
        assert data["total"] == 3
        assert data["pages"] == 2

    def test_pagination_seasons_is_active(self, client: TestClient, sample_seasons):
        """Debe filtrar por is_active."""
        response = client.get("/api/v1/seasons?is_active=true")
        data = response.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["is_active"] is True


class TestPaginationResults:
    """Tests de paginación para resultados."""

    def test_pagination_results(self, client: TestClient, sample_results):
        """Debe paginar resultados correctamente."""
        response = client.get("/api/v1/results?include_ficticio=true&page=1&limit=2")
        data = response.json()
        assert len(data["items"]) == 2
        assert data["total"] == 3
        assert data["pages"] == 2

    def test_pagination_results_by_pilot(self, client: TestClient, sample_results, sample_pilots):
        """Debe filtrar resultados por piloto."""
        pilot_id = sample_pilots[0].id
        response = client.get(f"/api/v1/results?pilot_id={pilot_id}")
        data = response.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["pilot_id"] == pilot_id

    def test_pagination_results_by_circuit(self, client: TestClient, sample_results, sample_circuits):
        """Debe filtrar resultados por circuito."""
        circuit_id = sample_circuits[0].id
        response = client.get(f"/api/v1/results?circuit_id={circuit_id}&include_ficticio=true")
        data = response.json()
        assert len(data["items"]) == 3  # Los 3 resultados son en circuito 1


class TestPaginationSessions:
    """Tests de paginación para sesiones."""

    def test_pagination_sessions(self, client: TestClient, sample_sessions):
        """Debe paginar sesiones correctamente."""
        response = client.get("/api/v1/sessions?page=1&limit=2")
        data = response.json()
        assert len(data["items"]) == 2
        assert data["total"] == 3
        assert data["pages"] == 2

    def test_pagination_sessions_by_type(self, client: TestClient, sample_sessions):
        """Debe filtrar sesiones por tipo."""
        response = client.get("/api/v1/sessions?session_type=race")
        data = response.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["session_type"] == "race"
