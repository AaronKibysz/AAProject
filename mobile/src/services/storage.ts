// Storage wrapper que funciona en web y nativo
// En web usa localStorage, en nativo usa expo-secure-store

import { Platform } from 'react-native';
import * as SecureStore from 'expo-secure-store';

const AsyncStorage = Platform.OS === 'web'
  ? {
      getItem: async (key: string) => {
        try {
          return localStorage.getItem(key);
        } catch {
          return null;
        }
      },
      setItem: async (key: string, value: string) => {
        try {
          localStorage.setItem(key, value);
        } catch {
          // ignore
        }
      },
      removeItem: async (key: string) => {
        try {
          localStorage.removeItem(key);
        } catch {
          // ignore
        }
      },
    }
  : {
      getItem: async (key: string) => {
        try {
          return await SecureStore.getItemAsync(key);
        } catch {
          return null;
        }
      },
      setItem: async (key: string, value: string) => {
        try {
          await SecureStore.setItemAsync(key, value);
        } catch {
          // ignore
        }
      },
      removeItem: async (key: string) => {
        try {
          await SecureStore.deleteItemAsync(key);
        } catch {
          // ignore
        }
      },
    };

export default AsyncStorage;
