// Pantalla de circuitos con diseño racing

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
import { Circuit } from '../types';

export default function CircuitsScreen({ navigation }: any) {
  const [circuits, setCircuits] = useState<Circuit[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  const loadData = useCallback(async (pageNum = 1) => {
    try {
      const response = await apiService.getCircuits({ page: pageNum, limit: 20 });
      const items = response.items || response;
      if (pageNum === 1) {
        setCircuits(items);
      } else {
        setCircuits((prev) => [...prev, ...items]);
      }
      setTotalPages(response.pages || 1);
      setPage(pageNum);
    } catch (error) {
      console.error('Error loading circuits:', error);
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

  const renderItem = ({ item }: { item: Circuit }) => (
    <Card style={styles.card} onPress={() => navigation.getParent()?.navigate('CircuitDetail', { circuit: item })}>
      <View style={styles.cardRow}>
        <View style={styles.cardInfo}>
          <Text style={styles.cardTitle}>{item.name}</Text>
          {item.location && <Text style={styles.cardDesc}>{item.location}</Text>}
          {item.country && <Text style={styles.cardDesc}>{item.country}</Text>}
        </View>
        <View style={styles.rightSection}>
          {item.length_km && <Badge text={`${item.length_km} km`} color={colors.info} />}
          {item.is_ficticio && <Badge text="Muestra" color={colors.warning} />}
        </View>
      </View>
    </Card>
  );

  if (loading) {
    return <Loading message="Cargando circuitos..." />;
  }

  return (
    <View style={styles.container}>
      <FlatList
        data={circuits}
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
          <EmptyState title="Sin circuitos" message="No hay circuitos disponibles" icon="🏁" />
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
});
