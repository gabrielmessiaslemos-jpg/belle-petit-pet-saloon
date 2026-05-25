import React, { useState } from 'react';
import {
  StyleSheet, View, Text, FlatList,
  TouchableOpacity, ScrollView,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { format, addMonths, subMonths, parseISO } from 'date-fns';
import { ptBR } from 'date-fns/locale';
import { AppHeader } from '../../components/AppHeader';
import { GoldCard } from '../../components/GoldCard';
import { EmptyState } from '../../components/EmptyState';
import { useFinancial } from '../../hooks/useFinancial';
import { Colors, Spacing, Typography, Radius } from '../../theme';
import { Transaction } from '../../types';

function TransactionItem({ item, onPress }: { item: Transaction; onPress: () => void }) {
  const isRevenue = item.type === 'receita';
  return (
    <TouchableOpacity onPress={onPress}>
      <View style={transStyles.row}>
        <View style={[transStyles.iconBox, { backgroundColor: isRevenue ? Colors.successContainer : Colors.errorContainer }]}>
          <Ionicons
            name={isRevenue ? 'arrow-down-outline' : 'arrow-up-outline'}
            size={18}
            color={isRevenue ? Colors.success : Colors.error}
          />
        </View>
        <View style={{ flex: 1 }}>
          <Text style={transStyles.desc} numberOfLines={1}>{item.description}</Text>
          <Text style={transStyles.category}>{item.category} · {item.date}</Text>
        </View>
        <Text style={[transStyles.amount, { color: isRevenue ? Colors.success : Colors.error }]}>
          {isRevenue ? '+' : '-'} {item.amount.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}
        </Text>
      </View>
    </TouchableOpacity>
  );
}

const transStyles = StyleSheet.create({
  row: { flexDirection: 'row', alignItems: 'center', gap: Spacing.md, paddingHorizontal: Spacing.md, paddingVertical: 10, borderBottomWidth: 1, borderBottomColor: Colors.divider },
  iconBox: { width: 36, height: 36, borderRadius: Radius.sm, alignItems: 'center', justifyContent: 'center' },
  desc: { ...Typography.body, fontWeight: '500' },
  category: { ...Typography.caption, color: Colors.textMuted, marginTop: 2 },
  amount: { fontSize: 15, fontWeight: '700' },
});

export function FinancialScreen({ navigation }: any) {
  const [month, setMonth] = useState(format(new Date(), 'yyyy-MM'));
  const { transactions, summary, loading } = useFinancial(month);

  const monthDate = parseISO(`${month}-01`);
  const monthLabel = format(monthDate, "MMMM 'de' yyyy", { locale: ptBR });

  function prevMonth() { setMonth(format(subMonths(monthDate, 1), 'yyyy-MM')); }
  function nextMonth() { setMonth(format(addMonths(monthDate, 1), 'yyyy-MM')); }

  // Simple bar visualization
  const maxVal = Math.max(summary.revenue, summary.expenses, 1);
  const revenueBar = (summary.revenue / maxVal) * 100;
  const expensesBar = (summary.expenses / maxVal) * 100;

  return (
    <View style={styles.container}>
      <AppHeader
        title="Financeiro"
        rightComponent={
          <TouchableOpacity
            style={styles.addBtn}
            onPress={() => navigation.push('NewTransaction', {})}
          >
            <Ionicons name="add" size={22} color={Colors.primary} />
          </TouchableOpacity>
        }
      />

      <ScrollView showsVerticalScrollIndicator={false}>
        {/* Month selector */}
        <View style={styles.monthRow}>
          <TouchableOpacity onPress={prevMonth} style={styles.monthBtn}>
            <Ionicons name="chevron-back" size={20} color={Colors.primary} />
          </TouchableOpacity>
          <Text style={styles.monthLabel}>{monthLabel}</Text>
          <TouchableOpacity onPress={nextMonth} style={styles.monthBtn}>
            <Ionicons name="chevron-forward" size={20} color={Colors.primary} />
          </TouchableOpacity>
        </View>

        {/* Summary Cards */}
        <View style={styles.summaryRow}>
          <GoldCard style={styles.summaryCard}>
            <Ionicons name="trending-up-outline" size={20} color={Colors.success} />
            <Text style={styles.summaryValue}>{summary.revenue.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}</Text>
            <Text style={styles.summaryLabel}>Receitas</Text>
          </GoldCard>
          <GoldCard style={styles.summaryCard}>
            <Ionicons name="trending-down-outline" size={20} color={Colors.error} />
            <Text style={[styles.summaryValue, { color: Colors.error }]}>{summary.expenses.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}</Text>
            <Text style={styles.summaryLabel}>Despesas</Text>
          </GoldCard>
          <GoldCard style={[styles.summaryCard, { borderWidth: 1, borderColor: summary.balance >= 0 ? Colors.primary + '55' : Colors.error + '55' }]}>
            <Ionicons name="wallet-outline" size={20} color={summary.balance >= 0 ? Colors.primary : Colors.error} />
            <Text style={[styles.summaryValue, { color: summary.balance >= 0 ? Colors.primary : Colors.error }]}>
              {summary.balance.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}
            </Text>
            <Text style={styles.summaryLabel}>Saldo</Text>
          </GoldCard>
        </View>

        {/* Bar chart */}
        <GoldCard style={styles.chartCard}>
          <Text style={styles.chartTitle}>Visão geral</Text>
          <View style={styles.barRow}>
            <Text style={styles.barLabel}>Receitas</Text>
            <View style={styles.barTrack}>
              <View style={[styles.barFill, { width: `${revenueBar}%`, backgroundColor: Colors.success }]} />
            </View>
          </View>
          <View style={styles.barRow}>
            <Text style={styles.barLabel}>Despesas</Text>
            <View style={styles.barTrack}>
              <View style={[styles.barFill, { width: `${expensesBar}%`, backgroundColor: Colors.error }]} />
            </View>
          </View>
        </GoldCard>

        {/* Transactions list */}
        <Text style={styles.sectionTitle}>Lançamentos ({transactions.length})</Text>
        {transactions.length === 0 && !loading ? (
          <EmptyState icon="💰" title="Nenhum lançamento" description="Registre receitas e despesas do mês." />
        ) : (
          <GoldCard style={{ padding: 0, overflow: 'hidden', marginHorizontal: Spacing.md }}>
            {transactions.map((t) => (
              <TransactionItem
                key={t.id}
                item={t}
                onPress={() => navigation.push('NewTransaction', { transactionId: t.id })}
              />
            ))}
          </GoldCard>
        )}
        <View style={{ height: 100 }} />
      </ScrollView>

      {/* FAB */}
      <TouchableOpacity style={styles.fab} onPress={() => navigation.push('NewTransaction', {})}>
        <Ionicons name="add" size={28} color={Colors.onPrimary} />
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.background },
  addBtn: {
    width: 36, height: 36, backgroundColor: Colors.primaryContainer,
    borderRadius: Radius.sm, alignItems: 'center', justifyContent: 'center',
    borderWidth: 1, borderColor: Colors.primary + '55',
  },
  monthRow: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', paddingVertical: Spacing.md, gap: Spacing.lg },
  monthBtn: { padding: Spacing.sm },
  monthLabel: { ...Typography.heading3, textTransform: 'capitalize', minWidth: 180, textAlign: 'center' },
  summaryRow: { flexDirection: 'row', paddingHorizontal: Spacing.md, gap: Spacing.sm },
  summaryCard: { flex: 1, alignItems: 'center', gap: 4, paddingVertical: Spacing.md },
  summaryValue: { fontSize: 13, fontWeight: '700', color: Colors.text, textAlign: 'center' },
  summaryLabel: { ...Typography.caption, color: Colors.textSecondary },
  chartCard: { marginHorizontal: Spacing.md, marginTop: Spacing.md, gap: Spacing.sm },
  chartTitle: { ...Typography.label },
  barRow: { flexDirection: 'row', alignItems: 'center', gap: Spacing.sm },
  barLabel: { ...Typography.bodySmall, color: Colors.textSecondary, width: 70 },
  barTrack: { flex: 1, height: 10, backgroundColor: Colors.divider, borderRadius: Radius.full, overflow: 'hidden' },
  barFill: { height: '100%', borderRadius: Radius.full },
  sectionTitle: { ...Typography.heading3, paddingHorizontal: Spacing.md, marginTop: Spacing.lg, marginBottom: Spacing.sm },
  fab: {
    position: 'absolute', bottom: Spacing.xl, right: Spacing.lg,
    width: 58, height: 58, borderRadius: 29,
    backgroundColor: Colors.primary,
    alignItems: 'center', justifyContent: 'center',
    elevation: 6,
    shadowColor: Colors.primary,
    shadowOffset: { width: 0, height: 3 }, shadowOpacity: 0.4, shadowRadius: 8,
  },
});
