// Pantalla de Búsqueda Global
// Permite buscar en todas las entidades del sistema

import React, { useState, useEffect, useCallback } from 'react';
import {
  View,
  Text,
  FlatList,
  StyleSheet,
  RefreshControl,
  TouchableOpacity,
  TextInput,
  Keyboard,
} from 'react-native';
import { colors, typography, spacing, borderRadius } from '../theme';
import { Card, Loading, EmptyState, Badge } from '../components';
import { apiService } from '../services/api';
import { SearchResult } from '../types';

export default function SearchScreen() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);

  const performSearch = useCallback(async (searchQuery: string) => {
    if (!searchQuery.trim()) {
      setResults([]);
      setSearched(false);
      return;
    }

    setLoading(true);
    try {
      const response = await apiService.search(searchQuery);
      setResults(response || []);
      setSearched(true);
    } catch (error) {
      console.error('Error searching:', error);
      setResults([]);
      setSearched(true);
    } finally {
      setLoading(false);
    }
  }, []);

  const handleSearch = () => {
    Keyboard.dismiss();
    performSearch(query);
  };

  const getIcon = (type: string) => {
    switch (type) {
      case 'category': return '📋';
      case 'pilot': return '🏎️';
      case 'circuit': return '🏁';
      case 'season': return '📅';
      case 'result': return '📊';
      case 'session': return '🕐';
      default: return '🔍';
    }
  };

  const getTypeLabel = (type: string) => {
    switch (type) {
      case 'category': return 'Categoría';
      case 'pilot': return 'Piloto';
      case 'circuit': return 'Circuito';
      case 'season': return 'Temporada';
      case 'result': return 'Resultado';
      case 'session': return 'Sesión';
      default: return type;
    }
  };

  const renderItem = ({ item }: { item: SearchResult }) => (
    <Card style={styles.resultCard}>
      <View style={styles.resultRow}>
        <Text style={styles.resultIcon}>{getIcon(item.resource_type)}</Text>
        <View style={styles.resultInfo}>
          <Text style={styles.resultName}>{item.name}</Text>
          {item.description && <Text style={styles.resultDesc}>{item.description}</Text>}
          <Badge text={getTypeLabel(item.resource_type)} color={colors.primary} />
        </View>
        {item.is_ficticio && <Badge text="Muestra" color={colors.warning} />}
      </View>
    </Card>
  );

  return (
    <View style={styles.container}>
      {/* Barra de búsqueda */}
      <View style={styles.searchBar}>
        <TextInput
          style={styles.searchInput}
          placeholder="Buscar pilotos, circuitos, categorías..."
          placeholderTextColor={colors.textMuted}
          value={query}
          onChangeText={setQuery}
          onSubmitEditing={handleSearch}
          returnKeyType="search"
          autoCapitalize="none"
        />
        <TouchableOpacity style={styles.searchButton} onPress={handleSearch}>
          <Text style={styles.searchButtonText}>🔍</Text>
        </TouchableOpacity>
      </View>

      {loading ? (
        <Loading message="Buscando..." />
      ) : searched && results.length === 0 ? (
        <EmptyState
          title="Sin resultados"
          message={`No se encontraron resultados para "${query}"`}
          icon="🔍"
        />
      ) : !searched ? (
        <EmptyState
          title="Busca en todo"
          message="Pilotos, circuitos, categorías, temporadas y más"
          icon="🏁"
        />
      ) : (
        <FlatList
          data={results}
          renderItem={renderItem}
          keyExtractor={(item, index) => `${item.resource_type}-${item.resource_id}-${index}`}
          contentContainerStyle={styles.list}
          ListHeaderComponent={
            <Text style={styles.resultsCount}>
              {results.length} resultado{results.length !== 1 ? 's' : ''} encontrado{results.length !== 1 ? 's' : ''}
            </Text>
          }
        />
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  searchBar: {
    flexDirection: 'row',
    padding: spacing.lg,
    gap: spacing.sm,
  },
  searchInput: {
    flex: 1,
    backgroundColor: colors.surfaceLight,
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: borderRadius.md,
    padding: spacing.md,
    fontSize: typography.md,
    color: colors.text,
  },
  searchButton: {
    backgroundColor: colors.primary,
    borderRadius: borderRadius.md,
    paddingHorizontal: spacing.lg,
    justifyContent: 'center',
    alignItems: 'center',
  },
  searchButtonText: {
    fontSize: typography.lg,
  },
  list: {
    padding: spacing.lg,
    paddingTop: 0,
  },
  resultsCount: {
    fontSize: typography.sm,
    color: colors.textSecondary,
    marginBottom: spacing.md,
  },
  resultCard: {
    marginBottom: spacing.sm,
  },
  resultRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.md,
  },
  resultIcon: {
    fontSize: 24,
  },
  resultInfo: {
    flex: 1,
    gap: spacing.xs,
  },
  resultName: {
    fontSize: typography.lg,
    fontWeight: typography.semibold,
    color: colors.text,
  },
  resultDesc: {
    fontSize: typography.sm,
    color: colors.textSecondary,
  },
});
