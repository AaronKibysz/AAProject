// Pantalla de Historia
// Muestra todos los pilotos, circuitos y resultados históricos

import React, { useState, useEffect, useCallback } from 'react';
import {
  View,
  Text,
  FlatList,
  StyleSheet,
  RefreshControl,
  TouchableOpacity,
  TextInput,
} from 'react-native';
import { colors, typography, spacing, borderRadius } from '../theme';
import { Card, Loading, EmptyState, Badge } from '../components';
import { ScreenHeader } from '../components/ScreenHeader';
import { apiService } from '../services/api';
import { Pilot, Circuit, Category } from '../types';

type TabType = 'pilots' | 'circuits' | 'categories';

export default function HistoryScreen() {
  const [activeTab, setActiveTab] = useState<TabType>('pilots');
  const [pilots, setPilots] = useState<Pilot[]>([]);
  const [circuits, setCircuits] = useState<Circuit[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    loadData();
  }, []);

  const loadData = useCallback(async () => {
    try {
      const [pilotsData, circuitsData, catsData] = await Promise.all([
        apiService.getPilots({ limit: 100 }),
        apiService.getCircuits({ limit: 100 }),
        apiService.getCategories({ limit: 50 }),
      ]);
      setPilots(pilotsData.items || pilotsData);
      setCircuits(circuitsData.items || circuitsData);
      setCategories(catsData.items || catsData);
    } catch (error) {
      console.error('Error loading history:', error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, []);

  const onRefresh = () => {
    setRefreshing(true);
    loadData();
  };

  const filteredPilots = pilots.filter((p) =>
    p.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const filteredCircuits = circuits.filter((c) =>
    c.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const filteredCategories = categories.filter((c) =>
    c.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  if (loading) {
    return <Loading message="Cargando historia..." />;
  }

  const renderPilot = ({ item }: { item: Pilot }) => (
    <Card style={styles.card}>
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

  const renderCircuit = ({ item }: { item: Circuit }) => (
    <Card style={styles.card}>
      <View style={styles.cardRow}>
        <View style={styles.cardInfo}>
          <Text style={styles.cardTitle}>{item.name}</Text>
          {item.location && <Text style={styles.cardDesc}>{item.location}</Text>}
          {item.country && <Text style={styles.cardDesc}>{item.country}</Text>}
        </View>
        <View style={styles.rightSection}>
          {item.length_km && <Badge text={`${item.length_km} km`} color={colors.info} />}
        </View>
      </View>
    </Card>
  );

  const renderCategory = ({ item }: { item: Category }) => (
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

  return (
    <View style={styles.container}>
      <ScreenHeader title="Historia" subtitle="Pilotos, circuitos y categorías" />
      {/* Tabs */}
      <View style={styles.tabBar}>
        {(['pilots', 'circuits', 'categories'] as TabType[]).map((tab) => (
          <TouchableOpacity
            key={tab}
            style={[styles.tab, activeTab === tab && styles.tabActive]}
            onPress={() => setActiveTab(tab)}
          >
            <Text style={[styles.tabText, activeTab === tab && styles.tabTextActive]}>
              {tab === 'pilots' ? 'Pilotos' : tab === 'circuits' ? 'Circuitos' : 'Categorías'}
            </Text>
          </TouchableOpacity>
        ))}
      </View>

      {/* Búsqueda */}
      <View style={styles.searchContainer}>
        <TextInput
          style={styles.searchInput}
          placeholder={`Buscar ${activeTab === 'pilots' ? 'pilotos' : activeTab === 'circuits' ? 'circuitos' : 'categorías'}...`}
          placeholderTextColor={colors.textMuted}
          value={searchQuery}
          onChangeText={setSearchQuery}
        />
        {searchQuery.trim() === '' && (
          <Text style={styles.featuredHint}>
            Mostrando destacados. Usa el buscador para ver más.
          </Text>
        )}
      </View>

      {/* Lista - solo destacados si no hay búsqueda */}
      <FlatList
        data={
          searchQuery.trim() === ''
            ? (activeTab === 'pilots'
                ? filteredPilots.slice(0, 5)
                : activeTab === 'circuits'
                ? filteredCircuits.slice(0, 5)
                : filteredCategories.slice(0, 5))
            : (activeTab === 'pilots'
                ? filteredPilots
                : activeTab === 'circuits'
                ? filteredCircuits
                : filteredCategories)
        }
        renderItem={
          activeTab === 'pilots'
            ? renderPilot
            : activeTab === 'circuits'
            ? renderCircuit
            : renderCategory
        }
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
          <EmptyState
            title="Sin resultados"
            message="No se encontraron elementos"
            icon="🔍"
          />
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
  tabBar: {
    flexDirection: 'row',
    backgroundColor: colors.surface,
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
  },
  tab: {
    flex: 1,
    paddingVertical: spacing.md,
    alignItems: 'center',
  },
  tabActive: {
    borderBottomWidth: 2,
    borderBottomColor: colors.primary,
  },
  tabText: {
    fontSize: typography.md,
    color: colors.textSecondary,
    fontWeight: typography.medium,
  },
  tabTextActive: {
    color: colors.primaryLight,
    fontWeight: typography.semibold,
  },
  searchContainer: {
    padding: spacing.lg,
  },
  searchInput: {
    backgroundColor: colors.surfaceLight,
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: borderRadius.md,
    padding: spacing.md,
    fontSize: typography.md,
    color: colors.text,
  },
  featuredHint: {
    fontSize: typography.sm,
    color: colors.textMuted,
    marginTop: spacing.sm,
    fontStyle: 'italic',
  },
  list: {
    padding: spacing.lg,
    paddingTop: 0,
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
