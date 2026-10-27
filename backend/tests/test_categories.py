"""
Tests de categorías para el backend automovilismo-app.
Incluye tests de CRUD y paginación.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import os
import pytest
from fastapi.testclient import TestClient


class TestCategoriesList:
    """Tests para listar categorías."""

    def test_list_categories_empty(self, client: TestClient):
        """Debe retornar lista vacía cuando no hay categorías."""
        response = client.get("/api/v1/categories")
        assert response.status_code == 200
        data = response.json()
        assert data["items"] == []
        assert data["total"] == 0
        assert data["page"] == 1
        assert data["limit"] == 10
        assert data["pages"] == 0

    def test_list_categories_with_data(self, client: TestClient, sample_categories):
        """Debe retornar las categorías creadas."""
        response = client.get("/api/v1/categories?include_ficticio=true")
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 3
        assert data["total"] == 3
        assert data["pages"] == 1

    def test_list_categories_pagination(self, client: TestClient, sample_categories):
        """Debe soportar paginación con page y limit."""
        response = client.get("/api/v1/categories?include_ficticio=true&page=1&limit=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 2
        assert data["total"] == 3
        assert data["page"] == 1
        assert data["limit"] == 2
        assert data["pages"] == 2

    def test_list_categories_page_2(self, client: TestClient, sample_categories):
        """Debe retornar la segunda página cuando hay paginación."""
        response = client.get("/api/v1/categories?include_ficticio=true&page=2&limit=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 1
        assert data["page"] == 2
        assert data["pages"] == 2

    def test_list_categories_include_ficticio(self, client: TestClient, sample_categories):
        """Por defecto debe excluir categorías ficticias."""
        response = client.get("/api/v1/categories?include_ficticio=false")
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 2  # Solo las no ficticias
        for cat in data["items"]:
            assert cat["is_ficticio"] is False

    def test_list_categories_include_ficticio_true(self, client: TestClient, sample_categories):
        """Con include_ficticio=true debe incluir todas."""
        response = client.get("/api/v1/categories?include_ficticio=true")
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 3  # Todas las categorías


class TestCategoriesGetById:
    """Tests para obtener categoría por ID."""

    def test_get_category_by_id_success(self, client: TestClient, sample_categories):
        """Debe retornar la categoría solicitada."""
        cat_id = sample_categories[0].id
        response = client.get(f"/api/v1/categories/{cat_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == cat_id
        assert data["name"] == "Turismo Carretera"

    def test_get_category_by_id_not_found(self, client: TestClient):
        """Debe retornar 404 si la categoría no existe."""
        response = client.get("/api/v1/categories/999")
        assert response.status_code == 404


class TestCategoriesCreate:
    """Tests para crear categorías."""

    def test_create_category_success(self, client: TestClient):
        """Debe crear una categoría y retornar 201."""
        response = client.post("/api/v1/categories", json={
            "name": "Nueva Categoría",
            "description": "Descripción de prueba",
            "is_ficticio": False
        })
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Nueva Categoría"
        assert data["description"] == "Descripción de prueba"
        assert data["is_ficticio"] is False
        assert data["id"] is not None

    def test_create_category_duplicate(self, client: TestClient, sample_categories):
        """Debe rechazar categoría duplicada con 409."""
        response = client.post("/api/v1/categories", json={
            "name": "Turismo Carretera",
            "is_ficticio": False
        })
        assert response.status_code == 409

    def test_create_category_invalid_name(self, client: TestClient):
        """Debe rechazar nombre muy corto con 422."""
        response = client.post("/api/v1/categories", json={
            "name": "A",
            "is_ficticio": False
        })
        assert response.status_code == 422


class TestCategoriesUpdate:
    """Tests para actualizar categorías."""

    def test_update_category_success(self, client: TestClient, sample_categories):
        """Debe actualizar la categoría y retornar 200."""
        cat_id = sample_categories[0].id
        response = client.put(f"/api/v1/categories/{cat_id}", json={
            "name": "Turismo Carretera Actualizado",
            "is_ficticio": False
        })
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Turismo Carretera Actualizado"

    def test_update_category_not_found(self, client: TestClient):
        """Debe retornar 404 si la categoría no existe."""
        response = client.put("/api/v1/categories/999", json={
            "name": "Nuevo Nombre"
        })
        assert response.status_code == 404
