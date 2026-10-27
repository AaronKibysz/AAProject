"""
Tests de refresh tokens para el backend automovilismo-app.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import os
import pytest
from fastapi.testclient import TestClient


class TestRefreshToken:
    """Tests para el endpoint de renovación de tokens."""

    def test_login_returns_refresh_token(self, client: TestClient, test_user):
        """El login debe retornar un refresh_token en la respuesta."""
        response = client.post("/api/v1/auth/login", json={
            "email": "test@example.com",
            "password": "TestPassword123"
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["refresh_token"] is not None
        assert "refresh_expires_in" in data
        assert data["refresh_expires_in"] > 0

    def test_refresh_token_success(self, client: TestClient, test_user):
        """Debe renovar el access token usando un refresh token válido."""
        # Login primero
        login_resp = client.post("/api/v1/auth/login", json={
            "email": "test@example.com",
            "password": "TestPassword123"
        })
        assert login_resp.status_code == 200
        refresh_token = login_resp.json()["refresh_token"]

        # Usar refresh token para obtener nuevo access token
        response = client.post("/api/v1/auth/refresh", json={"refresh_token": refresh_token})
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["refresh_token"] != refresh_token  # Rotación de tokens

    def test_refresh_token_invalid(self, client: TestClient):
        """Debe rechazar un refresh token inválido con 422."""
        response = client.post("/api/v1/auth/refresh", json={"refresh_token": "token_invalido"})
        assert response.status_code == 422

    def test_refresh_token_revoked(self, client: TestClient, test_user):
        """Debe rechazar un refresh token revocado."""
        # Login primero
        login_resp = client.post("/api/v1/auth/login", json={
            "email": "test@example.com",
            "password": "TestPassword123"
        })
        refresh_token = login_resp.json()["refresh_token"]

        # Hacer logout para revocar el token
        client.post("/api/v1/auth/logout", json=refresh_token)

        # Intentar usar el token revocado
        response = client.post("/api/v1/auth/refresh", json={"refresh_token": refresh_token})
        assert response.status_code == 422

    def test_logout_success(self, client: TestClient, test_user):
        """Debe revocar el refresh token con logout."""
        login_resp = client.post("/api/v1/auth/login", json={
            "email": "test@example.com",
            "password": "TestPassword123"
        })
        refresh_token = login_resp.json()["refresh_token"]

        response = client.post("/api/v1/auth/logout", json={"refresh_token": refresh_token})
        assert response.status_code == 204

    def test_logout_all_success(self, client: TestClient, auth_headers):
        """Debe revocar todos los refresh tokens del usuario."""
        # Crear un refresh token primero (hacer login)
        login_resp = client.post("/api/v1/auth/login", json={
            "email": "test@example.com",
            "password": "TestPassword123"
        })
        assert login_resp.status_code == 200

        # Logout all
        response = client.post("/api/v1/auth/logout-all", headers=auth_headers)
        assert response.status_code == 204

    def test_logout_all_without_auth(self, client: TestClient):
        """Debe rechazar logout-all sin token con 401."""
        response = client.post("/api/v1/auth/logout-all")
        assert response.status_code == 401

    def test_refresh_token_rotation(self, client: TestClient, test_user):
        """El refresh token debe rotarse (el viejo se revoca)."""
        # Login
        login_resp = client.post("/api/v1/auth/login", json={
            "email": "test@example.com",
            "password": "TestPassword123"
        })
        old_refresh = login_resp.json()["refresh_token"]

        # Usar refresh para obtener nuevo token
        refresh_resp = client.post("/api/v1/auth/refresh", json=old_refresh)
        assert refresh_resp.status_code == 200
        new_refresh = refresh_resp.json()["refresh_token"]

        # El viejo refresh token debe estar revocado
        old_refresh_resp = client.post("/api/v1/auth/refresh", json={"refresh_token": old_refresh})
        assert old_refresh_resp.status_code == 422
