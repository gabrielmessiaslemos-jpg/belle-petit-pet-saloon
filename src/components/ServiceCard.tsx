import React from 'react';
import { StyleSheet, View, Text } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { GoldCard } from './GoldCard';
import { Colors, Spacing, Typography, Radius } from '../theme';
import { Service } from '../types';

const CATEGORY_ICONS: Record<string, keyof typeof Ionicons.glyphMap> = {
  'Banho':         'water-outline',
  'Tosa':          'cut-outline',
  'Banho + Tosa':  'sparkles-outline',
  'Consulta':      'medkit-outline',
  'Hotel':         'bed-outline',
  'Outros':        'ellipsis-horizontal-outline',
};

interface ServiceCardProps {
  service: Service;
  onPress?: () => void;
}

export function ServiceCard({ service, onPress }: ServiceCardProps) {
  const icon = CATEGORY_ICONS[service.category] || 'paw-outline';

  return (
    <GoldCard onPress={onPress} style={styles.card}>
      <View style={styles.row}>
        <View style={styles.iconBox}>
          <Ionicons name={icon} size={22} color={Colors.primary} />
        </View>
        <View style={styles.info}>
          <Text style={styles.name} numberOfLines={1}>{service.name}</Text>
          <Text style={styles.category}>{service.category} · {service.durationMinutes} min</Text>
        </View>
        <View style={styles.priceBlock}>
          <Text style={styles.price}>
            {service.price.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}
          </Text>
          {!service.active && (
            <View style={styles.inactiveBadge}>
              <Text style={styles.inactiveLabel}>Inativo</Text>
            </View>
          )}
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
  iconBox: {
    width: 42,
    height: 42,
    borderRadius: Radius.sm,
    backgroundColor: Colors.primaryContainer,
    alignItems: 'center',
    justifyContent: 'center',
  },
  info: {
    flex: 1,
    gap: 3,
  },
  name: {
    ...Typography.body,
    fontWeight: '600',
  },
  category: {
    ...Typography.bodySmall,
    color: Colors.textSecondary,
  },
  priceBlock: {
    alignItems: 'flex-end',
    gap: 4,
  },
  price: {
    ...Typography.label,
    fontSize: 15,
  },
  inactiveBadge: {
    backgroundColor: Colors.error + '22',
    borderRadius: Radius.full,
    paddingHorizontal: 6,
    paddingVertical: 2,
  },
  inactiveLabel: {
    fontSize: 10,
    fontWeight: '600',
    color: Colors.error,
  },
});
