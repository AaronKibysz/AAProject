// Pantalla de registro con diseño racing

import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  StyleSheet,
  ActivityIndicator,
  Alert,
  ScrollView,
  KeyboardAvoidingView,
  Platform,
} from 'react-native';
import { colors, typography, spacing, borderRadius } from '../theme';
import { Button, Card } from '../components';
import { useAuth } from '../context/AuthContext';

export default function RegisterScreen({ navigation }: any) {
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [loading, setLoading] = useState(false);
  const { register } = useAuth();

  const handleRegister = async () => {
    if (!email || !username || !password) {
      Alert.alert('Error', 'Completa los campos obligatorios');
      return;
    }

    setLoading(true);
    try {
      await register({
        email,
        username,
        password,
        full_name: fullName || undefined,
      });
      navigation.getParent()?.navigate('MainTabs');
    } catch (error: any) {
      const message = error.response?.data?.detail || 'Error al registrarse';
      Alert.alert('Error', message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    >
      <ScrollView contentContainerStyle={styles.scrollContent}>
        <View style={styles.header}>
          <Text style={styles.logo}>🏁</Text>
          <Text style={styles.title}>Automovilismo</Text>
          <Text style={styles.subtitle}>Crear Cuenta</Text>
        </View>

        <Card style={styles.form}>
          <TextInput
            style={styles.input}
            placeholder="Email *"
            placeholderTextColor={colors.textMuted}
            value={email}
            onChangeText={setEmail}
            keyboardType="email-address"
            autoCapitalize="none"
          />
          <TextInput
            style={styles.input}
            placeholder="Nombre de usuario *"
            placeholderTextColor={colors.textMuted}
            value={username}
            onChangeText={setUsername}
            autoCapitalize="none"
          />
          <TextInput
            style={styles.input}
            placeholder="Contraseña *"
            placeholderTextColor={colors.textMuted}
            value={password}
            onChangeText={setPassword}
            secureTextEntry
          />
          <TextInput
            style={styles.input}
            placeholder="Nombre completo (opcional)"
            placeholderTextColor={colors.textMuted}
            value={fullName}
            onChangeText={setFullName}
          />

          <Button
            title="Registrarse"
            onPress={handleRegister}
            loading={loading}
            size="lg"
            style={styles.button}
          />

          <Button
            title="¿Ya tienes cuenta? Inicia sesión"
            onPress={() => navigation.navigate('Login')}
            variant="ghost"
            size="md"
            style={styles.linkButton}
          />
        </Card>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  scrollContent: {
    flexGrow: 1,
    justifyContent: 'center',
    padding: spacing.lg,
  },
  header: {
    alignItems: 'center',
    marginBottom: spacing.xxl,
  },
  logo: {
    fontSize: 64,
    marginBottom: spacing.md,
  },
  title: {
    fontSize: typography.xxxl,
    fontWeight: typography.black,
    color: colors.text,
  },
  subtitle: {
    fontSize: typography.lg,
    color: colors.textSecondary,
    marginTop: spacing.xs,
  },
  form: {
    padding: spacing.xl,
  },
  input: {
    backgroundColor: colors.surfaceLight,
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: borderRadius.md,
    padding: spacing.md,
    marginBottom: spacing.md,
    fontSize: typography.md,
    color: colors.text,
  },
  button: {
    marginBottom: spacing.md,
  },
  linkButton: {
    marginTop: spacing.sm,
  },
});
