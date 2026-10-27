// Pantalla de pilotos con diseño racing

import React, { useState, useEffect, useCallback } from 'react';
import {
  View,
  Text,
  FlatList,
  StyleSheet,
  RefreshControl,
} from 'react-native';
import { colors, typography, spacing, borderRadius } from '../theme';
import { Card, Loading, EmptyState, Badge } from '../components';
import { apiService } from '../services/api';
import { Pilot } from '../types';

export default function PilotsScreen({ navigation }: any) {
  const [pilots, setPilots] = useState<Pilot[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  const loadData = useCallback(async (pageNum = 1) => {
    try {
      const response = await apiService.getPilots({ page: pageNum, limit: 20 });
      const items = response.items || response;
      if (pageNum === 1) {
        setPilots(items);
      } else {
        setPilots((prev) => [...prev, ...items]);
      }
      setTotalPages(response.pages || 1);
      setPage(pageNum);
    } catch (error) {
      console.error('Error loading pilots:', error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, []);

  useEffect(() => {
    loadData(1);
  }, [loadData]);

  const onRefresh = () => {
    setRefreshing(true);
    loadData(1);
  };

  const loadMore = () => {
    if (page < totalPages) {
      loadData(page + 1);
    }
  };

  const renderItem = ({ item }: { item: Pilot }) => (
    <Card style={styles.card} onPress={() => navigation.getParent()?.navigate('PilotDetail', { pilot: item })}>
      <View style={styles.cardRow}>
        <View style={styles.cardInfo}>
          <Text style={styles.cardTitle}>{item.name}</Text>
          {item.team && <Text style={styles.cardDesc}>{item.team}</Text>}
        </View>
        <View style={styles.rightSection}>
          {item.number && (
            <View style={styles.numberBadge}>
              <Text style={styles.numberText}>#{item.number}</Text>
            </View>
          )}
          {item.is_ficticio && <Badge text="Muestra" color={colors.warning} />}
        </View>
      </View>
    </Card>
  );

  if (loading) {
    return <Loading message="Cargando pilotos..." />;
  }

  return (
    <View style={styles.container}>
      <FlatList
        data={pilots}
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
        onEndReached={loadMore}
        onEndReachedThreshold={0.5}
        ListEmptyComponent={
          <EmptyState title="Sin pilotos" message="No hay pilotos disponibles" icon="🏎️" />
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
  list: {
    padding: spacing.lg,
  },
  card: {
    marginBottom: spacing.sm,
  },
  cardRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  cardInfo: {
    flex: 1,
  },
  cardTitle: {
    fontSize: typography.lg,
    fontWeight: typography.semibold,
    color: colors.text,
  },
  cardDesc: {
    fontSize: typography.sm,
    color: colors.textSecondary,
    marginTop: spacing.xs,
  },
  rightSection: {
    alignItems: 'flex-end',
    gap: spacing.xs,
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
