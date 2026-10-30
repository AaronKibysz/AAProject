// Favoritos locales (sin cuentas ni sincronización en la nube)
// Se guardan en el dispositivo usando el storage local (AsyncStorage/SecureStore).

import AsyncStorage from './storage';

const FAVORITES_KEY = 'local_favorites';

export interface LocalFavorite {
  resource_type: 'pilot' | 'circuit' | 'category' | 'season';
  resource_id: number;
  created_at: string;
}

class FavoritesService {
  async getAll(): Promise<LocalFavorite[]> {
    const raw = await AsyncStorage.getItem(FAVORITES_KEY);
    if (!raw) return [];
    try {
      return JSON.parse(raw) as LocalFavorite[];
    } catch {
      return [];
    }
  }

  async isFavorite(resourceType: LocalFavorite['resource_type'], resourceId: number): Promise<boolean> {
    const list = await this.getAll();
    return list.some((f) => f.resource_type === resourceType && f.resource_id === resourceId);
  }

  async add(resourceType: LocalFavorite['resource_type'], resourceId: number): Promise<LocalFavorite> {
    const list = await this.getAll();
    const exists = list.some((f) => f.resource_type === resourceType && f.resource_id === resourceId);
    if (exists) {
      return list.find((f) => f.resource_type === resourceType && f.resource_id === resourceId)!;
    }
    const fav: LocalFavorite = {
      resource_type: resourceType,
      resource_id: resourceId,
      created_at: new Date().toISOString(),
    };
    list.push(fav);
    await AsyncStorage.setItem(FAVORITES_KEY, JSON.stringify(list));
    return fav;
  }

  async remove(resourceType: LocalFavorite['resource_type'], resourceId: number): Promise<void> {
    const list = await this.getAll();
    const filtered = list.filter((f) => !(f.resource_type === resourceType && f.resource_id === resourceId));
    await AsyncStorage.setItem(FAVORITES_KEY, JSON.stringify(filtered));
  }

  async clear(): Promise<void> {
    await AsyncStorage.removeItem(FAVORITES_KEY);
  }
}

export const favoritesService = new FavoritesService();
export default favoritesService;