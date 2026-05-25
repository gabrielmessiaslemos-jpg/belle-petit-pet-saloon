import React, { useState, useEffect } from 'react';
import {
  StyleSheet, View, Text, TextInput, ScrollView,
  TouchableOpacity, Alert, Platform, Switch,
} from 'react-native';
import { AppHeader } from '../../components/AppHeader';
import { GoldButton } from '../../components/GoldButton';
import { useServices } from '../../hooks/useServices';
import { Colors, Spacing, Radius, Typography } from '../../theme';
import { ServiceCategory } from '../../types';

const CATEGORIES: ServiceCategory[] = ['Banho', 'Tosa', 'Banho + Tosa', 'Consulta', 'Hotel', 'Outros'];

export function NewServiceScreen({ navigation, route }: any) {
  const { serviceId } = route.params || {};
  const isEditing = !!serviceId;
  const { services, addService, updateService } = useServices();
  const existing = services.find((s) => s.id === serviceId);

  const [name, setName] = useState('');
  const [category, setCategory] = useState<ServiceCategory>('Banho');
  const [price, setPrice] = useState('');
  const [duration, setDuration] = useState('60');
  const [description, setDescription] = useState('');
  const [active, setActive] = useState(true);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (existing) {
      setName(existing.name);
      setCategory(existing.category);
      setPrice(existing.price.toString());
      setDuration(existing.durationMinutes.toString());
      setDescription(existing.description || '');
      setActive(existing.active);
    }
  }, [existing?.id]);

  async function handleSave() {
    if (!name.trim() || !price) {
      Alert.alert('Atenção', 'Nome e preço são obrigatórios.');
      return;
    }
    const parsedPrice = parseFloat(price.replace(',', '.'));
    if (isNaN(parsedPrice) || parsedPrice < 0) {
      Alert.alert('Atenção', 'Insira um preço válido.'); return;
    }
    setSaving(true);
    try {
      const data = {
        name: name.trim(), category,
        price: parsedPrice,
        durationMinutes: parseInt(duration) || 60,
        description,
        active,
      };
      if (isEditing) { await updateService(serviceId, data); }
      else { await addService(data); }
      navigation.goBack();
    } catch (e: any) {
      Alert.alert('Erro', e.message);
    } finally {
      setSaving(false);
    }
  }

  return (
    <View style={styles.container}>
      <AppHeader title={isEditing ? 'Editar Serviço' : 'Novo Serviço'} onBack={() => navigation.goBack()} />
      <ScrollView contentContainerStyle={styles.content} keyboardShouldPersistTaps="handled">

        <Text style={styles.label}>Categoria *</Text>
        <View style={styles.categoryGrid}>
          {CATEGORIES.map((c) => (
            <TouchableOpacity
              key={c}
              style={[styles.catBtn, category === c && styles.catBtnActive]}
              onPress={() => setCategory(c)}
            >
              <Text style={[styles.catLabel, category === c && styles.catLabelActive]}>{c}</Text>
            </TouchableOpacity>
          ))}
        </View>

        <Text style={[styles.label, { marginTop: Spacing.md }]}>Nome do serviço *</Text>
        <TextInput style={styles.input} value={name} onChangeText={setName} placeholder="Ex: Banho Especial" placeholderTextColor={Colors.textMuted} />

        <View style={styles.row}>
          <View style={{ flex: 1 }}>
            <Text style={[styles.label, { marginTop: Spacing.md }]}>Preço (R$) *</Text>
            <TextInput style={styles.input} value={price} onChangeText={setPrice} placeholder="0,00" placeholderTextColor={Colors.textMuted} keyboardType="decimal-pad" />
          </View>
          <View style={{ flex: 1 }}>
            <Text style={[styles.label, { marginTop: Spacing.md }]}>Duração (min)</Text>
            <TextInput style={styles.input} value={duration} onChangeText={setDuration} placeholder="60" placeholderTextColor={Colors.textMuted} keyboardType="number-pad" />
          </View>
        </View>

        <Text style={[styles.label, { marginTop: Spacing.md }]}>Descrição</Text>
        <TextInput
          style={[styles.input, styles.textarea]}
          value={description}
          onChangeText={setDescription}
          placeholder="Inclui secagem, perfume..."
          placeholderTextColor={Colors.textMuted}
          multiline numberOfLines={3}
        />

        <View style={styles.activeRow}>
          <Text style={styles.label}>Serviço ativo</Text>
          <Switch
            value={active}
            onValueChange={setActive}
            trackColor={{ false: Colors.border, true: Colors.primary + '66' }}
            thumbColor={active ? Colors.primary : Colors.textMuted}
          />
        </View>

        <GoldButton
          label={isEditing ? 'Salvar alterações' : 'Cadastrar serviço'}
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
  textarea: { textAlignVertical: 'top', minHeight: 80 },
  row: { flexDirection: 'row', gap: Spacing.md },
  categoryGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: Spacing.sm },
  catBtn: {
    paddingHorizontal: Spacing.md, paddingVertical: 8,
    borderRadius: Radius.full, borderWidth: 1, borderColor: Colors.border,
    backgroundColor: Colors.surface,
  },
  catBtnActive: { backgroundColor: Colors.primaryContainer, borderColor: Colors.primary },
  catLabel: { fontSize: 13, color: Colors.textSecondary },
  catLabelActive: { color: Colors.primary, fontWeight: '700' },
  activeRow: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', marginTop: Spacing.lg },
});
