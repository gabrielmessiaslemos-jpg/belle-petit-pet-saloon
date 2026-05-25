import { MD3DarkTheme } from 'react-native-paper';
import type { MD3Theme } from 'react-native-paper';

// ─── Belle Petit Color Palette ───────────────────────────────────────────────
export const Colors = {
  // Backgrounds
  background: '#121212',
  surface: '#1E1E1E',
  surfaceVariant: '#2A2A2A',
  elevated: '#252525',

  // Brand
  primary: '#C9A84C',       // Dourado principal
  primaryLight: '#E8C97A',  // Dourado claro
  primaryDark: '#9B7A2E',   // Dourado escuro
  primaryContainer: '#2C2410', // Fundo dourado suave

  // Text
  text: '#FFFFFF',
  textSecondary: '#9E9E9E',
  textMuted: '#5E5E5E',
  onPrimary: '#121212',     // Texto sobre botões dourados

  // Status
  success: '#4CAF50',
  successContainer: '#1B3B1C',
  warning: '#FF9800',
  warningContainer: '#3B2800',
  error: '#CF6679',
  errorContainer: '#3B1018',
  info: '#64B5F6',
  infoContainer: '#0D2B45',

  // Appointment Status
  statusPending: '#FF9800',
  statusConfirmed: '#4CAF50',
  statusDone: '#9E9E9E',
  statusCancelled: '#CF6679',

  // Divider
  divider: '#2E2E2E',
  border: '#333333',
};

// ─── Paper Theme (Dark + Gold) ───────────────────────────────────────────────
export const AppTheme: MD3Theme = {
  ...MD3DarkTheme,
  colors: {
    ...MD3DarkTheme.colors,
    primary: Colors.primary,
    primaryContainer: Colors.primaryContainer,
    onPrimary: Colors.onPrimary,
    onPrimaryContainer: Colors.primaryLight,
    secondary: Colors.primaryLight,
    secondaryContainer: Colors.primaryContainer,
    background: Colors.background,
    surface: Colors.surface,
    surfaceVariant: Colors.surfaceVariant,
    onSurface: Colors.text,
    onSurfaceVariant: Colors.textSecondary,
    error: Colors.error,
    errorContainer: Colors.errorContainer,
    outline: Colors.border,
    outlineVariant: Colors.divider,
  },
};

// ─── Typography ──────────────────────────────────────────────────────────────
export const Typography = {
  heading1: { fontSize: 28, fontWeight: '700' as const, color: Colors.text },
  heading2: { fontSize: 22, fontWeight: '600' as const, color: Colors.text },
  heading3: { fontSize: 18, fontWeight: '600' as const, color: Colors.text },
  body:     { fontSize: 15, fontWeight: '400' as const, color: Colors.text },
  bodySmall:{ fontSize: 13, fontWeight: '400' as const, color: Colors.textSecondary },
  caption:  { fontSize: 11, fontWeight: '400' as const, color: Colors.textMuted },
  label:    { fontSize: 13, fontWeight: '600' as const, color: Colors.primary },
};

// ─── Spacing ─────────────────────────────────────────────────────────────────
export const Spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
  xxl: 48,
};

// ─── Border Radius ───────────────────────────────────────────────────────────
export const Radius = {
  sm: 6,
  md: 12,
  lg: 18,
  xl: 24,
  full: 999,
};

// ─── Shadows ─────────────────────────────────────────────────────────────────
export const Shadow = {
  gold: {
    shadowColor: Colors.primary,
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 8,
    elevation: 5,
  },
  dark: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.4,
    shadowRadius: 6,
    elevation: 4,
  },
};
