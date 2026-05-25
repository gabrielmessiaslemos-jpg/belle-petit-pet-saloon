import React, { useState, useEffect } from 'react';
import {
  StyleSheet, View, Text, TextInput, ScrollView,
  TouchableOpacity, Alert, Platform,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { format } from 'date-fns';
import { AppHeader } from '../../components/AppHeader';
import { GoldButton } from '../../components/GoldButton';
import { GoldCard } from '../../components/GoldCard';
import { useAppointments } from '../../hooks/useAppointments';
import { useClients, usePets } from '../../hooks/useClients';
import { useServices } from '../../hooks/useServices';
import { Colors, Spacing, Typography, Radius } from '../../theme';
import { Client, Pet, Service } from '../../types';

export function NewAppointmentScreen({ navigation, route }: any) {
  const { appointmentId } = route.params || {};
  const isEditing = !!appointmentId;

  const { appointments, addAppointment, updateAppointment } = useAppointments();
  const { clients } = useClients();
  const { services } = useServices(true);

  const existing = appointments.find((a) => a.id === appointmentId);

  const [selectedClient, setSelectedClient] = useState<Client | null>(null);
  const [selectedPet, setSelectedPet] = useState<Pet | null>(null);
  const [selectedService, setSelectedService] = useState<Service | null>(null);
  const [date, setDate] = useState(format(new Date(), 'yyyy-MM-dd'));
  const [time, setTime] = useState('09:00');
  const [notes, setNotes] = useState('');
  const [saving, setSaving] = useState(false);

  const { pets } = usePets(selectedClient?.id || '');

  // Pickers visibility
  const [showClientPicker, setShowClientPicker] = useState(false);
  const [showPetPicker, setShowPetPicker] = useState(false);
  const [showServicePicker, setShowServicePicker] = useState(false);

  useEffect(() => {
    if (existing) {
      const client = clients.find((c) => c.id === existing.clientId);
      setSelectedClient(client || null);
      setDate(existing.date);
      setTime(existing.time);
      setNotes(existing.notes || '');
    }
  }, [existing?.id]);

  async function handleSave() {
    if (!selectedClient || !selectedPet || !selectedService) {
      Alert.alert('Atenção', 'Selecione cliente, pet e serviço.');
      return;
    }
    setSaving(true);
    try {
      const data = {
        clientId: selectedClient.id,
        clientName: selectedClient.name,
        petId: selectedPet.id,
        petName: selectedPet.name,
        serviceId: selectedService.id,
        serviceName: selectedService.name,
        date,
        time,
        status: 'pendente' as const,
        price: selectedService.price,
        notes,
      };
      if (isEditing) {
        await updateAppointment(appointmentId, data);
      } else {
        await addAppointment(data);
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
        title={isEditing ? 'Editar Agendamento' : 'Novo Agendamento'}
        onBack={() => navigation.goBack()}
      />
      <ScrollView contentContainerStyle={styles.content} keyboardShouldPersistTaps="handled">

        {/* Client picker */}
        <Text style={styles.label}>Cliente *</Text>
        <TouchableOpacity style={styles.picker} onPress={() => setShowClientPicker(!showClientPicker)}>
          <Text style={selectedClient ? styles.pickerValue : styles.pickerPlaceholder}>
            {selectedClient?.name || 'Selecionar cliente...'}
          </Text>
          <Ionicons name={showClientPicker ? 'chevron-up' : 'chevron-down'} size={16} color={Colors.textSecondary} />
        </TouchableOpacity>
        {showClientPicker && (
          <GoldCard style={styles.dropdownCard}>
            <ScrollView style={{ maxHeight: 200 }} nestedScrollEnabled>
              {clients.map((c) => (
                <TouchableOpacity
                  key={c.id}
                  style={styles.dropdownItem}
                  onPress={() => { setSelectedClient(c); setSelectedPet(null); setShowClientPicker(false); }}
                >
                  <Text style={styles.dropdownText}>{c.name}</Text>
                  <Text style={styles.dropdownSub}>{c.phone}</Text>
                </TouchableOpacity>
              ))}
            </ScrollView>
          </GoldCard>
        )}

        {/* Pet picker */}
        <Text style={[styles.label, { marginTop: Spacing.md }]}>Pet *</Text>
        <TouchableOpacity
          style={[styles.picker, !selectedClient && styles.pickerDisabled]}
          onPress={() => selectedClient && setShowPetPicker(!showPetPicker)}
          disabled={!selectedClient}
        >
          <Text style={selectedPet ? styles.pickerValue : styles.pickerPlaceholder}>
            {selectedPet?.name || (selectedClient ? 'Selecionar pet...' : 'Selecione o cliente primeiro')}
          </Text>
          <Ionicons name={showPetPicker ? 'chevron-up' : 'chevron-down'} size={16} color={Colors.textSecondary} />
        </TouchableOpacity>
        {showPetPicker && pets.length > 0 && (
          <GoldCard style={styles.dropdownCard}>
            {pets.map((p) => (
              <TouchableOpacity
                key={p.id}
                style={styles.dropdownItem}
                onPress={() => { setSelectedPet(p); setShowPetPicker(false); }}
              >
                <Text style={styles.dropdownText}>{p.name}</Text>
                <Text style={styles.dropdownSub}>{p.breed} · {p.species}</Text>
              </TouchableOpacity>
            ))}
          </GoldCard>
        )}

        {/* Service picker */}
        <Text style={[styles.label, { marginTop: Spacing.md }]}>Serviço *</Text>
        <TouchableOpacity style={styles.picker} onPress={() => setShowServicePicker(!showServicePicker)}>
          <Text style={selectedService ? styles.pickerValue : styles.pickerPlaceholder}>
            {selectedService ? `${selectedService.name} — ${selectedService.price.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}` : 'Selecionar serviço...'}
          </Text>
          <Ionicons name={showServicePicker ? 'chevron-up' : 'chevron-down'} size={16} color={Colors.textSecondary} />
        </TouchableOpacity>
        {showServicePicker && (
          <GoldCard style={styles.dropdownCard}>
            <ScrollView style={{ maxHeight: 200 }} nestedScrollEnabled>
              {services.map((s) => (
                <TouchableOpacity
                  key={s.id}
                  style={styles.dropdownItem}
                  onPress={() => { setSelectedService(s); setShowServicePicker(false); }}
                >
                  <Text style={styles.dropdownText}>{s.name}</Text>
                  <Text style={styles.dropdownSub}>
                    {s.category} · {s.durationMinutes}min · {s.price.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}
                  </Text>
                </TouchableOpacity>
              ))}
            </ScrollView>
          </GoldCard>
        )}

        {/* Date & Time */}
        <View style={styles.dateTimeRow}>
          <View style={{ flex: 1 }}>
            <Text style={styles.label}>Data *</Text>
            <TextInput
              style={styles.input}
              value={date}
              onChangeText={setDate}
              placeholder="AAAA-MM-DD"
              placeholderTextColor={Colors.textMuted}
            />
          </View>
          <View style={{ flex: 1 }}>
            <Text style={styles.label}>Horário *</Text>
            <TextInput
              style={styles.input}
              value={time}
              onChangeText={setTime}
              placeholder="HH:mm"
              placeholderTextColor={Colors.textMuted}
              keyboardType="numbers-and-punctuation"
            />
          </View>
        </View>

        {/* Notes */}
        <Text style={[styles.label, { marginTop: Spacing.md }]}>Observações</Text>
        <TextInput
          style={[styles.input, styles.textarea]}
          value={notes}
          onChangeText={setNotes}
          placeholder="Alergia, comportamento, preferências..."
          placeholderTextColor={Colors.textMuted}
          multiline
          numberOfLines={3}
        />

        <GoldButton
          label={isEditing ? 'Salvar alterações' : 'Criar agendamento'}
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
  picker: {
    flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between',
    backgroundColor: Colors.surface, borderRadius: Radius.md,
    borderWidth: 1, borderColor: Colors.border,
    paddingHorizontal: Spacing.md, paddingVertical: 13,
  },
  pickerDisabled: { opacity: 0.5 },
  pickerValue: { ...Typography.body, flex: 1 },
  pickerPlaceholder: { ...Typography.body, color: Colors.textMuted, flex: 1 },
  dropdownCard: { marginTop: 4, padding: 0, overflow: 'hidden' },
  dropdownItem: {
    paddingHorizontal: Spacing.md, paddingVertical: 10,
    borderBottomWidth: 1, borderBottomColor: Colors.divider,
  },
  dropdownText: { ...Typography.body },
  dropdownSub: { ...Typography.caption, color: Colors.textSecondary, marginTop: 2 },
  dateTimeRow: { flexDirection: 'row', gap: Spacing.md, marginTop: Spacing.md },
  input: {
    backgroundColor: Colors.surface, color: Colors.text,
    borderRadius: Radius.md, borderWidth: 1, borderColor: Colors.border,
    paddingHorizontal: Spacing.md,
    paddingVertical: Platform.OS === 'ios' ? 13 : 10,
    fontSize: 15,
  },
  textarea: { textAlignVertical: 'top', minHeight: 80 },
});
