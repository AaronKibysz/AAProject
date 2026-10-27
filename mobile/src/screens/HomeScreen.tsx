// Pantalla de inicio
// Muestra un resumen de la app y accesos rápidos

import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  ActivityIndicator,
} from 'react-native';
import { apiService } from '../services/api';
import { Category, Pilot, Circuit } from '../types';

export default function HomeScreen() {
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
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#1976d2" />
      </View>
    );
  }

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Automovilismo Argentino</Text>
        <Text style={styles.subtitle}>Turismo Carretera y más</Text>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Categorías ({categories.length})</Text>
        {categories.map((cat) => (
          <View key={cat.id} style={styles.card}>
            <Text style={styles.cardTitle}>{cat.name}</Text>
            {cat.description && <Text style={styles.cardDesc}>{cat.description}</Text>}
          </View>
        ))}
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Pilotos ({pilots.length})</Text>
        {pilots.map((pilot) => (
          <View key={pilot.id} style={styles.card}>
            <Text style={styles.cardTitle}>{pilot.name}</Text>
            {pilot.team && <Text style={styles.cardDesc}>{pilot.team}</Text>}
          </View>
        ))}
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Circuitos ({circuits.length})</Text>
        {circuits.map((circuit) => (
          <View key={circuit.id} style={styles.card}>
            <Text style={styles.cardTitle}>{circuit.name}</Text>
            {circuit.location && <Text style={styles.cardDesc}>{circuit.location}</Text>}
          </View>
        ))}
      </View>
    </ScrollView>
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
  header: {
    backgroundColor: '#1976d2',
    padding: 20,
    paddingTop: 40,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: 'white',
  },
  subtitle: {
    fontSize: 14,
    color: 'rgba(255,255,255,0.8)',
    marginTop: 4,
  },
  section: {
    padding: 16,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 12,
    color: '#333',
  },
  card: {
    backgroundColor: 'white',
    padding: 12,
    borderRadius: 8,
    marginBottom: 8,
    elevation: 2,
  },
  cardTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
  },
  cardDesc: {
    fontSize: 14,
    color: '#666',
    marginTop: 4,
  },
});
