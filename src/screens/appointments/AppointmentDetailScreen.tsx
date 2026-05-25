import React, { useState } from 'react';
import {
  StyleSheet, View, Text, ScrollView,
  TouchableOpacity, Alert,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { format, parseISO } from 'date-fns';
import { ptBR } from 'date-fns/locale';
import { AppHeader } from '../../components/AppHeader';
import { GoldCard } from '../../components/GoldCard';
import { GoldButton } from '../../components/GoldButton';
import { useAppointments } from '../../hooks/useAppointments';
import { Colors, Spacing, Typography, Radius } from '../../theme';
import { AppointmentStatus } from '../../types';

const STATUS_OPTIONS: { value: AppointmentStatus; label: string; color: string }[] = [
  { value: 'pendente',     label: 'Pendente',     color: Colors.statusPending },
  { value: 'confirmado',   label: 'Confirmado',   color: Colors.statusConfirmed },
  { value: 'em_andamento', label: 'Em andamento', color: Colors.info },
  { value: 'concluido',    label: 'Concluído',    color: Colors.statusDone },
  { value: 'cancelado',    label: 'Cancelado',    color: Colors.statusCancelled },
];

export function AppointmentDetailScreen({ navigation, route }: any) {
  const { appointmentId } = route.params;
  const { appointments, updateStatus, deleteAppointment } = useAppointments();
  const appointment = appointments.find((a) => a.id === appointmentId);

  if (!appointment) {
    return (
      <View style={styles.container}>
        <AppHeader title="Agendamento" onBack={() => navigation.goBack()} />
        <View style={styles.center}>
          <Text style={{ color: Colors.textSecondary }}>Agendamento não encontrado.</Text>
        </View>
      </View>
    );
  }

  const dateFormatted = format(parseISO(appointment.date), "dd 'de' MMMM 'de' yyyy", { locale: ptBR });
  const currentStatus = STATUS_OPTIONS.find((s) => s.value === appointment.status)!;

  function handleDelete() {
    Alert.alert(
      'Excluir agendamento',
      'Tem certeza que deseja excluir este agendamento?',
      [
        { text: 'Cancelar', style: 'cancel' },
        {
          text: 'Excluir',
          style: 'destructive',
          onPress: async () => {
            await deleteAppointment(appointmentId);
            navigation.goBack();
          },
        },
      ],
    );
  }

  return (
    <View style={styles.container}>
      <AppHeader
        title="Agendamento"
        onBack={() => navigation.goBack()}
        rightComponent={
          <TouchableOpacity onPress={() => navigation.push('NewAppointment', { appointmentId })} style={styles.editBtn}>
            <Ionicons name="pencil-outline" size={18} color={Colors.primary} />
          </TouchableOpacity>
        }
      />
      <ScrollView contentContainerStyle={styles.content} showsVerticalScrollIndicator={false}>

        {/* Pet & Service Header */}
        <GoldCard goldBorder style={styles.mainCard}>
          <Text style={styles.petName}>{appointment.petName}</Text>
          <Text style={styles.service}>{appointment.serviceName}</Text>
          <View style={styles.infoRow}>
            <Ionicons name="calendar-outline" size={15} color={Colors.textSecondary} />
            <Text style={styles.infoText}>{dateFormatted} às {appointment.time}</Text>
          </View>
          <View style={styles.infoRow}>
            <Ionicons name="person-outline" size={15} color={Colors.textSecondary} />
            <Text style={styles.infoText}>{appointment.clientName}</Text>
          </View>
          <Text style={styles.price}>
            {appointment.price.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}
          </Text>
        </GoldCard>

        {/* Status Selector */}
        <Text style={styles.sectionLabel}>Status</Text>
        <View style={styles.statusGrid}>
          {STATUS_OPTIONS.map((s) => (
            <TouchableOpacity
              key={s.value}
              style={[
                styles.statusBtn,
                { borderColor: s.color + '66' },
                appointment.status === s.value && { backgroundColor: s.color + '22', borderColor: s.color },
              ]}
              onPress={() => updateStatus(appointmentId, s.value)}
            >
              <Text style={[
                styles.statusBtnLabel,
                { color: appointment.status === s.value ? s.color : Colors.textSecondary },
              ]}>
                {s.label}
              </Text>
            </TouchableOpacity>
          ))}
        </View>

        {/* Notes */}
        {appointment.notes ? (
          <>
            <Text style={styles.sectionLabel}>Observações</Text>
            <GoldCard>
              <Text style={styles.notes}>{appointment.notes}</Text>
            </GoldCard>
          </>
        ) : null}

        {/* Delete */}
        <GoldButton
          label="Excluir agendamento"
          variant="outlined"
          onPress={handleDelete}
          fullWidth
          style={{ marginTop: Spacing.xl, borderColor: Colors.error }}
        />
        <View style={{ height: Spacing.xxl }} />
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.background },
  center: { flex: 1, alignItems: 'center', justifyContent: 'center' },
  editBtn: { padding: 6, backgroundColor: Colors.primaryContainer, borderRadius: Radius.sm },
  content: { padding: Spacing.md, gap: Spacing.sm },
  mainCard: { gap: Spacing.xs },
  petName: { ...Typography.heading2 },
  service: { ...Typography.body, color: Colors.textSecondary },
  infoRow: { flexDirection: 'row', alignItems: 'center', gap: Spacing.xs, marginTop: 4 },
  infoText: { ...Typography.bodySmall, color: Colors.textSecondary },
  price: { ...Typography.heading3, color: Colors.primary, marginTop: Spacing.sm },
  sectionLabel: { ...Typography.label, marginTop: Spacing.md },
  statusGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: Spacing.sm },
  statusBtn: {
    paddingHorizontal: Spacing.md, paddingVertical: 8,
    borderRadius: Radius.full, borderWidth: 1.5,
    borderColor: Colors.border,
  },
  statusBtnLabel: { fontSize: 13, fontWeight: '600' },
  notes: { ...Typography.body, lineHeight: 22 },
});
