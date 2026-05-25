import React from 'react';
import { StyleSheet, View, Text } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { GoldCard } from './GoldCard';
import { Colors, Spacing, Typography } from '../theme';
import { Client } from '../types';

interface ClientCardProps {
  client: Client;
  petsCount?: number;
  onPress?: () => void;
}

export function ClientCard({ client, petsCount = 0, onPress }: ClientCardProps) {
  const initials = client.name
    .split(' ')
    .slice(0, 2)
    .map((n) => n[0])
    .join('')
    .toUpperCase();

  return (
    <GoldCard onPress={onPress} style={styles.card}>
      <View style={styles.row}>
        {/* Avatar */}
        <View style={styles.avatar}>
          <Text style={styles.initials}>{initials}</Text>
        </View>

        {/* Info */}
        <View style={styles.info}>
          <Text style={styles.name} numberOfLines={1}>{client.name}</Text>
          <View style={styles.detailRow}>
            <Ionicons name="call-outline" size={12} color={Colors.textMuted} />
            <Text style={styles.phone}>{client.phone}</Text>
          </View>
        </View>

        {/* Pets count */}
        <View style={styles.petsTag}>
          <Text style={styles.petsEmoji}>🐾</Text>
          <Text style={styles.petsCount}>{petsCount}</Text>
        </View>
      </View>
    </GoldCard>
  );
}

const styles = StyleSheet.create({
  card: {
    marginHorizontal: Spacing.md,
    marginVertical: Spacing.xs,
  },
  row: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: Spacing.md,
  },
  avatar: {
    width: 46,
    height: 46,
    borderRadius: 23,
    backgroundColor: Colors.primaryContainer,
    borderWidth: 1.5,
    borderColor: Colors.primary + '66',
    alignItems: 'center',
    justifyContent: 'center',
  },
  initials: {
    fontSize: 16,
    fontWeight: '700',
    color: Colors.primary,
  },
  info: {
    flex: 1,
    gap: 3,
  },
  name: {
    ...Typography.body,
    fontWeight: '600',
  },
  detailRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
  },
  phone: {
    ...Typography.bodySmall,
    color: Colors.textSecondary,
  },
  petsTag: {
    alignItems: 'center',
    gap: 2,
  },
  petsEmoji: {
    fontSize: 16,
  },
  petsCount: {
    fontSize: 12,
    fontWeight: '700',
    color: Colors.primary,
  },
});
