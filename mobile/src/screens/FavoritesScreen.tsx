// Pantalla de Favoritos
// Muestra los recursos guardados por el usuario (requiere autenticación)

import React, { useState, useEffect, useCallback } from 'react';
import {
  View,
  Text,
  FlatList,
  StyleSheet,
  RefreshControl,
  TouchableOpacity,
  Alert,
} from 'react-native';
import { colors, typography, spacing, borderRadius } from '../theme';
import { Card, Loading, EmptyState, Badge, Button } from '../components';
import { apiService } from '../services/api';
import { Favorite } from '../types';
import { useAuth } from '../context/AuthContext';

export default function FavoritesScreen({ navigation }: any) {
  const { isAuthenticated } = useAuth();
  const [favorites, setFavorites] = useState<Favorite[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const loadData = useCallback(async () => {
    if (!isAuthenticated) {
      setLoading(false);
      return;
    }
    try {
      const response = await apiService.getFavorites();
      setFavorites(response.items || response || []);
    } catch (error) {
      console.error('Error loading favorites:', error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, [isAuthenticated]);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const onRefresh = () => {
    setRefreshing(true);
    loadData();
  };

  const handleDelete = (id: number) => {
    Alert.alert('Eliminar favorito', '¿Estás seguro?', [
      { text: 'Cancelar', style: 'cancel' },
      {
        text: 'Eliminar',
        style: 'destructive',
        onPress: async () => {
          try {
            await apiService.deleteFavorite(id);
            setFavorites((prev) => prev.filter((f) => f.id !== id));
          } catch (error) {
            Alert.alert('Error', 'No se pudo eliminar el favorito');
          }
        },
      },
    ]);
  };

  const getIcon = (type: string) => {
    switch (type) {
      case 'category': return '📋';
      case 'pilot': return '🏎️';
      case 'circuit': return '🏁';
      case 'season': return '📅';
      case 'result': return '📊';
      case 'session': return '🕐';
      default: return '⭐';
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

  const renderItem = ({ item }: { item: Favorite }) => (
    <Card style={styles.card}>
      <View style={styles.cardRow}>
        <Text style={styles.icon}>{getIcon(item.resource_type)}</Text>
        <View style={styles.cardInfo}>
          <Text style={styles.cardTitle}>
            {getTypeLabel(item.resource_type)} #{item.resource_id}
          </Text>
          <Text style={styles.cardDesc}>
            Guardado el {new Date(item.created_at || '').toLocaleDateString()}
          </Text>
        </View>
        <TouchableOpacity
          style={styles.deleteButton}
          onPress={() => handleDelete(item.id)}
        >
          <Text style={styles.deleteText}>🗑️</Text>
        </TouchableOpacity>
      </View>
    </Card>
  );

  if (!isAuthenticated) {
    return (
      <View style={styles.container}>
        <EmptyState
          title="Inicia sesión"
          message="Necesitas una cuenta para guardar favoritos"
          icon="⭐"
        />
        <View style={styles.actions}>
          <Button
            title="Iniciar sesión"
            onPress={() => navigation.getParent()?.navigate('Login')}
            variant="primary"
            size="lg"
            style={styles.button}
          />
        </View>
      </View>
    );
  }

  if (loading) {
    return <Loading message="Cargando favoritos..." />;
  }

  return (
    <View style={styles.container}>
      <FlatList
        data={favorites}
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
          <EmptyState
            title="Sin favoritos"
            message="Guarda pilotos, circuitos y categorías que te interesen"
            icon="⭐"
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
  icon: {
    fontSize: 24,
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
  deleteButton: {
    padding: spacing.sm,
  },
  deleteText: {
    fontSize: 20,
  },
  actions: {
    padding: spacing.lg,
  },
  button: {
    marginBottom: spacing.sm,
  },
});
