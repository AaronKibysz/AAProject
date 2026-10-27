// Pantalla de Live Tracking
// Muestra los eventos en vivo con tracking en tiempo real

import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Animated,
} from 'react-native';
import { colors, typography, spacing, borderRadius } from '../theme';
import { Card, Loading, EmptyState, LiveBadge } from '../components';

export default function LiveScreen() {
  const [liveEvents, setLiveEvents] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  // Simular carga de eventos en vivo
  useEffect(() => {
    // Por ahora no hay eventos en vivo
    setLiveEvents([]);
    setLoading(false);
  }, []);

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <View style={styles.headerRow}>
          <Text style={styles.title}>En vivo</Text>
          <LiveBadge />
        </View>
        <Text style={styles.subtitle}>Tracking en tiempo real</Text>
      </View>

      {loading ? (
        <Loading message="Buscando eventos en vivo..." />
      ) : liveEvents.length === 0 ? (
        <View style={styles.emptyContainer}>
          <View style={styles.emptyIconContainer}>
            <Text style={styles.emptyIcon}>🏁</Text>
          </View>
          <Text style={styles.emptyTitle}>No hay carreras en vivo</Text>
          <Text style={styles.emptyMessage}>
            Cuando comience una carrera, aparecerá aquí con tracking en tiempo real
          </Text>
          <View style={styles.featuresContainer}>
            <Text style={styles.featuresTitle}>Próximamente:</Text>
            <Text style={styles.featureItem}>• Posiciones en tiempo real</Text>
            <Text style={styles.featureItem}>• Tiempos por vuelta</Text>
            <Text style={styles.featureItem}>• Alertas de adelantamientos</Text>
            <Text style={styles.featureItem}>• Clasificación en vivo</Text>
          </View>
        </View>
      ) : (
        <ScrollView style={styles.content}>
          {liveEvents.map((event, index) => (
            <Card key={index} style={styles.eventCard}>
              <Text style={styles.eventTitle}>{event.title}</Text>
              <Text style={styles.eventDesc}>{event.description}</Text>
            </Card>
          ))}
        </ScrollView>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  header: {
    backgroundColor: colors.surface,
    padding: spacing.xl,
    paddingTop: spacing.xxxl,
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
  },
  headerRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  title: {
    fontSize: typography.xxxl,
    fontWeight: typography.black,
    color: colors.text,
  },
  subtitle: {
    fontSize: typography.md,
    color: colors.textSecondary,
    marginTop: spacing.xs,
  },
  content: {
    flex: 1,
    padding: spacing.lg,
  },
  emptyContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: spacing.xxl,
  },
  emptyIconContainer: {
    width: 100,
    height: 100,
    borderRadius: 50,
    backgroundColor: colors.liveBg,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: spacing.lg,
    borderWidth: 2,
    borderColor: colors.live,
  },
  emptyIcon: {
    fontSize: 48,
  },
  emptyTitle: {
    fontSize: typography.xxl,
    fontWeight: typography.bold,
    color: colors.text,
    textAlign: 'center',
    marginBottom: spacing.sm,
  },
  emptyMessage: {
    fontSize: typography.md,
    color: colors.textSecondary,
    textAlign: 'center',
    marginBottom: spacing.xl,
  },
  featuresContainer: {
    backgroundColor: colors.surface,
    borderRadius: borderRadius.lg,
    padding: spacing.lg,
    width: '100%',
    borderWidth: 1,
    borderColor: colors.border,
  },
  featuresTitle: {
    fontSize: typography.md,
    fontWeight: typography.semibold,
    color: colors.text,
    marginBottom: spacing.sm,
  },
  featureItem: {
    fontSize: typography.sm,
    color: colors.textSecondary,
    marginBottom: spacing.xs,
  },
  eventCard: {
    marginBottom: spacing.md,
  },
  eventTitle: {
    fontSize: typography.lg,
    fontWeight: typography.semibold,
    color: colors.text,
  },
  eventDesc: {
    fontSize: typography.sm,
    color: colors.textSecondary,
    marginTop: spacing.xs,
  },
});
