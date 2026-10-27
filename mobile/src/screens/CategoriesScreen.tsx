// Pantalla de categorías con diseño racing

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
import { Category } from '../types';

export default function CategoriesScreen() {
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  const loadData = useCallback(async (pageNum = 1) => {
    try {
      const response = await apiService.getCategories({ page: pageNum, limit: 20 });
      const items = response.items || response;
      if (pageNum === 1) {
        setCategories(items);
      } else {
        setCategories((prev) => [...prev, ...items]);
      }
      setTotalPages(response.pages || 1);
      setPage(pageNum);
    } catch (error) {
      console.error('Error loading categories:', error);
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

  const renderItem = ({ item }: { item: Category }) => (
    <Card style={styles.card}>
      <View style={styles.cardRow}>
        <View style={styles.cardInfo}>
          <Text style={styles.cardTitle}>{item.name}</Text>
          {item.description && <Text style={styles.cardDesc}>{item.description}</Text>}
        </View>
        {item.is_ficticio && <Badge text="Muestra" color={colors.warning} />}
      </View>
    </Card>
  );

  if (loading) {
    return <Loading message="Cargando categorías..." />;
  }

  return (
    <View style={styles.container}>
      <FlatList
        data={categories}
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
          <EmptyState title="Sin categorías" message="No hay categorías disponibles" icon="📋" />
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
});
