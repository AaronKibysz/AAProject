"""
Tests de búsqueda global para el backend automovilismo-app.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import os
import pytest
from fastapi.testclient import TestClient


class TestSearch:
    """Tests para el endpoint de búsqueda global."""

    def test_search_empty_query(self, client: TestClient):
        """Debe rechazar query vacío con 422."""
        response = client.get("/api/v1/search?q=")
        assert response.status_code == 422

    def test_search_no_results(self, client: TestClient):
        """Debe retornar lista vacía cuando no hay resultados."""
        response = client.get("/api/v1/search?q=zzzznonexistent")
        assert response.status_code == 200
        data = response.json()
        assert data == []

    def test_search_category(self, client: TestClient, sample_categories):
        """Debe buscar categorías por nombre."""
        response = client.get("/api/v1/search?q=Turismo")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        # Debe encontrar Turismo Carretera
        tc_results = [r for r in data if r["resource_type"] == "category" and "Turismo" in r["name"]]
        assert len(tc_results) >= 1
        assert tc_results[0]["resource_id"] is not None

    def test_search_pilot(self, client: TestClient, sample_pilots):
        """Debe buscar pilotos por nombre."""
        response = client.get("/api/v1/search?q=Traverso")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        pilot_results = [r for r in data if r["resource_type"] == "pilot"]
        assert len(pilot_results) >= 1
        assert pilot_results[0]["name"] == "Juan María Traverso"

    def test_search_circuit(self, client: TestClient, sample_circuits):
        """Debe buscar circuitos por nombre."""
        response = client.get("/api/v1/search?q=Mouras")
        assert response.status_code == 200
        data = response.json()
        circuit_results = [r for r in data if r["resource_type"] == "circuit"]
        assert len(circuit_results) >= 1
        assert circuit_results[0]["name"] == "Autódromo Roberto Mouras"

    def test_search_season(self, client: TestClient, sample_seasons):
        """Debe buscar temporadas por año."""
        response = client.get("/api/v1/search?q=2024")
        assert response.status_code == 200
        data = response.json()
        season_results = [r for r in data if r["resource_type"] == "season"]
        assert len(season_results) >= 1
        assert season_results[0]["name"] == "2024"

    def test_search_multiple_types(self, client: TestClient, sample_categories, sample_pilots, sample_circuits):
        """Debe retornar resultados de múltiples tipos."""
        response = client.get("/api/v1/search?q=Turismo")
        assert response.status_code == 200
        data = response.json()
        # Debe tener al menos categorías
        types_found = set(r["resource_type"] for r in data)
        assert "category" in types_found

    def test_search_limit_per_type(self, client: TestClient, sample_pilots):
        """Debe respetar limit_per_type."""
        response = client.get("/api/v1/search?q=a&limit_per_type=1")
        assert response.status_code == 200
        data = response.json()
        # Contar resultados por tipo
        pilot_count = sum(1 for r in data if r["resource_type"] == "pilot")
        assert pilot_count <= 1

    def test_search_result_structure(self, client: TestClient, sample_categories):
        """Debe retornar estructura correcta en cada resultado."""
        response = client.get("/api/v1/search?q=Turismo")
        assert response.status_code == 200
        data = response.json()
        if len(data) > 0:
            result = data[0]
            assert "resource_type" in result
            assert "resource_id" in result
            assert "name" in result
            assert "is_ficticio" in result
            assert result["resource_type"] in ("category", "pilot", "circuit", "season")
