// Sistema de diseño profesional para automovilismo-app
// Paleta de colores racing con alto contraste y coherencia visual

export const colors = {
  // === Colores de marca ===
  primary: '#E63946',          // Rojo racing (color principal)
  primaryDark: '#C1121F',      // Rojo oscuro
  primaryLight: '#FF6B6B',     // Rojo claro
  secondary: '#457B9D',        // Azul acero
  secondaryDark: '#1D3557',    // Azul marino
  secondaryLight: '#A8DADC',    // Azul claro
  accent: '#F4A261',           // Naranja dorado
  accentDark: '#E76F51',       // Naranja oscuro

  // === Fondos (dark theme) ===
  background: '#0D1117',       // Fondo principal (GitHub dark)
  backgroundElevated: '#161B22', // Fondo elevado
  surface: '#21262D',          // Superficie de cards
  surfaceHover: '#30363D',     // Superficie hover
  surfaceLight: '#30363D',    // Superficie clara (alias de surfaceHover)
  surfaceActive: '#383E47',    // Superficie activa

  // === Texto ===
  text: '#F0F6FC',            // Texto principal (blanco suave)
  textSecondary: '#8B949E',    // Texto secundario
  textMuted: '#6E7681',        // Texto atenuado
  textInverse: '#0D1117',      // Texto sobre fondos claros

  // === Bordes ===
  border: '#30363D',           // Borde principal
  borderLight: '#484F58',      // Borde claro
  borderFocus: '#E63946',      // Borde en focus

  // === Estados ===
  success: '#3FB950',          // Verde éxito
  warning: '#D29922',          // Amarillo advertencia
  error: '#F85149',            // Rojo error
  info: '#58A6FF',             // Azul info

  // === Live tracking ===
  live: '#FF4444',             // Rojo en vivo
  liveGlow: 'rgba(255, 68, 68, 0.25)',
  liveBg: 'rgba(255, 68, 68, 0.1)',

  // === Posiciones ===
  position1: '#FFD700',        // Oro
  position2: '#C0C0C0',        // Plata
  position3: '#CD7F32',        // Bronce
  positionDefault: '#8B949E',  // Default

  // === Gradientes (para uso con LinearGradient) ===
  gradientPrimary: ['#E63946', '#C1121F'],
  gradientSecondary: ['#457B9D', '#1D3557'],
  gradientDark: ['#161B22', '#0D1117'],
};

export const typography = {
  // Tamaños (escala modular 1.25)
  xs: 10,
  sm: 12,
  md: 14,
  base: 16,
  lg: 18,
  xl: 20,
  xxl: 24,
  xxxl: 30,
  display: 36,

  // Pesos
  light: '300' as const,
  regular: '400' as const,
  medium: '500' as const,
  semibold: '600' as const,
  bold: '700' as const,
  extrabold: '800' as const,
  black: '900' as const,

  // Familias
  mono: 'monospace',
  sans: 'System',
};

export const spacing = {
  xs: 4,
  sm: 8,
  md: 12,
  lg: 16,
  xl: 20,
  xxl: 24,
  xxxl: 32,
  xxxxl: 48,
};

export const borderRadius = {
  xs: 2,
  sm: 4,
  md: 8,
  lg: 12,
  xl: 16,
  xxl: 20,
  full: 9999,
};

export const shadows = {
  none: {
    shadowColor: 'transparent',
    shadowOffset: { width: 0, height: 0 },
    shadowOpacity: 0,
    shadowRadius: 0,
    elevation: 0,
  },
  sm: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.15,
    shadowRadius: 2,
    elevation: 2,
  },
  md: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.2,
    shadowRadius: 4,
    elevation: 4,
  },
  lg: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.25,
    shadowRadius: 8,
    elevation: 8,
  },
  xl: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.3,
    shadowRadius: 16,
    elevation: 12,
  },
  glow: (color: string) => ({
    shadowColor: color,
    shadowOffset: { width: 0, height: 0 },
    shadowOpacity: 0.4,
    shadowRadius: 8,
    elevation: 6,
  }),
};

// Utilidades de estilo
export const utils = {
  // Separador visual
  divider: {
    height: 1,
    backgroundColor: colors.border,
    marginVertical: spacing.md,
  },
  // Contenedor de sección
  section: {
    paddingHorizontal: spacing.lg,
    paddingVertical: spacing.md,
  },
  // Texto de sección
  sectionTitle: {
    fontSize: typography.xl,
    fontWeight: typography.bold,
    color: colors.text,
    marginBottom: spacing.md,
  },
};

export default { colors, typography, spacing, borderRadius, shadows, utils };
