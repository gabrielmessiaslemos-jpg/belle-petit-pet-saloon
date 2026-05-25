import React, { useState, useEffect } from 'react';
import {
  StyleSheet, View, Text, TextInput, ScrollView,
  TouchableOpacity, Alert, Platform,
} from 'react-native';
import { AppHeader } from '../../components/AppHeader';
import { GoldButton } from '../../components/GoldButton';
import { usePets } from '../../hooks/useClients';
import { Colors, Spacing, Radius, Typography } from '../../theme';
import { PetSpecies } from '../../types';

const SPECIES: PetSpecies[] = ['Cachorro', 'Gato', 'Outro'];

export function NewPetScreen({ navigation, route }: any) {
  const { clientId, petId } = route.params;
  const isEditing = !!petId;
  const { pets, addPet, updatePet } = usePets(clientId);
  const existing = pets.find((p) => p.id === petId);

  const [name, setName] = useState('');
  const [species, setSpecies] = useState<PetSpecies>('Cachorro');
  const [breed, setBreed] = useState('');
  const [weight, setWeight] = useState('');
  const [birthDate, setBirthDate] = useState('');
  const [notes, setNotes] = useState('');
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (existing) {
      setName(existing.name);
      setSpecies(existing.species);
      setBreed(existing.breed);
      setWeight(existing.weight?.toString() || '');
      setBirthDate(existing.birthDate || '');
      setNotes(existing.notes || '');
    }
  }, [existing?.id]);

  async function handleSave() {
    if (!name.trim() || !breed.trim()) {
      Alert.alert('Atenção', 'Nome e raça são obrigatórios.');
      return;
    }
    setSaving(true);
    try {
      const data = {
        clientId,
        name: name.trim(),
        species,
        breed: breed.trim(),
        weight: weight ? parseFloat(weight) : undefined,
        birthDate,
        notes,
      };
      if (isEditing) {
        await updatePet(petId, data);
      } else {
        await addPet(data);
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
      <AppHeader title={isEditing ? 'Editar Pet' : 'Novo Pet'} onBack={() => navigation.goBack()} />
      <ScrollView contentContainerStyle={styles.content} keyboardShouldPersistTaps="handled">

        {/* Species selector */}
        <Text style={styles.label}>Espécie *</Text>
        <View style={styles.speciesRow}>
          {SPECIES.map((s) => (
            <TouchableOpacity
              key={s}
              style={[styles.speciesBtn, species === s && styles.speciesBtnActive]}
              onPress={() => setSpecies(s)}
            >
              <Text style={styles.speciesEmoji}>{s === 'Cachorro' ? '🐶' : s === 'Gato' ? '🐱' : '🐾'}</Text>
              <Text style={[styles.speciesLabel, species === s && styles.speciesLabelActive]}>{s}</Text>
            </TouchableOpacity>
          ))}
        </View>

        <Text style={[styles.label, { marginTop: Spacing.md }]}>Nome *</Text>
        <TextInput style={styles.input} value={name} onChangeText={setName} placeholder="Nome do pet" placeholderTextColor={Colors.textMuted} />

        <Text style={[styles.label, { marginTop: Spacing.md }]}>Raça *</Text>
        <TextInput style={styles.input} value={breed} onChangeText={setBreed} placeholder="Ex: Golden Retriever" placeholderTextColor={Colors.textMuted} />

        <View style={styles.row}>
          <View style={{ flex: 1 }}>
            <Text style={[styles.label, { marginTop: Spacing.md }]}>Peso (kg)</Text>
            <TextInput style={styles.input} value={weight} onChangeText={setWeight} placeholder="Ex: 4.5" placeholderTextColor={Colors.textMuted} keyboardType="decimal-pad" />
          </View>
          <View style={{ flex: 1 }}>
            <Text style={[styles.label, { marginTop: Spacing.md }]}>Nascimento</Text>
            <TextInput style={styles.input} value={birthDate} onChangeText={setBirthDate} placeholder="AAAA-MM-DD" placeholderTextColor={Colors.textMuted} />
          </View>
        </View>

        <Text style={[styles.label, { marginTop: Spacing.md }]}>Observações</Text>
        <TextInput
          style={[styles.input, styles.textarea]}
          value={notes}
          onChangeText={setNotes}
          placeholder="Alergias, comportamento..."
          placeholderTextColor={Colors.textMuted}
          multiline numberOfLines={3}
        />

        <GoldButton
          label={isEditing ? 'Salvar alterações' : 'Cadastrar pet'}
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
  speciesRow: { flexDirection: 'row', gap: Spacing.sm },
  speciesBtn: {
    flex: 1, alignItems: 'center', paddingVertical: Spacing.md,
    borderRadius: Radius.md, borderWidth: 1.5, borderColor: Colors.border,
    backgroundColor: Colors.surface, gap: 4,
  },
  speciesBtnActive: { borderColor: Colors.primary, backgroundColor: Colors.primaryContainer },
  speciesEmoji: { fontSize: 24 },
  speciesLabel: { ...Typography.bodySmall, color: Colors.textSecondary },
  speciesLabelActive: { color: Colors.primary, fontWeight: '600' },
});
