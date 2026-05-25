import React from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { Ionicons } from '@expo/vector-icons';
import { Colors } from '../theme';
import { AppTabParamList } from '../types';

// Screens
import { DashboardScreen } from '../screens/dashboard/DashboardScreen';
import { AppointmentsScreen } from '../screens/appointments/AppointmentsScreen';
import { NewAppointmentScreen } from '../screens/appointments/NewAppointmentScreen';
import { AppointmentDetailScreen } from '../screens/appointments/AppointmentDetailScreen';
import { ClientsScreen } from '../screens/clients/ClientsScreen';
import { ClientDetailScreen } from '../screens/clients/ClientDetailScreen';
import { NewClientScreen } from '../screens/clients/NewClientScreen';
import { NewPetScreen } from '../screens/clients/NewPetScreen';
import { PetDetailScreen } from '../screens/clients/PetDetailScreen';
import { FinancialScreen } from '../screens/financial/FinancialScreen';
import { NewTransactionScreen } from '../screens/financial/NewTransactionScreen';
import { ServicesScreen } from '../screens/services/ServicesScreen';
import { NewServiceScreen } from '../screens/services/NewServiceScreen';

// ─── Stack navigators per tab ─────────────────────────────────────────────────
function AppointmentsStack() {
  const Stack = createNativeStackNavigator();
  return (
    <Stack.Navigator screenOptions={{ headerShown: false }}>
      <Stack.Screen name="AppointmentsList" component={AppointmentsScreen} />
      <Stack.Screen name="NewAppointment" component={NewAppointmentScreen} />
      <Stack.Screen name="AppointmentDetail" component={AppointmentDetailScreen} />
    </Stack.Navigator>
  );
}

function ClientsStack() {
  const Stack = createNativeStackNavigator();
  return (
    <Stack.Navigator screenOptions={{ headerShown: false }}>
      <Stack.Screen name="ClientsList" component={ClientsScreen} />
      <Stack.Screen name="NewClient" component={NewClientScreen} />
      <Stack.Screen name="ClientDetail" component={ClientDetailScreen} />
      <Stack.Screen name="NewPet" component={NewPetScreen} />
      <Stack.Screen name="PetDetail" component={PetDetailScreen} />
    </Stack.Navigator>
  );
}

function FinancialStack() {
  const Stack = createNativeStackNavigator();
  return (
    <Stack.Navigator screenOptions={{ headerShown: false }}>
      <Stack.Screen name="FinancialOverview" component={FinancialScreen} />
      <Stack.Screen name="NewTransaction" component={NewTransactionScreen} />
    </Stack.Navigator>
  );
}

function ServicesStack() {
  const Stack = createNativeStackNavigator();
  return (
    <Stack.Navigator screenOptions={{ headerShown: false }}>
      <Stack.Screen name="ServicesList" component={ServicesScreen} />
      <Stack.Screen name="NewService" component={NewServiceScreen} />
    </Stack.Navigator>
  );
}

// ─── Bottom Tab Navigator ─────────────────────────────────────────────────────
const Tab = createBottomTabNavigator<AppTabParamList>();

export function MainNavigator() {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        headerShown: false,
        tabBarStyle: {
          backgroundColor: Colors.surface,
          borderTopColor: Colors.primary + '33',
          borderTopWidth: 1,
          paddingBottom: 6,
          height: 62,
        },
        tabBarActiveTintColor: Colors.primary,
        tabBarInactiveTintColor: Colors.textMuted,
        tabBarLabelStyle: { fontSize: 11, fontWeight: '600', marginTop: 2 },
        tabBarIcon: ({ color, focused }) => {
          const icons: Record<string, { active: keyof typeof Ionicons.glyphMap; inactive: keyof typeof Ionicons.glyphMap }> = {
            Dashboard:    { active: 'home',             inactive: 'home-outline' },
            Appointments: { active: 'calendar',          inactive: 'calendar-outline' },
            Clients:      { active: 'people',            inactive: 'people-outline' },
            Financial:    { active: 'wallet',            inactive: 'wallet-outline' },
            Services:     { active: 'cut',               inactive: 'cut-outline' },
          };
          const icon = icons[route.name];
          return (
            <Ionicons
              name={focused ? icon?.active : icon?.inactive}
              size={22}
              color={color}
            />
          );
        },
      })}
    >
      <Tab.Screen name="Dashboard"    component={DashboardScreen}   options={{ tabBarLabel: 'Início' }} />
      <Tab.Screen name="Appointments" component={AppointmentsStack} options={{ tabBarLabel: 'Agenda' }} />
      <Tab.Screen name="Clients"      component={ClientsStack}      options={{ tabBarLabel: 'Clientes' }} />
      <Tab.Screen name="Financial"    component={FinancialStack}    options={{ tabBarLabel: 'Financeiro' }} />
      <Tab.Screen name="Services"     component={ServicesStack}     options={{ tabBarLabel: 'Serviços' }} />
    </Tab.Navigator>
  );
}
