// Pantalla de perfil con diseño racing

import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Alert,
} from 'react-native';
import { colors, typography, spacing, borderRadius } from '../theme';
import { Card, Button, Loading } from '../components';
import { useAuth } from '../context/AuthContext';

export default function ProfileScreen({ navigation }: any) {
  const { user, logout, logoutAll, isAuthenticated } = useAuth();

  if (!isAuthenticated || !user) {
    return (
      <View style={styles.container}>
        <View style={styles.header}>
          <View style={styles.avatar}>
            <Text style={styles.avatarText}>?</Text>
          </View>
          <Text style={styles.name}>Invitado</Text>
          <Text style={styles.email}>Inicia sesión para acceder a tu perfil</Text>
        </View>
        <View style={styles.actions}>
          <Button
            title="Iniciar sesión"
            onPress={() => navigation.getParent()?.navigate('Login')}
            variant="primary"
            size="lg"
            style={styles.button}
          />
          <Button
            title="Registrarse"
            onPress={() => navigation.getParent()?.navigate('Register')}
            variant="secondary"
            size="lg"
            style={styles.button}
          />
        </View>
      </View>
    );
  }

  const handleLogout = async () => {
    Alert.alert('Cerrar sesión', '¿Estás seguro?', [
      { text: 'Cancelar', style: 'cancel' },
      {
        text: 'Cerrar sesión',
        style: 'destructive',
        onPress: async () => {
          try {
            await logout();
          } catch (error) {
            Alert.alert('Error', 'No se pudo cerrar sesión');
          }
        },
      },
    ]);
  };

  const handleLogoutAll = async () => {
    Alert.alert('Cerrar todas las sesiones', '¿Estás seguro?', [
      { text: 'Cancelar', style: 'cancel' },
      {
        text: 'Cerrar todas',
        style: 'destructive',
        onPress: async () => {
          try {
            await logoutAll();
          } catch (error) {
            Alert.alert('Error', 'No se pudo cerrar todas las sesiones');
          }
        },
      },
    ]);
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <View style={styles.avatar}>
          <Text style={styles.avatarText}>
            {user.username.charAt(0).toUpperCase()}
          </Text>
        </View>
        <Text style={styles.name}>{user.full_name || user.username}</Text>
        <Text style={styles.email}>{user.email}</Text>
      </View>

      <View style={styles.section}>
        <Card style={styles.infoCard}>
          <View style={styles.infoRow}>
            <Text style={styles.label}>Usuario</Text>
            <Text style={styles.value}>{user.username}</Text>
          </View>
          <View style={styles.infoRow}>
            <Text style={styles.label}>Email</Text>
            <Text style={styles.value}>{user.email}</Text>
          </View>
          <View style={styles.infoRow}>
            <Text style={styles.label}>Estado</Text>
            <Text style={[styles.value, user.is_active ? styles.active : styles.inactive]}>
              {user.is_active ? 'Activo' : 'Inactivo'}
            </Text>
          </View>
        </Card>
      </View>

      <View style={styles.actions}>
        <Button
          title="Cerrar sesión"
          onPress={handleLogout}
          variant="primary"
          size="lg"
          style={styles.button}
        />
        <Button
          title="Cerrar todas las sesiones"
          onPress={handleLogoutAll}
          variant="danger"
          size="lg"
          style={styles.button}
        />
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  header: {
    backgroundColor: colors.surface,
    padding: spacing.xl,
    paddingTop: spacing.xxxl,
    alignItems: 'center',
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
  },
  avatar: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: colors.primary + '40',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: spacing.md,
    borderWidth: 2,
    borderColor: colors.primary,
  },
  avatarText: {
    fontSize: typography.xxxl,
    fontWeight: typography.bold,
    color: colors.primaryLight,
  },
  name: {
    fontSize: typography.xxl,
    fontWeight: typography.bold,
    color: colors.text,
  },
  email: {
    fontSize: typography.md,
    color: colors.textSecondary,
    marginTop: spacing.xs,
  },
  section: {
    padding: spacing.lg,
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
  label: {
    fontSize: typography.md,
    color: colors.textSecondary,
  },
  value: {
    fontSize: typography.md,
    fontWeight: typography.medium,
    color: colors.text,
  },
  active: {
    color: colors.success,
  },
  inactive: {
    color: colors.error,
  },
  actions: {
    padding: spacing.lg,
    gap: spacing.sm,
  },
  button: {
    marginBottom: spacing.sm,
  },
});
