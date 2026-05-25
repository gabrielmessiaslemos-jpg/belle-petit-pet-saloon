import React, { useState } from 'react';
import {
  StyleSheet, View, Text, FlatList,
  TouchableOpacity, ScrollView,
} from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { format, addDays, subDays, parseISO, isToday } from 'date-fns';
import { ptBR } from 'date-fns/locale';
import { useAppointments } from '../../hooks/useAppointments';
import { AppHeader } from '../../components/AppHeader';
import { AppointmentCard } from '../../components/AppointmentCard';
import { EmptyState } from '../../components/EmptyState';
import { Colors, Spacing, Radius, Typography } from '../../theme';

export function AppointmentsScreen({ navigation }: any) {
  const [selectedDate, setSelectedDate] = useState(
    format(new Date(), 'yyyy-MM-dd'),
  );
  const { appointments, loading } = useAppointments(selectedDate);

  // Generate 7-day strip centered on today
  const today = new Date();
  const days = Array.from({ length: 7 }, (_, i) => addDays(subDays(today, 3), i));

  function goToDay(delta: number) {
    const current = parseISO(selectedDate);
    setSelectedDate(format(addDays(current, delta), 'yyyy-MM-dd'));
  }

  const selectedParsed = parseISO(selectedDate);

  return (
    <View style={styles.container}>
      <AppHeader
        title="Agenda"
        subtitle={format(selectedParsed, "MMMM 'de' yyyy", { locale: ptBR })}
        rightComponent={
          <TouchableOpacity
            onPress={() => navigation.push('NewAppointment', {})}
            style={styles.addBtn}
          >
            <Ionicons name="add" size={22} color={Colors.primary} />
          </TouchableOpacity>
        }
      />

      {/* Week strip */}
      <View style={styles.weekStrip}>
        <TouchableOpacity onPress={() => goToDay(-7)} style={styles.navBtn}>
          <Ionicons name="chevron-back" size={18} color={Colors.textSecondary} />
        </TouchableOpacity>
        <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={styles.daysScroll}>
          {days.map((day) => {
            const dateStr = format(day, 'yyyy-MM-dd');
            const isSelected = dateStr === selectedDate;
            const isTodayDay = isToday(day);
            return (
              <TouchableOpacity
                key={dateStr}
                onPress={() => setSelectedDate(dateStr)}
                style={[
                  styles.dayBtn,
                  isSelected && styles.dayBtnSelected,
                ]}
              >
                <Text style={[styles.dayName, isSelected && styles.dayNameSelected]}>
                  {format(day, 'EEE', { locale: ptBR }).slice(0, 3)}
                </Text>
                <Text style={[styles.dayNum, isSelected && styles.dayNumSelected]}>
                  {format(day, 'dd')}
                </Text>
                {isTodayDay && <View style={[styles.todayDot, isSelected && styles.todayDotSelected]} />}
              </TouchableOpacity>
            );
          })}
        </ScrollView>
        <TouchableOpacity onPress={() => goToDay(7)} style={styles.navBtn}>
          <Ionicons name="chevron-forward" size={18} color={Colors.textSecondary} />
        </TouchableOpacity>
      </View>

      {/* Count badge */}
      <View style={styles.countRow}>
        <Text style={styles.countText}>
          {appointments.length} agendamento{appointments.length !== 1 ? 's' : ''}
        </Text>
      </View>

      {/* List */}
      {appointments.length === 0 && !loading ? (
        <EmptyState
          icon="📅"
          title="Nenhum agendamento"
          description={`Sem agendamentos para ${format(selectedParsed, "dd 'de' MMMM", { locale: ptBR })}`}
        />
      ) : (
        <FlatList
          data={appointments}
          keyExtractor={(item) => item.id}
          renderItem={({ item }) => (
            <AppointmentCard
              appointment={item}
              onPress={() => navigation.push('AppointmentDetail', { appointmentId: item.id })}
            />
          )}
          contentContainerStyle={styles.list}
          showsVerticalScrollIndicator={false}
        />
      )}

      {/* FAB */}
      <TouchableOpacity
        style={styles.fab}
        onPress={() => navigation.push('NewAppointment', {})}
      >
        <Ionicons name="add" size={28} color={Colors.onPrimary} />
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.background },
  addBtn: {
    width: 36, height: 36,
    backgroundColor: Colors.primaryContainer,
    borderRadius: Radius.sm,
    alignItems: 'center', justifyContent: 'center',
    borderWidth: 1, borderColor: Colors.primary + '55',
  },
  weekStrip: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: Colors.surface,
    paddingVertical: Spacing.sm,
    borderBottomWidth: 1,
    borderBottomColor: Colors.divider,
  },
  navBtn: {
    padding: Spacing.sm,
  },
  daysScroll: {
    paddingHorizontal: Spacing.xs,
    gap: Spacing.xs,
  },
  dayBtn: {
    width: 44,
    alignItems: 'center',
    paddingVertical: 8,
    borderRadius: Radius.md,
    gap: 2,
  },
  dayBtnSelected: {
    backgroundColor: Colors.primary,
  },
  dayName: {
    fontSize: 11,
    fontWeight: '600',
    color: Colors.textSecondary,
    textTransform: 'capitalize',
  },
  dayNameSelected: { color: Colors.onPrimary },
  dayNum: {
    fontSize: 16,
    fontWeight: '700',
    color: Colors.text,
  },
  dayNumSelected: { color: Colors.onPrimary },
  todayDot: {
    width: 5, height: 5,
    borderRadius: 3,
    backgroundColor: Colors.primary,
  },
  todayDotSelected: { backgroundColor: Colors.onPrimary },
  countRow: {
    paddingHorizontal: Spacing.md,
    paddingVertical: Spacing.sm,
  },
  countText: {
    ...Typography.bodySmall,
    color: Colors.textSecondary,
  },
  list: {
    paddingBottom: 100,
  },
  fab: {
    position: 'absolute',
    bottom: Spacing.xl,
    right: Spacing.lg,
    width: 58,
    height: 58,
    borderRadius: 29,
    backgroundColor: Colors.primary,
    alignItems: 'center',
    justifyContent: 'center',
    elevation: 6,
    shadowColor: Colors.primary,
    shadowOffset: { width: 0, height: 3 },
    shadowOpacity: 0.4,
    shadowRadius: 8,
  },
});
