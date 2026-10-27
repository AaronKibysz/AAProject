// Tipos TypeScript para la aplicación mobile de automovilismo
// Corresponden a los schemas del backend (Pydantic)

export interface Category {
  id: number;
  name: string;
  description?: string;
  is_ficticio: boolean;
  created_at?: string;
}

export interface Pilot {
  id: number;
  name: string;
  number?: number;
  team?: string;
  category_id?: number;
  is_ficticio: boolean;
  created_at?: string;
}

export interface Circuit {
  id: number;
  name: string;
  location?: string;
  country?: string;
  length_km?: number;
  is_ficticio: boolean;
  created_at?: string;
}

export interface Season {
  id: number;
  year: number;
  category_id: number;
  is_ficticio: boolean;
  created_at?: string;
}

export interface Result {
  id: number;
  season_id: number;
  pilot_id: number;
  circuit_id: number;
  position?: number;
  points?: number;
  is_ficticio: boolean;
  created_at?: string;
}

export interface Session {
  id: number;
  season_id: number;
  circuit_id: number;
  date?: string;
  session_type?: string;
  is_ficticio: boolean;
  created_at?: string;
}

export interface User {
  id: number;
  email: string;
  username: string;
  full_name?: string;
  is_active: boolean;
  is_ficticio: boolean;
  created_at?: string;
}

export interface Favorite {
  id: number;
  user_id: number;
  resource_type: string;
  resource_id: number;
  created_at?: string;
}

export interface Token {
  access_token: string;
  token_type: string;
  expires_in: number;
  refresh_token?: string;
  refresh_expires_in?: number;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  limit: number;
  pages: number;
}

export interface SearchResult {
  resource_type: string;
  resource_id: number;
  name: string;
  description?: string;
  is_ficticio: boolean;
}

export interface ApiError {
  detail: string;
}
