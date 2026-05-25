import React from 'react';
import { StyleSheet, View, Text } from 'react-native';
import { Colors, Spacing, Typography } from '../theme';

interface EmptyStateProps {
  icon?: string;
  title: string;
  description?: string;
  action?: React.ReactNode;
}

export function EmptyState({ icon = '🐾', title, description, action }: EmptyStateProps) {
  return (
    <View style={styles.container}>
      <Text style={styles.icon}>{icon}</Text>
      <Text style={styles.title}>{title}</Text>
      {description ? <Text style={styles.description}>{description}</Text> : null}
      {action ? <View style={styles.action}>{action}</View> : null}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: Spacing.xl,
    paddingVertical: Spacing.xxl,
    gap: Spacing.sm,
  },
  icon: {
    fontSize: 56,
    marginBottom: Spacing.sm,
  },
  title: {
    ...Typography.heading3,
    color: Colors.textSecondary,
    textAlign: 'center',
  },
  description: {
    ...Typography.bodySmall,
    color: Colors.textMuted,
    textAlign: 'center',
    lineHeight: 20,
  },
  action: {
    marginTop: Spacing.md,
  },
});
