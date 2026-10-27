// Pantalla de detalle de circuito
// Muestra datos técnicos, descripción y récord de vuelta

import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  Image,
} from 'react-native';
import { colors, typography, spacing, borderRadius } from '../theme';
import { Card, Badge, Loading } from '../components';
import { Circuit } from '../types';

export default function CircuitDetailScreen({ route }: any) {
  const { circuit } = route.params as { circuit: Circuit };

  if (!circuit) {
    return <Loading message="Cargando circuito..." />;
  }

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      {/* Header con foto */}
      <View style={styles.header}>
        <View style={styles.photoContainer}>
          {circuit.photo_url ? (
            <Image source={{ uri: circuit.photo_url }} style={styles.photo} />
          ) : (
            <View style={styles.photoPlaceholder}>
              <Text style={styles.photoPlaceholderText}>🏁</Text>
            </View>
          )}
        </View>
        <Text style={styles.name}>{circuit.name}</Text>
        {circuit.location && (
          <Text style={styles.location}>{circuit.location}</Text>
        )}
        {circuit.country && (
          <Text style={styles.country}>{circuit.country}</Text>
        )}
      </View>

      {/* Datos técnicos */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Datos Técnicos</Text>
        <Card style={styles.infoCard}>
          {circuit.length_km && (
            <View style={styles.infoRow}>
              <Text style={styles.infoLabel}>Longitud</Text>
              <Text style={styles.infoValue}>{circuit.length_km} km</Text>
            </View>
          )}
          {circuit.turns && (
            <View style={styles.infoRow}>
              <Text style={styles.infoLabel}>Curvas</Text>
              <Text style={styles.infoValue}>{circuit.turns}</Text>
            </View>
          )}
          {circuit.capacity && (
            <View style={styles.infoRow}>
              <Text style={styles.infoLabel}>Capacidad</Text>
              <Text style={styles.infoValue}>{circuit.capacity.toLocaleString()} espectadores</Text>
            </View>
          )}
          {circuit.record_lap && (
            <View style={styles.infoRow}>
              <Text style={styles.infoLabel}>Récord de vuelta</Text>
              <Text style={styles.infoValue}>{circuit.record_lap}</Text>
            </View>
          )}
          {circuit.record_holder && (
            <View style={styles.infoRow}>
              <Text style={styles.infoLabel}>Récord holder</Text>
              <Text style={styles.infoValue}>{circuit.record_holder}</Text>
            </View>
          )}
        </Card>
      </View>

      {/* Descripción */}
      {circuit.description && (
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Descripción</Text>
          <Card style={styles.descCard}>
            <Text style={styles.descText}>{circuit.description}</Text>
          </Card>
        </View>
      )}

      {/* Estado */}
      <View style={styles.section}>
        <Card style={styles.statusCard}>
          <View style={styles.statusRow}>
            <Text style={styles.statusLabel}>Estado</Text>
            <Badge
              text={circuit.is_ficticio ? 'Muestra' : 'Oficial'}
              color={circuit.is_ficticio ? colors.warning : colors.success}
            />
          </View>
        </Card>
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
    alignItems: 'center',
    padding: spacing.xl,
    paddingTop: spacing.xxxl,
    backgroundColor: colors.surface,
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
  },
  photoContainer: {
    marginBottom: spacing.md,
  },
  photo: {
    width: 200,
    height: 120,
    borderRadius: borderRadius.lg,
    borderWidth: 2,
    borderColor: colors.primary,
  },
  photoPlaceholder: {
    width: 200,
    height: 120,
    borderRadius: borderRadius.lg,
    backgroundColor: colors.primary + '30',
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 2,
    borderColor: colors.primary,
  },
  photoPlaceholderText: {
    fontSize: 48,
  },
  name: {
    fontSize: typography.xxl,
    fontWeight: typography.black,
    color: colors.text,
    textAlign: 'center',
  },
  location: {
    fontSize: typography.lg,
    color: colors.textSecondary,
    marginTop: spacing.xs,
  },
  country: {
    fontSize: typography.md,
    color: colors.textMuted,
    marginTop: spacing.xs,
  },
  section: {
    padding: spacing.lg,
    paddingTop: 0,
  },
  sectionTitle: {
    fontSize: typography.xl,
    fontWeight: typography.bold,
    color: colors.text,
    marginBottom: spacing.md,
    marginTop: spacing.lg,
  },
  infoCard: {
    padding: spacing.lg,
  },
  infoRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: spacing.sm,
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
  },
  infoLabel: {
    fontSize: typography.md,
    color: colors.textSecondary,
  },
  infoValue: {
    fontSize: typography.md,
    fontWeight: typography.medium,
    color: colors.text,
    fontFamily: typography.mono,
  },
  descCard: {
    padding: spacing.lg,
  },
  descText: {
    fontSize: typography.md,
    color: colors.textSecondary,
    lineHeight: 22,
  },
  statusCard: {
    padding: spacing.lg,
  },
  statusRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  statusLabel: {
    fontSize: typography.md,
    color: colors.textSecondary,
  },
});
