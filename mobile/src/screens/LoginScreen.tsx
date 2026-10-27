// Pantalla de login con diseño racing

import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  StyleSheet,
  ActivityIndicator,
  Alert,
  KeyboardAvoidingView,
  Platform,
} from 'react-native';
import { colors, typography, spacing, borderRadius } from '../theme';
import { Button, Card } from '../components';
import { useAuth } from '../context/AuthContext';

export default function LoginScreen({ navigation }: any) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();

  const handleLogin = async () => {
    if (!email || !password) {
      Alert.alert('Error', 'Completa todos los campos');
      return;
    }

    setLoading(true);
    try {
      await login(email, password);
      navigation.getParent()?.navigate('MainTabs');
    } catch (error: any) {
      const message = error.response?.data?.detail || 'Error al iniciar sesión';
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
      <View style={styles.header}>
        <Text style={styles.logo}>🏁</Text>
        <Text style={styles.title}>Automovilismo</Text>
        <Text style={styles.subtitle}>Iniciar Sesión</Text>
      </View>

      <Card style={styles.form}>
        <TextInput
          style={styles.input}
          placeholder="Email"
          placeholderTextColor={colors.textMuted}
          value={email}
          onChangeText={setEmail}
          keyboardType="email-address"
          autoCapitalize="none"
        />
        <TextInput
          style={styles.input}
          placeholder="Contraseña"
          placeholderTextColor={colors.textMuted}
          value={password}
          onChangeText={setPassword}
          secureTextEntry
        />

        <Button
          title="Iniciar Sesión"
          onPress={handleLogin}
          loading={loading}
          size="lg"
          style={styles.button}
        />

        <Button
          title="¿No tienes cuenta? Regístrate"
          onPress={() => navigation.navigate('Register')}
          variant="ghost"
          size="md"
          style={styles.linkButton}
        />
      </Card>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
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
