import React from 'react';
import { StyleSheet, View, Text, TouchableOpacity, StatusBar } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { Colors, Spacing, Typography } from '../theme';

interface AppHeaderProps {
  title: string;
  subtitle?: string;
  onBack?: () => void;
  rightComponent?: React.ReactNode;
}

export function AppHeader({ title, subtitle, onBack, rightComponent }: AppHeaderProps) {
  const insets = useSafeAreaInsets();

  return (
    <View style={[styles.container, { paddingTop: insets.top + Spacing.sm }]}>
      <StatusBar barStyle="light-content" backgroundColor={Colors.background} />
      <View style={styles.row}>
        {onBack ? (
          <TouchableOpacity onPress={onBack} style={styles.backBtn} hitSlop={{ top: 8, bottom: 8, left: 8, right: 8 }}>
            <Ionicons name="arrow-back" size={24} color={Colors.primary} />
          </TouchableOpacity>
        ) : (
          <View style={styles.logoMark}>
            <Text style={styles.logoText}>🐾</Text>
          </View>
        )}

        <View style={styles.titleBlock}>
          <Text style={styles.title} numberOfLines={1}>{title}</Text>
          {subtitle ? <Text style={styles.subtitle} numberOfLines={1}>{subtitle}</Text> : null}
        </View>

        <View style={styles.right}>
          {rightComponent || null}
        </View>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: Colors.background,
    paddingHorizontal: Spacing.md,
    paddingBottom: Spacing.md,
    borderBottomWidth: 1,
    borderBottomColor: Colors.primary + '33',
  },
  row: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: Spacing.sm,
  },
  backBtn: {
    width: 36,
    height: 36,
    alignItems: 'center',
    justifyContent: 'center',
  },
  logoMark: {
    width: 36,
    height: 36,
    backgroundColor: Colors.primaryContainer,
    borderRadius: 18,
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 1,
    borderColor: Colors.primary + '55',
  },
  logoText: {
    fontSize: 18,
  },
  titleBlock: {
    flex: 1,
  },
  title: {
    ...Typography.heading3,
    color: Colors.text,
  },
  subtitle: {
    ...Typography.bodySmall,
    color: Colors.textSecondary,
    marginTop: 2,
  },
  right: {
    minWidth: 36,
    alignItems: 'flex-end',
  },
});
