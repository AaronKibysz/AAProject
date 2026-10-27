// Servicio API para comunicación con el backend
// Usa axios para las peticiones HTTP

import axios, { AxiosInstance, AxiosResponse } from 'axios';
import AsyncStorage from './storage';
import { Token } from '../types';

// URL base del backend (Docker: 8080, local: 8000)
const API_BASE_URL = 'http://10.0.2.2:8080';

// Claves de almacenamiento
const ACCESS_TOKEN_KEY = 'access_token';
const REFRESH_TOKEN_KEY = 'refresh_token';

class ApiService {
  private api: AxiosInstance;

  constructor() {
    this.api = axios.create({
      baseURL: API_BASE_URL,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Interceptor para agregar token de autenticación
    this.api.interceptors.request.use(
      async (config) => {
        const token = await AsyncStorage.getItem(ACCESS_TOKEN_KEY);
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Interceptor para manejar respuestas y refresh de token
    this.api.interceptors.response.use(
      (response) => response,
      async (error) => {
        const originalRequest = error.config;

        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true;

          try {
            const refreshToken = await AsyncStorage.getItem(REFRESH_TOKEN_KEY);
            if (refreshToken) {
              const response = await axios.post<Token>(
                `${API_BASE_URL}/api/v1/auth/refresh`,
                { refresh_token: refreshToken }
              );

              const { access_token, refresh_token: newRefreshToken } = response.data;

              await AsyncStorage.setItem(ACCESS_TOKEN_KEY, access_token);
              if (newRefreshToken) {
                await AsyncStorage.setItem(REFRESH_TOKEN_KEY, newRefreshToken);
              }

              originalRequest.headers.Authorization = `Bearer ${access_token}`;
              return this.api(originalRequest);
            }
          } catch (refreshError) {
            // Si el refresh falla, limpiar tokens
            await AsyncStorage.removeItem(ACCESS_TOKEN_KEY);
            await AsyncStorage.removeItem(REFRESH_TOKEN_KEY);
          }
        }

        return Promise.reject(error);
      }
    );
  }

  // --- Autenticación ---

  async register(data: { email: string; username: string; password: string; full_name?: string }) {
    const response = await this.api.post('/api/v1/auth/register', data);
    return response.data;
  }

  async login(email: string, password: string): Promise<Token> {
    const response = await this.api.post<Token>('/api/v1/auth/login', {
      email,
      password,
    });
    const { access_token, refresh_token } = response.data;

    await AsyncStorage.setItem(ACCESS_TOKEN_KEY, access_token);
    if (refresh_token) {
      await AsyncStorage.setItem(REFRESH_TOKEN_KEY, refresh_token);
    }

    return response.data;
  }

  async logout(): Promise<void> {
    const refreshToken = await AsyncStorage.getItem(REFRESH_TOKEN_KEY);
    if (refreshToken) {
      try {
        await this.api.post('/api/v1/auth/logout', { refresh_token: refreshToken });
      } catch (error) {
        // Ignorar errores de logout
      }
    }
    await AsyncStorage.removeItem(ACCESS_TOKEN_KEY);
    await AsyncStorage.removeItem(REFRESH_TOKEN_KEY);
  }

  async logoutAll(): Promise<void> {
    await this.api.post('/api/v1/auth/logout-all');
    await AsyncStorage.removeItem(ACCESS_TOKEN_KEY);
    await AsyncStorage.removeItem(REFRESH_TOKEN_KEY);
  }

  async getCurrentUser() {
    const response = await this.api.get('/api/v1/auth/me');
    return response.data;
  }

  // --- Categorías ---

  async getCategories(params?: { page?: number; limit?: number; search?: string }) {
    const response = await this.api.get('/api/v1/categories', { params });
    return response.data;
  }

  async getCategory(id: number) {
    const response = await this.api.get(`/api/v1/categories/${id}`);
    return response.data;
  }

  // --- Pilotos ---

  async getPilots(params?: { page?: number; limit?: number; search?: string; category_id?: number }) {
    const response = await this.api.get('/api/v1/pilots', { params });
    return response.data;
  }

  async getPilot(id: number) {
    const response = await this.api.get(`/api/v1/pilots/${id}`);
    return response.data;
  }

  // --- Circuitos ---

  async getCircuits(params?: { page?: number; limit?: number; search?: string }) {
    const response = await this.api.get('/api/v1/circuits', { params });
    return response.data;
  }

  async getCircuit(id: number) {
    const response = await this.api.get(`/api/v1/circuits/${id}`);
    return response.data;
  }

  // --- Temporadas ---

  async getSeasons(params?: { page?: number; limit?: number; search?: string; category_id?: number }) {
    const response = await this.api.get('/api/v1/seasons', { params });
    return response.data;
  }

  // --- Resultados ---

  async getResults(params?: { page?: number; limit?: number; season_id?: number; pilot_id?: number }) {
    const response = await this.api.get('/api/v1/results', { params });
    return response.data;
  }

  // --- Sesiones ---

  async getSessions(params?: { page?: number; limit?: number; season_id?: number }) {
    const response = await this.api.get('/api/v1/sessions', { params });
    return response.data;
  }

  // --- Búsqueda Global ---

  async search(query: string) {
    const response = await this.api.get('/api/v1/search', { params: { q: query } });
    return response.data;
  }

  // --- Favoritos ---

  async getFavorites() {
    const response = await this.api.get('/api/v1/favorites');
    return response.data;
  }

  async createFavorite(resourceType: string, resourceId: number) {
    const response = await this.api.post('/api/v1/favorites', {
      resource_type: resourceType,
      resource_id: resourceId,
    });
    return response.data;
  }

  async deleteFavorite(id: number) {
    const response = await this.api.delete(`/api/v1/favorites/${id}`);
    return response.data;
  }

  // --- Utilidades ---

  async isAuthenticated(): Promise<boolean> {
    const token = await AsyncStorage.getItem(ACCESS_TOKEN_KEY);
    return !!token;
  }

  async clearTokens(): Promise<void> {
    await AsyncStorage.removeItem(ACCESS_TOKEN_KEY);
    await AsyncStorage.removeItem(REFRESH_TOKEN_KEY);
  }
}

export const apiService = new ApiService();
export default apiService;
