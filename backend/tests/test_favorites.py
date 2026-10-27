"""
Tests de favoritos para el backend automovilismo-app.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import os
import pytest
from fastapi.testclient import TestClient


class TestFavoritesCreate:
    """Tests para crear favoritos."""

    def test_create_favorite_success(self, client: TestClient, auth_headers, sample_pilots):
        """Debe crear un favorito y retornar 201."""
        response = client.post("/api/v1/favorites", json={
            "resource_type": "pilot",
            "resource_id": sample_pilots[0].id
        }, headers=auth_headers)
        assert response.status_code == 201
        data = response.json()
        assert data["resource_type"] == "pilot"
        assert data["resource_id"] == sample_pilots[0].id
        assert data["user_id"] is not None

    def test_create_favorite_duplicate(self, client: TestClient, auth_headers, sample_pilots):
        """Debe rechazar favorito duplicado con 409."""
        client.post("/api/v1/favorites", json={
            "resource_type": "pilot",
            "resource_id": sample_pilots[0].id
        }, headers=auth_headers)
        response = client.post("/api/v1/favorites", json={
            "resource_type": "pilot",
            "resource_id": sample_pilots[0].id
        }, headers=auth_headers)
        assert response.status_code == 409

    def test_create_favorite_without_auth(self, client: TestClient, sample_pilots):
        """Debe rechazar sin token con 401."""
        response = client.post("/api/v1/favorites", json={
            "resource_type": "pilot",
            "resource_id": sample_pilots[0].id
        })
        assert response.status_code == 401

    def test_create_favorite_invalid_type(self, client: TestClient, auth_headers):
        """Debe rechazar tipo de recurso inválido con 422."""
        response = client.post("/api/v1/favorites", json={
            "resource_type": "tipo_invalido",
            "resource_id": 1
        }, headers=auth_headers)
        assert response.status_code == 422


class TestFavoritesList:
    """Tests para listar favoritos."""

    def test_list_favorites_empty(self, client: TestClient, auth_headers):
        """Debe retornar lista vacía si no hay favoritos."""
        response = client.get("/api/v1/favorites", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data == []

    def test_list_favorites_with_data(self, client: TestClient, auth_headers, sample_pilots, sample_circuits):
        """Debe retornar los favoritos del usuario."""
        client.post("/api/v1/favorites", json={
            "resource_type": "pilot",
            "resource_id": sample_pilots[0].id
        }, headers=auth_headers)
        client.post("/api/v1/favorites", json={
            "resource_type": "circuit",
            "resource_id": sample_circuits[0].id
        }, headers=auth_headers)
        
        response = client.get("/api/v1/favorites", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    def test_list_favorites_without_auth(self, client: TestClient):
        """Debe rechazar sin token con 401."""
        response = client.get("/api/v1/favorites")
        assert response.status_code == 401


class TestFavoritesDelete:
    """Tests para eliminar favoritos."""

    def test_delete_favorite_success(self, client: TestClient, auth_headers, sample_pilots):
        """Debe eliminar el favorito y retornar 204."""
        create_resp = client.post("/api/v1/favorites", json={
            "resource_type": "pilot",
            "resource_id": sample_pilots[0].id
        }, headers=auth_headers)
        favorite_id = create_resp.json()["id"]
        
        response = client.delete(f"/api/v1/favorites/{favorite_id}", headers=auth_headers)
        assert response.status_code == 204

    def test_delete_favorite_not_found(self, client: TestClient, auth_headers):
        """Debe retornar 404 si el favorito no existe."""
        response = client.delete("/api/v1/favorites/999", headers=auth_headers)
        assert response.status_code == 404

    def test_delete_favorite_without_auth(self, client: TestClient):
        """Debe rechazar sin token con 401."""
        response = client.delete("/api/v1/favorites/1")
        assert response.status_code == 401

    def test_delete_favorite_not_owner(self, client: TestClient, auth_headers, sample_pilots):
        """Un usuario no puede eliminar favoritos de otro usuario."""
        # Crear favorito con el primer usuario
        create_resp = client.post("/api/v1/favorites", json={
            "resource_type": "pilot",
            "resource_id": sample_pilots[0].id
        }, headers=auth_headers)
        favorite_id = create_resp.json()["id"]
        
        # Crear otro usuario y tratar de eliminar su favorito
        client.post("/api/v1/auth/register", json={
            "email": "otro.usuario@ejemplo.com",
            "password": "OtraClave123"
        })
        login_resp = client.post("/api/v1/auth/login", json={
            "email": "otro.usuario@ejemplo.com",
            "password": "OtraClave123"
        })
        other_token = login_resp.json()["access_token"]
        other_headers = {"Authorization": f"Bearer {other_token}"}
        
        response = client.delete(f"/api/v1/favorites/{favorite_id}", headers=other_headers)
        assert response.status_code == 404
