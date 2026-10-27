// App principal: navegación por pestañas con botón central elevado para "En vivo"

import React from 'react';
import { NavigationContainer, DefaultTheme } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createStackNavigator } from '@react-navigation/stack';
import { AuthProvider, useAuth } from './src/context/AuthContext';
import { ActivityIndicator, View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { colors, typography, spacing } from './src/theme';

import ChampionshipsScreen from './src/screens/ChampionshipsScreen';
import RecentEventsScreen from './src/screens/RecentEventsScreen';
import LiveScreen from './src/screens/LiveScreen';
import HistoryScreen from './src/screens/HistoryScreen';
import SearchScreen from './src/screens/SearchScreen';
import FavoritesScreen from './src/screens/FavoritesScreen';
import PilotDetailScreen from './src/screens/PilotDetailScreen';
import CircuitDetailScreen from './src/screens/CircuitDetailScreen';
import LoginScreen from './src/screens/LoginScreen';
import RegisterScreen from './src/screens/RegisterScreen';
import ProfileScreen from './src/screens/ProfileScreen';

const Tab = createBottomTabNavigator();
const Stack = createStackNavigator();

const navigationTheme = {
  ...DefaultTheme,
  colors: {
    ...DefaultTheme.colors,
    background: colors.background,
    card: colors.surface,
    text: colors.text,
    border: colors.border,
    primary: colors.primary,
  },
};

function LiveTabButton({ onPress, accessibilityState, accessibilityLabel }: any) {
  const focused = accessibilityState?.selected;
  return (
    <TouchableOpacity
      onPress={onPress}
      accessibilityLabel={accessibilityLabel}
      accessibilityState={accessibilityState}
      activeOpacity={0.85}
      style={styles.liveSlot}
    >
      <View style={[styles.liveButton, focused && styles.liveButtonFocused]}>
        <Ionicons name="radio-outline" size={26} color={colors.text} />
      </View>
    </TouchableOpacity>
  );
}

function MainTabs() {
  return (
    <Tab.Navigator
      screenOptions={{
        headerShown: false,
        tabBarActiveTintColor: colors.primary,
        tabBarInactiveTintColor: colors.textMuted,
        tabBarStyle: styles.tabBar,
        tabBarLabelStyle: styles.tabBarLabel,
        tabBarIconStyle: styles.tabBarIcon,
      }}
    >
      <Tab.Screen
        name="Championships"
        component={ChampionshipsScreen}
        options={{
          tabBarLabel: 'Campeonatos',
          tabBarIcon: ({ color }) => <Ionicons name="trophy-outline" size={22} color={color} />,
        }}
      />
      <Tab.Screen
        name="RecentEvents"
        component={RecentEventsScreen}
        options={{
          tabBarLabel: 'Resultados',
          tabBarIcon: ({ color }) => <Ionicons name="stats-chart-outline" size={22} color={color} />,
        }}
      />
      <Tab.Screen
        name="Live"
        component={LiveScreen}
        options={{
          tabBarLabel: 'En vivo',
          tabBarShowLabel: false,
          tabBarButton: (props) => <LiveTabButton {...props} />,
        }}
      />
      <Tab.Screen
        name="History"
        component={HistoryScreen}
        options={{
          tabBarLabel: 'Historia',
          tabBarIcon: ({ color }) => <Ionicons name="book-outline" size={22} color={color} />,
        }}
      />
      <Tab.Screen
        name="Profile"
        component={ProfileScreen}
        options={{
          tabBarLabel: 'Perfil',
          tabBarIcon: ({ color }) => <Ionicons name="person-outline" size={22} color={color} />,
        }}
      />
    </Tab.Navigator>
  );
}

function AppContent() {
  const { isLoading } = useAuth();

  if (isLoading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color={colors.primary} />
        <Text style={styles.loadingText}>Cargando...</Text>
      </View>
    );
  }

  return (
    <NavigationContainer theme={navigationTheme}>
      <Stack.Navigator screenOptions={{ headerShown: false, cardStyle: { backgroundColor: colors.background } }}>
        <Stack.Screen name="MainTabs" component={MainTabs} />
        <Stack.Screen name="Login" component={LoginScreen} />
        <Stack.Screen name="Register" component={RegisterScreen} />
        <Stack.Screen name="Search" component={SearchScreen} />
        <Stack.Screen name="Favorites" component={FavoritesScreen} />
        <Stack.Screen name="PilotDetail" component={PilotDetailScreen} />
        <Stack.Screen name="CircuitDetail" component={CircuitDetailScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}

const styles = StyleSheet.create({
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: colors.background,
  },
  loadingText: {
    marginTop: spacing.md,
    fontSize: typography.base,
    color: colors.textSecondary,
  },
  tabBar: {
    height: 68,
    paddingTop: 8,
    paddingBottom: 10,
    backgroundColor: colors.surface,
    borderTopWidth: 1,
    borderTopColor: colors.border,
  },
  tabBarLabel: {
    fontSize: 11,
    fontWeight: '600',
    letterSpacing: 0.2,
    marginTop: 2,
  },
  tabBarIcon: {
    marginBottom: 0,
  },
  liveSlot: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'flex-start',
  },
  liveButton: {
    width: 58,
    height: 58,
    borderRadius: 29,
    marginTop: -26,
    backgroundColor: colors.primary,
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 4,
    borderColor: colors.background,
    shadowColor: colors.primary,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.4,
    shadowRadius: 10,
    elevation: 8,
  },
  liveButtonFocused: {
    backgroundColor: colors.primaryDark,
  },
});
