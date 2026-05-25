import React from 'react';
import {
  StyleSheet, View, Text, ScrollView,
  TouchableOpacity, RefreshControl,
} from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { format } from 'date-fns';
import { ptBR } from 'date-fns/locale';
import { useAuth } from '../../context/AuthContext';
import { useTodayAppointments } from '../../hooks/useAppointments';
import { useFinancial } from '../../hooks/useFinancial';
import { GoldCard } from '../../components/GoldCard';
import { AppointmentCard } from '../../components/AppointmentCard';
import { EmptyState } from '../../components/EmptyState';
import { Colors, Spacing, Typography, Radius } from '../../theme';

export function DashboardScreen({ navigation }: any) {
  const insets = useSafeAreaInsets();
  const { signOut } = useAuth();
  const { appointments, loading: loadingAppts } = useTodayAppointments();
  const { summary, loading: loadingFin } = useFinancial();

  const today = format(new Date(), "EEEE, dd 'de' MMMM", { locale: ptBR });
  const todayRevenue = appointments
    .filter((a) => a.status === 'concluido')
    .reduce((sum, a) => sum + a.price, 0);

  const pendingCount = appointments.filter(
    (a) => a.status === 'pendente' || a.status === 'confirmado',
  ).length;

  return (
    <ScrollView
      style={[styles.container, { paddingTop: insets.top }]}
      contentContainerStyle={styles.content}
      showsVerticalScrollIndicator={false}
    >
      {/* Header */}
      <View style={styles.header}>
        <View>
          <Text style={styles.greeting}>Olá, Belle Petit 🐾</Text>
          <Text style={styles.date}>{today}</Text>
        </View>
        <TouchableOpacity onPress={signOut} style={styles.logoutBtn}>
          <Ionicons name="log-out-outline" size={22} color={Colors.textSecondary} />
        </TouchableOpacity>
      </View>

      {/* Stats Row */}
      <View style={styles.statsRow}>
        <GoldCard style={styles.statCard} goldBorder>
          <Ionicons name="calendar-outline" size={22} color={Colors.primary} />
          <Text style={styles.statValue}>{appointments.length}</Text>
          <Text style={styles.statLabel}>Hoje</Text>
        </GoldCard>
        <GoldCard style={styles.statCard} goldBorder>
          <Ionicons name="time-outline" size={22} color={Colors.statusPending} />
          <Text style={[styles.statValue, { color: Colors.statusPending }]}>{pendingCount}</Text>
          <Text style={styles.statLabel}>Pendentes</Text>
        </GoldCard>
        <GoldCard style={styles.statCard} goldBorder>
          <Ionicons name="cash-outline" size={22} color={Colors.success} />
          <Text style={[styles.statValue, { color: Colors.success, fontSize: 15 }]}>
            {todayRevenue.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}
          </Text>
          <Text style={styles.statLabel}>Hoje</Text>
        </GoldCard>
      </View>

      {/* Quick Actions */}
      <Text style={styles.sectionTitle}>Ações Rápidas</Text>
      <View style={styles.actionsRow}>
        {[
          { icon: 'add-circle-outline', label: 'Agendar',   tab: 'Appointments' },
          { icon: 'person-add-outline',  label: 'Cliente',   tab: 'Clients' },
          { icon: 'cash-outline',        label: 'Lançar',    tab: 'Financial' },
          { icon: 'cut-outline',         label: 'Serviços',  tab: 'Services' },
        ].map((action) => (
          <TouchableOpacity
            key={action.tab}
            style={styles.actionBtn}
            onPress={() => navigation.navigate(action.tab)}
          >
            <View style={styles.actionIcon}>
              <Ionicons name={action.icon as any} size={24} color={Colors.primary} />
            </View>
            <Text style={styles.actionLabel}>{action.label}</Text>
          </TouchableOpacity>
        ))}
      </View>

      {/* Today's Appointments */}
      <View style={styles.sectionHeader}>
        <Text style={styles.sectionTitle}>Agenda de Hoje</Text>
        <TouchableOpacity onPress={() => navigation.navigate('Appointments')}>
          <Text style={styles.seeAll}>Ver tudo</Text>
        </TouchableOpacity>
      </View>

      {appointments.length === 0 && !loadingAppts ? (
        <EmptyState
          icon="📅"
          title="Nenhum agendamento hoje"
          description="Que tal aproveitar o dia?"
        />
      ) : (
        appointments.slice(0, 5).map((a) => (
          <AppointmentCard
            key={a.id}
            appointment={a}
            onPress={() =>
              navigation.navigate('Appointments', {
                screen: 'AppointmentDetail',
                params: { appointmentId: a.id },
              })
            }
          />
        ))
      )}

      {/* Monthly summary teaser */}
      <Text style={[styles.sectionTitle, { marginTop: Spacing.lg }]}>Resumo do Mês</Text>
      <GoldCard style={styles.summaryCard}>
        <View style={styles.summaryRow}>
          <View style={styles.summaryItem}>
            <Text style={styles.summaryLabel}>Receitas</Text>
            <Text style={[styles.summaryValue, { color: Colors.success }]}>
              {summary.revenue.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}
            </Text>
          </View>
          <View style={styles.summaryDivider} />
          <View style={styles.summaryItem}>
            <Text style={styles.summaryLabel}>Despesas</Text>
            <Text style={[styles.summaryValue, { color: Colors.error }]}>
              {summary.expenses.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}
            </Text>
          </View>
          <View style={styles.summaryDivider} />
          <View style={styles.summaryItem}>
            <Text style={styles.summaryLabel}>Saldo</Text>
            <Text style={[
              styles.summaryValue,
              { color: summary.balance >= 0 ? Colors.primary : Colors.error },
            ]}>
              {summary.balance.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}
            </Text>
          </View>
        </View>
      </GoldCard>

      <View style={{ height: Spacing.xxl }} />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
  },
  content: {
    paddingBottom: Spacing.xl,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    paddingHorizontal: Spacing.md,
    paddingVertical: Spacing.md,
    borderBottomWidth: 1,
    borderBottomColor: Colors.primary + '33',
  },
  greeting: {
    ...Typography.heading2,
    color: Colors.primary,
  },
  date: {
    ...Typography.bodySmall,
    color: Colors.textSecondary,
    marginTop: 2,
    textTransform: 'capitalize',
  },
  logoutBtn: {
    padding: Spacing.sm,
  },
  statsRow: {
    flexDirection: 'row',
    gap: Spacing.sm,
    paddingHorizontal: Spacing.md,
    marginTop: Spacing.lg,
  },
  statCard: {
    flex: 1,
    alignItems: 'center',
    gap: Spacing.xs,
    paddingVertical: Spacing.md,
  },
  statValue: {
    ...Typography.heading2,
    color: Colors.primary,
    fontSize: 20,
  },
  statLabel: {
    ...Typography.caption,
    color: Colors.textSecondary,
  },
  sectionTitle: {
    ...Typography.heading3,
    paddingHorizontal: Spacing.md,
    marginTop: Spacing.lg,
    marginBottom: Spacing.sm,
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: Spacing.md,
    marginTop: Spacing.lg,
    marginBottom: Spacing.sm,
  },
  seeAll: {
    ...Typography.label,
    fontSize: 13,
  },
  actionsRow: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    paddingHorizontal: Spacing.md,
    gap: Spacing.sm,
  },
  actionBtn: {
    alignItems: 'center',
    gap: Spacing.xs,
  },
  actionIcon: {
    width: 54,
    height: 54,
    borderRadius: Radius.md,
    backgroundColor: Colors.primaryContainer,
    borderWidth: 1,
    borderColor: Colors.primary + '44',
    alignItems: 'center',
    justifyContent: 'center',
  },
  actionLabel: {
    ...Typography.caption,
    color: Colors.textSecondary,
    fontSize: 12,
  },
  summaryCard: {
    marginHorizontal: Spacing.md,
  },
  summaryRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  summaryItem: {
    flex: 1,
    alignItems: 'center',
    gap: 4,
  },
  summaryLabel: {
    ...Typography.caption,
    color: Colors.textSecondary,
  },
  summaryValue: {
    fontSize: 14,
    fontWeight: '700',
    color: Colors.text,
  },
  summaryDivider: {
    width: 1,
    height: 36,
    backgroundColor: Colors.divider,
  },
});
