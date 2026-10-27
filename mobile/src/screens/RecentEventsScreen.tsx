// Pantalla de Resultados Recientes
// Muestra las últimas carreras y eventos disputados

import React, { useState, useEffect, useCallback } from 'react';
import {
  View,
  Text,
  FlatList,
  StyleSheet,
  RefreshControl,
} from 'react-native';
import { colors, typography, spacing, borderRadius } from '../theme';
import { Card, Loading, EmptyState, Badge, PositionBadge } from '../components';
import { apiService } from '../services/api';
import { Result, Pilot } from '../types';

export default function RecentEventsScreen() {
  const [results, setResults] = useState<Result[]>([]);
  const [pilots, setPilots] = useState<Pilot[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = useCallback(async () => {
    try {
      const [resultsData, pilotsData] = await Promise.all([
        apiService.getResults({ limit: 30 }),
        apiService.getPilots({ limit: 100 }),
      ]);
      setResults(resultsData.items || resultsData);
      setPilots(pilotsData.items || pilotsData);
    } catch (error) {
      console.error('Error loading results:', error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, []);

  const onRefresh = () => {
    setRefreshing(true);
    loadData();
  };

  const getPilotName = (pilotId: number) => {
    const pilot = pilots.find((p) => p.id === pilotId);
    return pilot?.name || `Piloto #${pilotId}`;
  };

  const renderItem = ({ item }: { item: Result }) => (
    <Card style={styles.card}>
      <View style={styles.cardRow}>
        <PositionBadge position={item.position || 0} />
        <View style={styles.cardInfo}>
          <Text style={styles.pilotName}>{getPilotName(item.pilot_id)}</Text>
          <Text style={styles.circuitInfo}>
            {item.circuit_id ? `Circuito #${item.circuit_id}` : 'Circuito'}
          </Text>
        </View>
        <View style={styles.pointsContainer}>
          <Text style={styles.pointsText}>{item.points || 0}</Text>
          <Text style={styles.pointsLabel}>pts</Text>
        </View>
      </View>
    </Card>
  );

  if (loading) {
    return <Loading message="Cargando resultados..." />;
  }

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Resultados</Text>
        <Text style={styles.subtitle}>Últimas carreras disputadas</Text>
      </View>
      <FlatList
        data={results}
        renderItem={renderItem}
        keyExtractor={(item) => item.id.toString()}
        contentContainerStyle={styles.list}
        refreshControl={
          <RefreshControl
            refreshing={refreshing}
            onRefresh={onRefresh}
            tintColor={colors.primary}
            colors={[colors.primary]}
          />
        }
        ListEmptyComponent={
          <EmptyState title="Sin resultados" message="No hay resultados disponibles" icon="📊" />
        }
      />
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
  list: {
    padding: spacing.lg,
  },
  card: {
    marginBottom: spacing.sm,
  },
  cardRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.md,
  },
  cardInfo: {
    flex: 1,
  },
  pilotName: {
    fontSize: typography.lg,
    fontWeight: typography.semibold,
    color: colors.text,
  },
  circuitInfo: {
    fontSize: typography.sm,
    color: colors.textSecondary,
    marginTop: spacing.xs,
  },
  pointsContainer: {
    alignItems: 'center',
  },
  pointsText: {
    fontSize: typography.xl,
    fontWeight: typography.bold,
    color: colors.primaryLight,
    fontFamily: typography.mono,
  },
  pointsLabel: {
    fontSize: typography.xs,
    color: colors.textMuted,
  },
});
