// Pantalla de perfil
// Muestra datos del usuario y opciones de cuenta

import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Alert,
} from 'react-native';
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
          <Text style={styles.email}>Inicia sesi髇 para acceder a tu perfil</Text>
        </View>
        <View style={styles.actions}>
          <TouchableOpacity
            style={styles.button}
            onPress={() => navigation.getParent()?.navigate('Login')}
          >
            <Text style={styles.buttonText}>Iniciar sesi髇</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={[styles.button, styles.buttonSecondary]}
            onPress={() => navigation.getParent()?.navigate('Register')}
          >
            <Text style={styles.buttonText}>Registrarse</Text>
          </TouchableOpacity>
        </View>
      </View>
    );
  }

  const handleLogout = async () => {
    Alert.alert('Cerrar sesi贸n', '驴Est谩s seguro?', [
      { text: 'Cancelar', style: 'cancel' },
      {
        text: 'Cerrar sesi贸n',
        style: 'destructive',
        onPress: async () => {
          try {
            await logout();
          } catch (error) {
            Alert.alert('Error', 'No se pudo cerrar sesi贸n');
          }
        },
      },
    ]);
  };

  const handleLogoutAll = async () => {
    Alert.alert('Cerrar todas las sesiones', '驴Est谩s seguro?', [
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

  if (!user) {
    return null;
  }

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
      </View>

      <View style={styles.actions}>
        <TouchableOpacity style={styles.button} onPress={handleLogout}>
          <Text style={styles.buttonText}>Cerrar sesi贸n</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={[styles.button, styles.buttonDanger]}
          onPress={handleLogoutAll}
        >
          <Text style={styles.buttonText}>Cerrar todas las sesiones</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    backgroundColor: '#1976d2',
    padding: 20,
    paddingTop: 40,
    alignItems: 'center',
  },
  avatar: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: 'rgba(255,255,255,0.3)',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 12,
  },
  avatarText: {
    fontSize: 32,
    fontWeight: 'bold',
    color: 'white',
  },
  name: {
    fontSize: 20,
    fontWeight: 'bold',
    color: 'white',
  },
  email: {
    fontSize: 14,
    color: 'rgba(255,255,255,0.8)',
    marginTop: 4,
  },
  section: {
    backgroundColor: 'white',
    margin: 16,
    borderRadius: 8,
    padding: 16,
    elevation: 2,
  },
  infoRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: 8,
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
  },
  label: {
    fontSize: 14,
    color: '#666',
  },
  value: {
    fontSize: 14,
    fontWeight: '500',
    color: '#333',
  },
  active: {
    color: '#4caf50',
  },
  inactive: {
    color: '#f44336',
  },
  actions: {
    padding: 16,
  },
  button: {
    backgroundColor: '#1976d2',
    padding: 14,
    borderRadius: 8,
    alignItems: 'center',
    marginBottom: 12,
  },
  buttonSecondary: {
    backgroundColor: '#4caf50',
  },
  buttonDanger: {
    backgroundColor: '#f44336',
  },
  buttonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: '600',
  },
});
