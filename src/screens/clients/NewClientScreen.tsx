import React, { useState, useEffect } from 'react';
import {
  StyleSheet, View, Text, TextInput, ScrollView, Alert, Platform,
} from 'react-native';
import { AppHeader } from '../../components/AppHeader';
import { GoldButton } from '../../components/GoldButton';
import { useClients } from '../../hooks/useClients';
import { Colors, Spacing, Radius, Typography } from '../../theme';

export function NewClientScreen({ navigation, route }: any) {
  const { clientId } = route.params || {};
  const isEditing = !!clientId;
  const { clients, addClient, updateClient } = useClients();
  const existing = clients.find((c) => c.id === clientId);

  const [name, setName] = useState('');
  const [phone, setPhone] = useState('');
  const [email, setEmail] = useState('');
  const [address, setAddress] = useState('');
  const [notes, setNotes] = useState('');
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (existing) {
      setName(existing.name);
      setPhone(existing.phone);
      setEmail(existing.email || '');
      setAddress(existing.address || '');
      setNotes(existing.notes || '');
    }
  }, [existing?.id]);

  async function handleSave() {
    if (!name.trim() || !phone.trim()) {
      Alert.alert('Atenção', 'Nome e telefone são obrigatórios.');
      return;
    }
    setSaving(true);
    try {
      const data = { name: name.trim(), phone: phone.trim(), email, address, notes };
      if (isEditing) {
        await updateClient(clientId, data);
      } else {
        await addClient(data);
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
      <AppHeader
        title={isEditing ? 'Editar Cliente' : 'Novo Cliente'}
        onBack={() => navigation.goBack()}
      />
      <ScrollView contentContainerStyle={styles.content} keyboardShouldPersistTaps="handled">
        <Field label="Nome *" value={name} onChangeText={setName} placeholder="Nome completo do tutor" />
        <Field label="Telefone *" value={phone} onChangeText={setPhone} placeholder="(00) 00000-0000" keyboardType="phone-pad" />
        <Field label="E-mail" value={email} onChangeText={setEmail} placeholder="email@exemplo.com" keyboardType="email-address" autoCapitalize="none" />
        <Field label="Endereço" value={address} onChangeText={setAddress} placeholder="Rua, número, bairro" />
        <Field label="Observações" value={notes} onChangeText={setNotes} placeholder="Alergias, preferências..." multiline />

        <GoldButton
          label={isEditing ? 'Salvar alterações' : 'Cadastrar cliente'}
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

function Field({ label, multiline, ...props }: any) {
  return (
    <View style={fieldStyles.wrapper}>
      <Text style={fieldStyles.label}>{label}</Text>
      <TextInput
        style={[fieldStyles.input, multiline && fieldStyles.textarea]}
        placeholderTextColor={Colors.textMuted}
        multiline={multiline}
        numberOfLines={multiline ? 3 : 1}
        {...props}
      />
    </View>
  );
}

const fieldStyles = StyleSheet.create({
  wrapper: { marginBottom: Spacing.md },
  label: { ...Typography.label, marginBottom: 6 },
  input: {
    backgroundColor: Colors.surface, color: Colors.text,
    borderRadius: Radius.md, borderWidth: 1, borderColor: Colors.border,
    paddingHorizontal: Spacing.md,
    paddingVertical: Platform.OS === 'ios' ? 13 : 10, fontSize: 15,
  },
  textarea: { textAlignVertical: 'top', minHeight: 80 },
});

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.background },
  content: { padding: Spacing.md },
});
