// Pantalla de perfil
// En el MVP no hay cuentas: los favoritos se guardan localmente en el dispositivo.

import React from 'react';
import {
  View,
  Text,
  StyleSheet,
} from 'react-native';

export default function ProfileScreen() {
  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <View style={styles.avatar}>
          <Text style={styles.avatarText}>?</Text>
        </View>
        <Text style={styles.name}>Invitado</Text>
        <Text style={styles.email}>Los favoritos se guardan en este dispositivo</Text>
      </View>

      <View style={styles.section}>
        <Text style={styles.infoText}>
          Esta versión del MVP no incluye cuentas de usuario ni sincronización en la nube.
          Tus favoritos se almacenan localmente en el dispositivo.
        </Text>
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
    textAlign: 'center',
  },
  section: {
    backgroundColor: 'white',
    margin: 16,
    borderRadius: 8,
    padding: 16,
    elevation: 2,
  },
  infoText: {
    fontSize: 14,
    color: '#333',
    lineHeight: 20,
  },
});