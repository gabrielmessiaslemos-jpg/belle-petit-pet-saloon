/**
 * Firebase Configuration
 *
 * Para configurar:
 * 1. Acesse https://console.firebase.google.com/
 * 2. Crie um projeto chamado "belle-petit-admin"
 * 3. Ative Authentication (Email/Password)
 * 4. Crie um banco Firestore
 * 5. Adicione um app Web e copie as credenciais
 * 6. Copie .env.example → .env e preencha os valores
 */

import { initializeApp, getApps, getApp } from 'firebase/app';
import { initializeAuth, getReactNativePersistence } from 'firebase/auth';
import { getFirestore } from 'firebase/firestore';
import AsyncStorage from '@react-native-async-storage/async-storage';

const firebaseConfig = {
  apiKey:            process.env.EXPO_PUBLIC_FIREBASE_API_KEY,
  authDomain:        process.env.EXPO_PUBLIC_FIREBASE_AUTH_DOMAIN,
  projectId:         process.env.EXPO_PUBLIC_FIREBASE_PROJECT_ID,
  storageBucket:     process.env.EXPO_PUBLIC_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: process.env.EXPO_PUBLIC_FIREBASE_MESSAGING_SENDER_ID,
  appId:             process.env.EXPO_PUBLIC_FIREBASE_APP_ID,
};

// Evita inicializar múltiplas vezes durante hot-reload
const app = getApps().length === 0 ? initializeApp(firebaseConfig) : getApp();

// Auth com persistência via AsyncStorage (mantém login entre sessões)
export const auth = initializeAuth(app, {
  persistence: getReactNativePersistence(AsyncStorage),
});

// Banco de dados Firestore
export const db = getFirestore(app);

export default app;
