// Pantalla de Campeonatos: solo campeonatos activos y sus próximas carreras

import React, { useState, useEffect, useCallback } from 'react';
import { View, Text, StyleSheet, ScrollView, RefreshControl } from 'react-native';
import { colors, typography, spacing } from '../theme';
import { Card, Loading, EmptyState, Badge } from '../components';
import { ScreenHeader, SectionLabel } from '../components/ScreenHeader';
import { apiService } from '../services/api';
import { Category, Season, Session } from '../types';

export default function ChampionshipsScreen() {
  const [categories, setCategories] = useState<Category[]>([]);
  const [seasons, setSeasons] = useState<Season[]>([]);
  const [sessions, setSessions] = useState<Session[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const loadData = useCallback(async () => {
    try {
      const [cats, seasonsData, sessionsData] = await Promise.all([
        apiService.getCategories({ limit: 50 }),
        apiService.getSeasons({ limit: 50 }),
        apiService.getSessions({ limit: 20 }),
      ]);
      setCategories(cats.items || cats);
      setSeasons(seasonsData.items || seasonsData);
      setSessions(sessionsData.items || sessionsData);
    } catch (error) {
      console.error('Error loading championships:', error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, []);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const onRefresh = () => {
    setRefreshing(true);
    loadData();
  };

  if (loading) {
    return <Loading message="Cargando campeonatos..." />;
  }

  const activeSeasons = seasons.filter((s) => s.is_active === true);
  const activeSeasonIds = new Set(activeSeasons.map((s) => s.id));
  const upcomingSessions = sessions
    .filter((s) => activeSeasonIds.has(s.season_id))
    .slice(0, 5);

  return (
    <View style={styles.container}>
      <ScreenHeader title="Campeonatos" subtitle="Temporada en curso" />
      <ScrollView
        contentContainerStyle={styles.content}
        refreshControl={
          <RefreshControl
            refreshing={refreshing}
            onRefresh={onRefresh}
            tintColor={colors.primary}
            colors={[colors.primary]}
          />
        }
      >
        <SectionLabel>Activos</SectionLabel>
        {activeSeasons.length === 0 ? (
          <EmptyState
            title="Sin campeonatos activos"
            message="No hay campeonatos en curso en este momento"
          />
        ) : (
          activeSeasons.map((season) => {
            const cat = categories.find((c) => c.id === season.category_id);
            return (
              <Card key={season.id} style={styles.champCard}>
                <View style={styles.row}>
                  <View style={styles.info}>
                    <Text style={styles.champName}>{cat?.name ?? 'Campeonato'}</Text>
                    <Text style={styles.champYear}>Temporada {season.year}</Text>
                  </View>
                  <Badge text="En curso" color={colors.success} />
                </View>
              </Card>
            );
          })
        )}

        {activeSeasons.length > 0 && (
          <>
            <SectionLabel style={styles.sectionSpacing}>Próximas carreras</SectionLabel>
            {upcomingSessions.length === 0 ? (
              <EmptyState title="Sin carreras programadas" message="Aún no hay fechas cargadas" />
            ) : (
              upcomingSessions.map((session) => (
                <Card key={session.id} style={styles.sessionCard}>
                  <Text style={styles.sessionType}>
                    {(session.session_type || 'Carrera').toUpperCase()}
                  </Text>
                  <Text style={styles.sessionDate}>{session.date || 'Fecha por confirmar'}</Text>
                </Card>
              ))
            )}
          </>
        )}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  content: {
    paddingHorizontal: spacing.lg,
    paddingBottom: 120,
  },
  row: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  info: {
    flex: 1,
    marginRight: spacing.md,
  },
  champCard: {
    borderLeftWidth: 3,
    borderLeftColor: colors.primary,
    marginBottom: spacing.sm,
  },
  champName: {
    fontSize: typography.lg,
    fontWeight: typography.semibold,
    color: colors.text,
  },
  champYear: {
    fontSize: typography.sm,
    color: colors.textSecondary,
    marginTop: spacing.xs,
  },
  sectionSpacing: {
    marginTop: spacing.xl,
  },
  sessionCard: {
    marginBottom: spacing.sm,
  },
  sessionType: {
    fontSize: typography.sm,
    fontWeight: typography.bold,
    letterSpacing: 1,
    color: colors.primaryLight,
  },
  sessionDate: {
    fontSize: typography.md,
    color: colors.textSecondary,
    marginTop: spacing.xs,
  },
});
