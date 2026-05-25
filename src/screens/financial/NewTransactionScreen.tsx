import React, { useState, useEffect } from 'react';
import {
  StyleSheet, View, Text, TextInput, ScrollView,
  TouchableOpacity, Alert, Platform,
} from 'react-native';
import { format } from 'date-fns';
import { AppHeader } from '../../components/AppHeader';
import { GoldButton } from '../../components/GoldButton';
import { useFinancial } from '../../hooks/useFinancial';
import { Colors, Spacing, Radius, Typography } from '../../theme';
import { TransactionType, TransactionCategory } from '../../types';

const CATEGORIES: TransactionCategory[] = ['Serviço', 'Produto', 'Aluguel', 'Salário', 'Material', 'Conta', 'Outros'];

export function NewTransactionScreen({ navigation, route }: any) {
  const { transactionId } = route.params || {};
  const isEditing = !!transactionId;
  const { transactions, addTransaction, updateTransaction } = useFinancial();
  const existing = transactions.find((t) => t.id === transactionId);

  const [type, setType] = useState<TransactionType>('receita');
  const [amount, setAmount] = useState('');
  const [description, setDescription] = useState('');
  const [category, setCategory] = useState<TransactionCategory>('Serviço');
  const [date, setDate] = useState(format(new Date(), 'yyyy-MM-dd'));
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (existing) {
      setType(existing.type);
      setAmount(existing.amount.toString());
      setDescription(existing.description);
      setCategory(existing.category);
      setDate(existing.date);
    }
  }, [existing?.id]);

  async function handleSave() {
    if (!amount || !description.trim()) {
      Alert.alert('Atenção', 'Valor e descrição são obrigatórios.');
      return;
    }
    const parsed = parseFloat(amount.replace(',', '.'));
    if (isNaN(parsed) || parsed <= 0) {
      Alert.alert('Atenção', 'Insira um valor válido.');
      return;
    }
    setSaving(true);
    try {
      const data = { type, amount: parsed, description: description.trim(), category, date };
      if (isEditing) {
        await updateTransaction(transactionId, data);
      } else {
        await addTransaction(data);
      }
      navigation.goBack();
    } catch (e: any) {
      Alert.alert('Erro', e.message);
    } finally {
      setSaving(false);
    }
  }

  return (
    <View style={styles.container}>
      <AppHeader title={isEditing ? 'Editar Lançamento' : 'Novo Lançamento'} onBack={() => navigation.goBack()} />
      <ScrollView contentContainerStyle={styles.content} keyboardShouldPersistTaps="handled">

        {/* Type selector */}
        <Text style={styles.label}>Tipo *</Text>
        <View style={styles.typeRow}>
          {(['receita', 'despesa'] as TransactionType[]).map((t) => (
            <TouchableOpacity
              key={t}
              style={[
                styles.typeBtn,
                type === t && (t === 'receita' ? styles.typeBtnRevenue : styles.typeBtnExpense),
              ]}
              onPress={() => setType(t)}
            >
              <Text style={[
                styles.typeBtnLabel,
                type === t && { color: t === 'receita' ? Colors.success : Colors.error, fontWeight: '700' },
              ]}>
                {t === 'receita' ? '↓ Receita' : '↑ Despesa'}
              </Text>
            </TouchableOpacity>
          ))}
        </View>

        <Text style={[styles.label, { marginTop: Spacing.md }]}>Valor (R$) *</Text>
        <TextInput
          style={styles.input}
          value={amount}
          onChangeText={setAmount}
          placeholder="0,00"
          placeholderTextColor={Colors.textMuted}
          keyboardType="decimal-pad"
        />

        <Text style={[styles.label, { marginTop: Spacing.md }]}>Descrição *</Text>
        <TextInput
          style={styles.input}
          value={description}
          onChangeText={setDescription}
          placeholder="Ex: Banho + Tosa - Rex"
          placeholderTextColor={Colors.textMuted}
        />

        <Text style={[styles.label, { marginTop: Spacing.md }]}>Categoria</Text>
        <View style={styles.categoryGrid}>
          {CATEGORIES.map((c) => (
            <TouchableOpacity
              key={c}
              style={[styles.categoryBtn, category === c && styles.categoryBtnActive]}
              onPress={() => setCategory(c)}
            >
              <Text style={[styles.categoryLabel, category === c && styles.categoryLabelActive]}>{c}</Text>
            </TouchableOpacity>
          ))}
        </View>

        <Text style={[styles.label, { marginTop: Spacing.md }]}>Data</Text>
        <TextInput
          style={styles.input}
          value={date}
          onChangeText={setDate}
          placeholder="AAAA-MM-DD"
          placeholderTextColor={Colors.textMuted}
        />

        <GoldButton
          label={isEditing ? 'Salvar alterações' : 'Registrar lançamento'}
          onPress={handleSave}
          loading={saving}
          fullWidth
          style={{ marginTop: Spacing.xl }}
        />
        <View style={{ height: Spacing.xxl }} />
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.background },
  content: { padding: Spacing.md },
  label: { ...Typography.label, marginBottom: 6 },
  input: {
    backgroundColor: Colors.surface, color: Colors.text,
    borderRadius: Radius.md, borderWidth: 1, borderColor: Colors.border,
    paddingHorizontal: Spacing.md,
    paddingVertical: Platform.OS === 'ios' ? 13 : 10, fontSize: 15,
  },
  typeRow: { flexDirection: 'row', gap: Spacing.md },
  typeBtn: {
    flex: 1, paddingVertical: 12, borderRadius: Radius.md,
    borderWidth: 1.5, borderColor: Colors.border,
    backgroundColor: Colors.surface, alignItems: 'center',
  },
  typeBtnRevenue: { borderColor: Colors.success, backgroundColor: Colors.successContainer },
  typeBtnExpense: { borderColor: Colors.error, backgroundColor: Colors.errorContainer },
  typeBtnLabel: { fontSize: 15, fontWeight: '500', color: Colors.textSecondary },
  categoryGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: Spacing.sm },
  categoryBtn: {
    paddingHorizontal: Spacing.md, paddingVertical: 8,
    borderRadius: Radius.full, borderWidth: 1, borderColor: Colors.border,
    backgroundColor: Colors.surface,
  },
  categoryBtnActive: { borderColor: Colors.primary, backgroundColor: Colors.primaryContainer },
  categoryLabel: { fontSize: 13, color: Colors.textSecondary },
  categoryLabelActive: { color: Colors.primary, fontWeight: '600' },
});
