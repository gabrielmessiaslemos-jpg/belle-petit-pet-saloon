import React from 'react';
import { StyleSheet, View, Text, TouchableOpacity } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { GoldCard } from './GoldCard';
import { Colors, Spacing, Typography, Radius } from '../theme';
import { Appointment, AppointmentStatus } from '../types';

const STATUS_CONFIG: Record<AppointmentStatus, { label: string; color: string; icon: keyof typeof Ionicons.glyphMap }> = {
  pendente:      { label: 'Pendente',      color: Colors.statusPending,   icon: 'time-outline' },
  confirmado:    { label: 'Confirmado',    color: Colors.statusConfirmed, icon: 'checkmark-circle-outline' },
  em_andamento:  { label: 'Em andamento',  color: Colors.info,            icon: 'cut-outline' },
  concluido:     { label: 'Concluído',     color: Colors.statusDone,      icon: 'checkmark-done-outline' },
  cancelado:     { label: 'Cancelado',     color: Colors.statusCancelled, icon: 'close-circle-outline' },
};

interface AppointmentCardProps {
  appointment: Appointment;
  onPress?: () => void;
}

export function AppointmentCard({ appointment, onPress }: AppointmentCardProps) {
  const status = STATUS_CONFIG[appointment.status];

  return (
    <GoldCard onPress={onPress} style={styles.card}>
      {/* Time + Status */}
      <View style={styles.topRow}>
        <View style={styles.timeBlock}>
          <Ionicons name="time-outline" size={14} color={Colors.primary} />
          <Text style={styles.time}>{appointment.time}</Text>
        </View>
        <View style={[styles.statusBadge, { backgroundColor: status.color + '22' }]}>
          <Ionicons name={status.icon} size={12} color={status.color} />
          <Text style={[styles.statusLabel, { color: status.color }]}>{status.label}</Text>
        </View>
      </View>

      {/* Pet & Service */}
      <Text style={styles.petName}>{appointment.petName}</Text>
      <Text style={styles.service}>{appointment.serviceName}</Text>

      {/* Client + Price */}
      <View style={styles.bottomRow}>
        <View style={styles.clientRow}>
          <Ionicons name="person-outline" size={13} color={Colors.textSecondary} />
          <Text style={styles.clientName}>{appointment.clientName}</Text>
        </View>
        <Text style={styles.price}>
          {appointment.price.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}
        </Text>
      </View>
    </GoldCard>
  );
}

const styles = StyleSheet.create({
  card: {
    marginHorizontal: Spacing.md,
    marginVertical: Spacing.xs,
    gap: Spacing.xs,
  },
  topRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  timeBlock: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
  },
  time: {
    ...Typography.label,
    fontSize: 14,
  },
  statusBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: Radius.full,
  },
  statusLabel: {
    fontSize: 11,
    fontWeight: '600',
  },
  petName: {
    ...Typography.heading3,
    fontSize: 16,
    marginTop: 2,
  },
  service: {
    ...Typography.bodySmall,
    color: Colors.textSecondary,
  },
  bottomRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginTop: Spacing.xs,
  },
  clientRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
  },
  clientName: {
    ...Typography.bodySmall,
    color: Colors.textSecondary,
  },
  price: {
    ...Typography.label,
    fontSize: 15,
    color: Colors.primary,
  },
});
