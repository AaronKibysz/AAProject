"""
Tests de autenticación (auth) para el backend automovilismo-app.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import os
import pytest
from fastapi.testclient import TestClient


class TestAuthRegister:
    """Tests para el endpoint de registro de usuarios."""

    def test_register_success(self, client: TestClient):
        """Debe crear un usuario nuevo y retornar 201."""
        response = client.post("/api/v1/auth/register", json={
            "email": "nuevo.usuario@ejemplo.com",
            "password": "ClaveSegura123"
        })
        assert response.status_code == 201
        data = response.json()
        assert data["id"] is not None
        assert data["email"] == "nuevo.usuario@ejemplo.com"
        assert data["is_active"] is True
        assert "created_at" in data

    def test_register_duplicate_email(self, client: TestClient, test_user):
        """Debe rechazar el registro de un email ya existente con 409."""
        response = client.post("/api/v1/auth/register", json={
            "email": test_user.email,
            "password": "OtraClave123"
        })
        assert response.status_code == 409

    def test_register_invalid_email(self, client: TestClient):
        """Debe rechazar un email con formato inválido con 422."""
        response = client.post("/api/v1/auth/register", json={
            "email": "no-es-un-email",
            "password": "ClaveSegura123"
        })
        assert response.status_code == 422

    def test_register_short_password(self, client: TestClient):
        """Debe rechazar una contraseña menor a 8 caracteres con 422."""
        response = client.post("/api/v1/auth/register", json={
            "email": "usuario@ejemplo.com",
            "password": "corto"
        })
        assert response.status_code == 422


class TestAuthLogin:
    """Tests para el endpoint de login."""

    def test_login_success(self, client: TestClient, test_user):
        """Debe autenticar al usuario y retornar un token JWT."""
        response = client.post("/api/v1/auth/login", json={
            "email": test_user.email,
            "password": "TestPassword123"
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["expires_in"] > 0

    def test_login_wrong_password(self, client: TestClient, test_user):
        """Debe rechazar credenciales incorrectas con 422."""
        response = client.post("/api/v1/auth/login", json={
            "email": test_user.email,
            "password": "ContrasenaIncorrecta"
        })
        assert response.status_code == 422

    def test_login_nonexistent_user(self, client: TestClient):
        """Debe rechazar usuario inexistente con 404."""
        response = client.post("/api/v1/auth/login", json={
            "email": "noexiste@ejemplo.com",
            "password": "CualquierClave123"
        })
        assert response.status_code == 404

    def test_login_email_case_insensitive(self, client: TestClient, test_user):
        """El login debe ser case-insensitive para el email."""
        response = client.post("/api/v1/auth/login", json={
            "email": test_user.email.upper(),
            "password": "TestPassword123"
        })
        assert response.status_code == 200
        assert "access_token" in response.json()
