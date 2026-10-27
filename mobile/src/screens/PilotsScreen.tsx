// Pantalla de pilotos
// Muestra lista paginada de pilotos

import React, { useState, useEffect, useCallback } from 'react';
import {
  View,
  Text,
  FlatList,
  StyleSheet,
  ActivityIndicator,
  RefreshControl,
} from 'react-native';
import { apiService } from '../services/api';
import { Pilot } from '../types';

export default function PilotsScreen() {
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
    <View style={styles.card}>
      <View style={styles.cardHeader}>
        <Text style={styles.cardTitle}>{item.name}</Text>
        {item.number && <Text style={styles.number}>#{item.number}</Text>}
      </View>
      {item.team && <Text style={styles.cardDesc}>{item.team}</Text>}
      {item.is_ficticio && <Text style={styles.ficticioBadge}>Muestra</Text>}
    </View>
  );

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#1976d2" />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <FlatList
        data={pilots}
        renderItem={renderItem}
        keyExtractor={(item) => item.id.toString()}
        contentContainerStyle={styles.list}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
        onEndReached={loadMore}
        onEndReachedThreshold={0.5}
        ListEmptyComponent={
          <Text style={styles.emptyText}>No hay pilotos disponibles</Text>
        }
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  list: {
    padding: 16,
  },
  card: {
    backgroundColor: 'white',
    padding: 16,
    borderRadius: 8,
    marginBottom: 12,
    elevation: 2,
  },
  cardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#333',
  },
  number: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#1976d2',
  },
  cardDesc: {
    fontSize: 14,
    color: '#666',
    marginTop: 4,
  },
  ficticioBadge: {
    fontSize: 12,
    color: '#ff9800',
    marginTop: 4,
    fontWeight: '500',
  },
  emptyText: {
    textAlign: 'center',
    color: '#666',
    marginTop: 40,
    fontSize: 16,
  },
});
