// Pantalla de detalle de piloto
// Muestra biografía completa, estadísticas y datos del piloto

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
import { Pilot } from '../types';

export default function PilotDetailScreen({ route }: any) {
  const { pilot } = route.params as { pilot: Pilot };

  if (!pilot) {
    return <Loading message="Cargando piloto..." />;
  }

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      {/* Header con foto */}
      <View style={styles.header}>
        <View style={styles.photoContainer}>
          {pilot.photo_url ? (
            <Image source={{ uri: pilot.photo_url }} style={styles.photo} />
          ) : (
            <View style={styles.photoPlaceholder}>
              <Text style={styles.photoPlaceholderText}>
                {pilot.name.charAt(0).toUpperCase()}
              </Text>
            </View>
          )}
        </View>
        <Text style={styles.name}>{pilot.name}</Text>
        {pilot.number && (
          <View style={styles.numberBadge}>
            <Text style={styles.numberText}>#{pilot.number}</Text>
          </View>
        )}
        {pilot.team && (
          <Text style={styles.team}>{pilot.team}</Text>
        )}
        {pilot.nationality && (
          <Text style={styles.nationality}>🇦🇷 {pilot.nationality}</Text>
        )}
      </View>

      {/* Estadísticas */}
      <View style={styles.statsRow}>
        <Card style={styles.statCard}>
          <Text style={styles.statValue}>{pilot.championships || 0}</Text>
          <Text style={styles.statLabel}>Campeonatos</Text>
        </Card>
        <Card style={styles.statCard}>
          <Text style={styles.statValue}>{pilot.wins || 0}</Text>
          <Text style={styles.statLabel}>Victorias</Text>
        </Card>
        <Card style={styles.statCard}>
          <Text style={styles.statValue}>{pilot.podiums || 0}</Text>
          <Text style={styles.statLabel}>Podios</Text>
        </Card>
      </View>

      {/* Biografía */}
      {pilot.biography && (
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Biografía</Text>
          <Card style={styles.bioCard}>
            <Text style={styles.bioText}>{pilot.biography}</Text>
          </Card>
        </View>
      )}

      {/* Datos personales */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Datos Personales</Text>
        <Card style={styles.infoCard}>
          {pilot.birth_date && (
            <View style={styles.infoRow}>
              <Text style={styles.infoLabel}>Fecha de nacimiento</Text>
              <Text style={styles.infoValue}>{pilot.birth_date}</Text>
            </View>
          )}
          {pilot.nationality && (
            <View style={styles.infoRow}>
              <Text style={styles.infoLabel}>Nacionalidad</Text>
              <Text style={styles.infoValue}>{pilot.nationality}</Text>
            </View>
          )}
          {pilot.team && (
            <View style={styles.infoRow}>
              <Text style={styles.infoLabel}>Equipo</Text>
              <Text style={styles.infoValue}>{pilot.team}</Text>
            </View>
          )}
          {pilot.number && (
            <View style={styles.infoRow}>
              <Text style={styles.infoLabel}>Número</Text>
              <Text style={styles.infoValue}>#{pilot.number}</Text>
            </View>
          )}
        </Card>
      </View>

      {/* Estado */}
      <View style={styles.section}>
        <Card style={styles.statusCard}>
          <View style={styles.statusRow}>
            <Text style={styles.statusLabel}>Estado</Text>
            <Badge
              text={pilot.is_ficticio ? 'Muestra' : (pilot.championships && pilot.championships > 0 ? 'Histórico' : 'Activo')}
              color={pilot.is_ficticio ? colors.warning : colors.success}
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
    width: 120,
    height: 120,
    borderRadius: 60,
    borderWidth: 3,
    borderColor: colors.primary,
  },
  photoPlaceholder: {
    width: 120,
    height: 120,
    borderRadius: 60,
    backgroundColor: colors.primary + '30',
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 3,
    borderColor: colors.primary,
  },
  photoPlaceholderText: {
    fontSize: 48,
    fontWeight: typography.bold,
    color: colors.primaryLight,
  },
  name: {
    fontSize: typography.xxl,
    fontWeight: typography.black,
    color: colors.text,
    textAlign: 'center',
  },
  numberBadge: {
    backgroundColor: colors.primary + '30',
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.xs,
    borderRadius: borderRadius.full,
    borderWidth: 1,
    borderColor: colors.primary,
    marginTop: spacing.sm,
  },
  numberText: {
    color: colors.primaryLight,
    fontSize: typography.lg,
    fontWeight: typography.bold,
    fontFamily: typography.mono,
  },
  team: {
    fontSize: typography.lg,
    color: colors.textSecondary,
    marginTop: spacing.sm,
  },
  nationality: {
    fontSize: typography.md,
    color: colors.textMuted,
    marginTop: spacing.xs,
  },
  statsRow: {
    flexDirection: 'row',
    padding: spacing.lg,
    gap: spacing.sm,
  },
  statCard: {
    flex: 1,
    alignItems: 'center',
    padding: spacing.md,
  },
  statValue: {
    fontSize: typography.xxxl,
    fontWeight: typography.black,
    color: colors.primaryLight,
    fontFamily: typography.mono,
  },
  statLabel: {
    fontSize: typography.xs,
    color: colors.textSecondary,
    marginTop: spacing.xs,
    textTransform: 'uppercase',
    letterSpacing: 1,
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
  },
  bioCard: {
    padding: spacing.lg,
  },
  bioText: {
    fontSize: typography.md,
    color: colors.textSecondary,
    lineHeight: 22,
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
