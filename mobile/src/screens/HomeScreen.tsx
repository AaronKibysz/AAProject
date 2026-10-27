// Pantalla de inicio - Live Tracking
// Muestra las carreras en vivo y accesos rápidos

import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
} from 'react-native';
import { colors, typography, spacing, borderRadius } from '../theme';
import { Card, LiveBadge, Badge, Loading, EmptyState } from '../components';
import { apiService } from '../services/api';
import { Category, Pilot, Circuit } from '../types';

export default function HomeScreen({ navigation }: any) {
  const [categories, setCategories] = useState<Category[]>([]);
  const [pilots, setPilots] = useState<Pilot[]>([]);
  const [circuits, setCircuits] = useState<Circuit[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [cats, pilotsData, circuitsData] = await Promise.all([
        apiService.getCategories({ limit: 5 }),
        apiService.getPilots({ limit: 5 }),
        apiService.getCircuits({ limit: 5 }),
      ]);
      setCategories(cats.items || cats);
      setPilots(pilotsData.items || pilotsData);
      setCircuits(circuitsData.items || circuitsData);
    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <Loading message="Cargando datos..." />;
  }

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      {/* Header */}
      <View style={styles.header}>
        <View style={styles.headerRow}>
          <View>
            <Text style={styles.title}>🏁 Automovilismo</Text>
            <Text style={styles.subtitle}>Turismo Carretera y más</Text>
          </View>
          <View style={styles.headerButtons}>
            <TouchableOpacity
              style={styles.headerButton}
              onPress={() => navigation.navigate('Search')}
            >
              <Text style={styles.headerButtonText}>🔍</Text>
            </TouchableOpacity>
            <TouchableOpacity
              style={styles.headerButton}
              onPress={() => navigation.navigate('Favorites')}
            >
              <Text style={styles.headerButtonText}>⭐</Text>
            </TouchableOpacity>
          </View>
        </View>
      </View>

      {/* Live Section */}
      <View style={styles.section}>
        <View style={styles.sectionHeader}>
          <Text style={styles.sectionTitle}>🔴 En Vivo</Text>
          <LiveBadge />
        </View>
        <Card style={styles.liveCard}>
          <Text style={styles.liveCardTitle}>Próxima carrera</Text>
          <Text style={styles.liveCardDesc}>
            No hay carreras en vivo en este momento
          </Text>
          <Text style={styles.liveCardHint}>
            Las carreras aparecerán aquí cuando estén en curso
          </Text>
        </Card>
      </View>

      {/* Categorías */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Categorías</Text>
        {categories.length === 0 ? (
          <EmptyState title="Sin categorías" message="No hay categorías disponibles" icon="📋" />
        ) : (
          categories.map((cat) => (
            <Card key={cat.id} style={styles.itemCard}>
              <View style={styles.itemRow}>
                <View style={styles.itemInfo}>
                  <Text style={styles.itemTitle}>{cat.name}</Text>
                  {cat.description && <Text style={styles.itemDesc}>{cat.description}</Text>}
                </View>
                {cat.is_ficticio && <Badge text="Muestra" color={colors.warning} />}
              </View>
            </Card>
          ))
        )}
      </View>

      {/* Pilotos */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Pilotos Destacados</Text>
        {pilots.length === 0 ? (
          <EmptyState title="Sin pilotos" message="No hay pilotos disponibles" icon="🏎️" />
        ) : (
          pilots.map((pilot) => (
            <Card key={pilot.id} style={styles.itemCard}>
              <View style={styles.itemRow}>
                <View style={styles.itemInfo}>
                  <Text style={styles.itemTitle}>{pilot.name}</Text>
                  {pilot.team && <Text style={styles.itemDesc}>{pilot.team}</Text>}
                </View>
                {pilot.number && (
                  <View style={styles.numberBadge}>
                    <Text style={styles.numberText}>#{pilot.number}</Text>
                  </View>
                )}
              </View>
            </Card>
          ))
        )}
      </View>

      {/* Circuitos */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Circuitos</Text>
        {circuits.length === 0 ? (
          <EmptyState title="Sin circuitos" message="No hay circuitos disponibles" icon="🏁" />
        ) : (
          circuits.map((circuit) => (
            <Card key={circuit.id} style={styles.itemCard}>
              <View style={styles.itemRow}>
                <View style={styles.itemInfo}>
                  <Text style={styles.itemTitle}>{circuit.name}</Text>
                  {circuit.location && <Text style={styles.itemDesc}>{circuit.location}</Text>}
                </View>
                {circuit.length_km && (
                  <Badge text={`${circuit.length_km} km`} color={colors.info} />
                )}
              </View>
            </Card>
          ))
        )}
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  content: {
    paddingBottom: spacing.xxxl,
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
  headerButtons: {
    flexDirection: 'row',
    gap: spacing.sm,
  },
  headerButton: {
    width: 40,
    height: 40,
    borderRadius: borderRadius.full,
    backgroundColor: colors.surfaceLight,
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 1,
    borderColor: colors.border,
  },
  headerButtonText: {
    fontSize: typography.lg,
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
  section: {
    padding: spacing.lg,
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: spacing.md,
  },
  sectionTitle: {
    fontSize: typography.xl,
    fontWeight: typography.bold,
    color: colors.text,
  },
  liveCard: {
    borderLeftWidth: 3,
    borderLeftColor: colors.live,
  },
  liveCardTitle: {
    fontSize: typography.lg,
    fontWeight: typography.semibold,
    color: colors.text,
    marginBottom: spacing.xs,
  },
  liveCardDesc: {
    fontSize: typography.md,
    color: colors.textSecondary,
    marginBottom: spacing.xs,
  },
  liveCardHint: {
    fontSize: typography.sm,
    color: colors.textMuted,
    fontStyle: 'italic',
  },
  itemCard: {
    marginBottom: spacing.sm,
  },
  itemRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  itemInfo: {
    flex: 1,
  },
  itemTitle: {
    fontSize: typography.lg,
    fontWeight: typography.semibold,
    color: colors.text,
  },
  itemDesc: {
    fontSize: typography.sm,
    color: colors.textSecondary,
    marginTop: spacing.xs,
  },
  numberBadge: {
    backgroundColor: colors.primary + '30',
    paddingHorizontal: spacing.sm,
    paddingVertical: spacing.xs,
    borderRadius: borderRadius.sm,
    borderWidth: 1,
    borderColor: colors.primary,
  },
  numberText: {
    color: colors.primaryLight,
    fontSize: typography.md,
    fontWeight: typography.bold,
    fontFamily: typography.mono,
  },
});
