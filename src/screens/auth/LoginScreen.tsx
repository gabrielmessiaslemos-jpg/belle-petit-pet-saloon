import React, { useState } from 'react';
import {
  StyleSheet, View, Text, TextInput,
  TouchableOpacity, KeyboardAvoidingView,
  Platform, ScrollView, Alert, ActivityIndicator,
} from 'react-native';
import { StatusBar } from 'expo-status-bar';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { useAuth } from '../../context/AuthContext';
import { Colors, Spacing, Radius, Typography } from '../../theme';
import { GoldButton } from '../../components/GoldButton';

export function LoginScreen() {
  const { signIn } = useAuth();
  const insets = useSafeAreaInsets();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [showPass, setShowPass] = useState(false);

  async function handleLogin() {
    if (!email.trim() || !password.trim()) {
      Alert.alert('Atenção', 'Preencha e-mail e senha para continuar.');
      return;
    }
    setLoading(true);
    try {
      await signIn(email.trim().toLowerCase(), password);
    } catch (error: any) {
      const msg =
        error.code === 'auth/invalid-credential' ||
        error.code === 'auth/wrong-password' ||
        error.code === 'auth/user-not-found'
          ? 'E-mail ou senha incorretos.'
          : 'Erro ao fazer login. Verifique sua conexão.';
      Alert.alert('Erro', msg);
    } finally {
      setLoading(false);
    }
  }

  return (
    <KeyboardAvoidingView
      style={styles.wrapper}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    >
      <StatusBar style="light" />
      <ScrollView
        contentContainerStyle={[styles.container, { paddingTop: insets.top + 40, paddingBottom: insets.bottom + 24 }]}
        keyboardShouldPersistTaps="handled"
      >
        {/* Logo */}
        <View style={styles.logoArea}>
          <View style={styles.logoCircle}>
            <Text style={styles.logoPaw}>🐾</Text>
          </View>
          <Text style={styles.brandName}>Belle Petit</Text>
          <Text style={styles.brandSub}>PET SALOON</Text>
          <View style={styles.divider} />
          <Text style={styles.adminLabel}>Área Administrativa</Text>
        </View>

        {/* Form */}
        <View style={styles.form}>
          <Text style={styles.fieldLabel}>E-mail</Text>
          <TextInput
            style={styles.input}
            placeholder="seu@email.com"
            placeholderTextColor={Colors.textMuted}
            value={email}
            onChangeText={setEmail}
            keyboardType="email-address"
            autoCapitalize="none"
            autoCorrect={false}
          />

          <Text style={[styles.fieldLabel, { marginTop: Spacing.md }]}>Senha</Text>
          <View style={styles.passwordRow}>
            <TextInput
              style={[styles.input, styles.passwordInput]}
              placeholder="••••••••"
              placeholderTextColor={Colors.textMuted}
              value={password}
              onChangeText={setPassword}
              secureTextEntry={!showPass}
              autoCapitalize="none"
            />
            <TouchableOpacity
              onPress={() => setShowPass(!showPass)}
              style={styles.eyeBtn}
            >
              <Text style={styles.eyeIcon}>{showPass ? '🙈' : '👁️'}</Text>
            </TouchableOpacity>
          </View>

          <GoldButton
            label={loading ? '' : 'Entrar'}
            onPress={handleLogin}
            loading={loading}
            fullWidth
            style={{ marginTop: Spacing.xl }}
          />
        </View>

        <Text style={styles.footer}>
          Belle Petit Pet Saloon © {new Date().getFullYear()}
        </Text>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  wrapper: {
    flex: 1,
    backgroundColor: Colors.background,
  },
  container: {
    flexGrow: 1,
    paddingHorizontal: Spacing.xl,
    alignItems: 'center',
  },
  logoArea: {
    alignItems: 'center',
    marginBottom: Spacing.xxl,
  },
  logoCircle: {
    width: 90,
    height: 90,
    borderRadius: 45,
    backgroundColor: Colors.primaryContainer,
    borderWidth: 2.5,
    borderColor: Colors.primary,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: Spacing.md,
  },
  logoPaw: {
    fontSize: 42,
  },
  brandName: {
    fontSize: 34,
    fontWeight: '700',
    color: Colors.primary,
    letterSpacing: 2,
    fontStyle: 'italic',
  },
  brandSub: {
    fontSize: 13,
    fontWeight: '600',
    color: Colors.textSecondary,
    letterSpacing: 6,
    marginTop: 2,
  },
  divider: {
    width: 60,
    height: 1,
    backgroundColor: Colors.primary + '55',
    marginVertical: Spacing.md,
  },
  adminLabel: {
    fontSize: 13,
    color: Colors.textSecondary,
    letterSpacing: 1.5,
  },
  form: {
    width: '100%',
    gap: 4,
  },
  fieldLabel: {
    ...Typography.bodySmall,
    color: Colors.textSecondary,
    marginBottom: 6,
  },
  input: {
    backgroundColor: Colors.surface,
    color: Colors.text,
    borderRadius: Radius.md,
    borderWidth: 1,
    borderColor: Colors.border,
    paddingHorizontal: Spacing.md,
    paddingVertical: Platform.OS === 'ios' ? 14 : 11,
    fontSize: 15,
  },
  passwordRow: {
    position: 'relative',
  },
  passwordInput: {
    paddingRight: 48,
  },
  eyeBtn: {
    position: 'absolute',
    right: 14,
    top: 0,
    bottom: 0,
    justifyContent: 'center',
  },
  eyeIcon: {
    fontSize: 18,
  },
  footer: {
    marginTop: Spacing.xxl,
    ...Typography.caption,
    color: Colors.textMuted,
  },
});
