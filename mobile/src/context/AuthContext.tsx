// Contexto de autenticación deshabilitado para el MVP
// El MVP no incluye cuentas de usuario; los favoritos se guardan localmente.

import React, { createContext, useContext, useState, ReactNode } from 'react';

interface AuthContextType {
  user: null;
  isLoading: boolean;
  isAuthenticated: false;
  login: (email: string, password: string) => Promise<void>;
  register: (data: { email: string; username: string; password: string; full_name?: string }) => Promise<void>;
  logout: () => Promise<void>;
  logoutAll: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const disabled = async () => {
  throw new Error('La autenticación está deshabilitada en esta versión (MVP sin cuentas).');
};

export function AuthProvider({ children }: { children: ReactNode }) {
  const [isLoading] = useState(false);

  return (
    <AuthContext.Provider
      value={{
        user: null,
        isLoading,
        isAuthenticated: false,
        login: disabled,
        register: disabled,
        logout: async () => {},
        logoutAll: async () => {},
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}