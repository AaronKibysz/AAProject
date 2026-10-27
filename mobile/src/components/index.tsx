// Componentes reutilizables con el tema de automovilismo
// Estilo racing dark con foco en live tracking

import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ActivityIndicator,
} from 'react-native';
import { colors, typography, spacing, borderRadius, shadows } from '../theme';

// --- Card ---
export function Card({ children, style, onPress }: { children: React.ReactNode; style?: any; onPress?: () => void }) {
  const Container = onPress ? TouchableOpacity : View;
  return (
    <Container
      style={[styles.card, style]}
      onPress={onPress}
      activeOpacity={0.7}
    >
      {children}
    </Container>
  );
}

// --- Button ---
export function Button({
  title,
  onPress,
  variant = 'primary',
  size = 'md',
  loading = false,
  disabled = false,
  style,
}: {
  title: string;
  onPress: () => void;
  variant?: 'primary' | 'secondary' | 'danger' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
  disabled?: boolean;
  style?: any;
}) {
  const bgColor = {
    primary: colors.primary,
    secondary: colors.secondary,
    danger: colors.error,
    ghost: 'transparent',
  }[variant];

  const textColor = variant === 'ghost' ? colors.primary : colors.text;
  const padding = { sm: 8, md: 12, lg: 16 }[size];
  const fontSize = { sm: typography.sm, md: typography.md, lg: typography.lg }[size];

  return (
    <TouchableOpacity
      style={[
        styles.button,
        { backgroundColor: bgColor, paddingVertical: padding, paddingHorizontal: padding * 1.5 },
        disabled && styles.buttonDisabled,
        style,
      ]}
      onPress={onPress}
      disabled={disabled || loading}
      activeOpacity={0.7}
    >
      {loading ? (
        <ActivityIndicator color={textColor} size="small" />
      ) : (
        <Text style={[styles.buttonText, { color: textColor, fontSize }]}>{title}</Text>
      )}
    </TouchableOpacity>
  );
}

// --- Badge ---
export function Badge({ text, color = colors.primary, style }: { text: string; color?: string; style?: any }) {
  return (
    <View style={[styles.badge, { backgroundColor: color + '20', borderColor: color }, style]}>
      <Text style={[styles.badgeText, { color }]}>{text}</Text>
    </View>
  );
}

// --- LiveBadge ---
export function LiveBadge({ style }: { style?: any }) {
  return (
    <View style={[styles.liveBadge, style]}>
      <View style={styles.liveDot} />
      <Text style={styles.liveText}>EN VIVO</Text>
    </View>
  );
}

// --- PositionBadge ---
export function PositionBadge({ position, style }: { position: number; style?: any }) {
  const color =
    position === 1 ? colors.position1 :
    position === 2 ? colors.position2 :
    position === 3 ? colors.position3 :
    colors.textSecondary;

  return (
    <View style={[styles.positionBadge, { borderColor: color }, style]}>
      <Text style={[styles.positionText, { color }]}>{position}</Text>
    </View>
  );
}

// --- TimeDisplay ---
export function TimeDisplay({ time, style }: { time: string; style?: any }) {
  return (
    <Text style={[styles.timeDisplay, style]}>{time}</Text>
  );
}

// --- Loading ---
export function Loading({ message = 'Cargando...' }: { message?: string }) {
  return (
    <View style={styles.loadingContainer}>
      <ActivityIndicator size="large" color={colors.primary} />
      <Text style={styles.loadingText}>{message}</Text>
    </View>
  );
}

// --- EmptyState ---
export function EmptyState({ title, message, icon }: { title: string; message?: string; icon?: string }) {
  return (
    <View style={styles.emptyContainer}>
      {icon && <Text style={styles.emptyIcon}>{icon}</Text>}
      <Text style={styles.emptyTitle}>{title}</Text>
      {message && <Text style={styles.emptyMessage}>{message}</Text>}
    </View>
  );
}

// --- SectionHeader ---
export function SectionHeader({ title, subtitle }: { title: string; subtitle?: string }) {
  return (
    <View style={styles.sectionHeader}>
      <Text style={styles.sectionTitle}>{title}</Text>
      {subtitle && <Text style={styles.sectionSubtitle}>{subtitle}</Text>}
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: colors.surface,
    borderRadius: borderRadius.lg,
    padding: spacing.lg,
    marginBottom: spacing.md,
    borderWidth: 1,
    borderColor: colors.border,
    ...shadows.md,
  },
  button: {
    borderRadius: borderRadius.md,
    alignItems: 'center',
    justifyContent: 'center',
  },
  buttonDisabled: {
    opacity: 0.5,
  },
  buttonText: {
    fontWeight: typography.semibold,
  },
  badge: {
    paddingHorizontal: spacing.sm,
    paddingVertical: spacing.xs,
    borderRadius: borderRadius.sm,
    borderWidth: 1,
    alignSelf: 'flex-start',
  },
  badgeText: {
    fontSize: typography.xs,
    fontWeight: typography.semibold,
  },
  liveBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.live + '20',
    paddingHorizontal: spacing.sm,
    paddingVertical: spacing.xs,
    borderRadius: borderRadius.sm,
    borderWidth: 1,
    borderColor: colors.live,
  },
  liveDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: colors.live,
    marginRight: spacing.xs,
  },
  liveText: {
    color: colors.live,
    fontSize: typography.xs,
    fontWeight: typography.bold,
  },
  positionBadge: {
    width: 32,
    height: 32,
    borderRadius: 16,
    borderWidth: 2,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: colors.surfaceLight,
  },
  positionText: {
    fontSize: typography.md,
    fontWeight: typography.bold,
    fontFamily: typography.mono,
  },
  timeDisplay: {
    fontFamily: typography.mono,
    fontSize: typography.md,
    color: colors.text,
    fontWeight: typography.medium,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: colors.background,
  },
  loadingText: {
    marginTop: spacing.md,
    fontSize: typography.md,
    color: colors.textSecondary,
  },
  emptyContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: spacing.xxl,
  },
  emptyIcon: {
    fontSize: 48,
    marginBottom: spacing.md,
  },
  emptyTitle: {
    fontSize: typography.xl,
    fontWeight: typography.semibold,
    color: colors.text,
    textAlign: 'center',
    marginBottom: spacing.sm,
  },
  emptyMessage: {
    fontSize: typography.md,
    color: colors.textSecondary,
    textAlign: 'center',
  },
  sectionHeader: {
    marginBottom: spacing.md,
  },
  sectionTitle: {
    fontSize: typography.xl,
    fontWeight: typography.bold,
    color: colors.text,
  },
  sectionSubtitle: {
    fontSize: typography.sm,
    color: colors.textSecondary,
    marginTop: spacing.xs,
  },
});
