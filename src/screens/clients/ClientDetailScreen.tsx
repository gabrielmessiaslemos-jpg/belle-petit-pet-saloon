import React from 'react';
import {
  StyleSheet, View, Text, ScrollView,
  TouchableOpacity, Alert,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { AppHeader } from '../../components/AppHeader';
import { GoldCard } from '../../components/GoldCard';
import { GoldButton } from '../../components/GoldButton';
import { EmptyState } from '../../components/EmptyState';
import { useClients, usePets } from '../../hooks/useClients';
import { Colors, Spacing, Typography, Radius } from '../../theme';

export function ClientDetailScreen({ navigation, route }: any) {
  const { clientId } = route.params;
  const { clients, deleteClient } = useClients();
  const { pets, deletePet } = usePets(clientId);
  const client = clients.find((c) => c.id === clientId);

  if (!client) {
    return (
      <View style={styles.container}>
        <AppHeader title="Cliente" onBack={() => navigation.goBack()} />
        <View style={styles.center}><Text style={{ color: Colors.textSecondary }}>Cliente não encontrado.</Text></View>
      </View>
    );
  }

  function handleDeleteClient() {
    Alert.alert(
      'Excluir cliente',
      `Excluir ${client!.name}? Todos os pets também serão removidos.`,
      [
        { text: 'Cancelar', style: 'cancel' },
        {
          text: 'Excluir', style: 'destructive',
          onPress: async () => { await deleteClient(clientId); navigation.goBack(); },
        },
      ],
    );
  }

  return (
    <View style={styles.container}>
      <AppHeader
        title={client.name}
        onBack={() => navigation.goBack()}
        rightComponent={
          <TouchableOpacity
            onPress={() => navigation.push('NewClient', { clientId })}
            style={styles.editBtn}
          >
            <Ionicons name="pencil-outline" size={18} color={Colors.primary} />
          </TouchableOpacity>
        }
      />
      <ScrollView contentContainerStyle={styles.content} showsVerticalScrollIndicator={false}>

        {/* Client Info */}
        <GoldCard goldBorder>
          <InfoRow icon="call-outline" label="Telefone" value={client.phone} />
          {client.email ? <InfoRow icon="mail-outline" label="E-mail" value={client.email} /> : null}
          {client.address ? <InfoRow icon="location-outline" label="Endereço" value={client.address} /> : null}
          {client.notes ? <InfoRow icon="document-text-outline" label="Obs." value={client.notes} /> : null}
        </GoldCard>

        {/* Pets */}
        <View style={styles.sectionHeader}>
          <Text style={styles.sectionTitle}>Pets ({pets.length})</Text>
          <TouchableOpacity onPress={() => navigation.push('NewPet', { clientId })}>
            <Text style={styles.addPetBtn}>+ Adicionar pet</Text>
          </TouchableOpacity>
        </View>

        {pets.length === 0 ? (
          <EmptyState icon="🐶" title="Nenhum pet cadastrado" />
        ) : (
          pets.map((pet) => (
            <GoldCard
              key={pet.id}
              onPress={() => navigation.push('PetDetail', { clientId, petId: pet.id })}
              style={styles.petCard}
            >
              <View style={styles.petRow}>
                <View style={styles.petIcon}>
                  <Text style={styles.petEmoji}>{pet.species === 'Gato' ? '🐱' : '🐶'}</Text>
                </View>
                <View style={{ flex: 1 }}>
                  <Text style={styles.petName}>{pet.name}</Text>
                  <Text style={styles.petBreed}>{pet.breed} · {pet.species}</Text>
                  {pet.weight ? <Text style={styles.petBreed}>{pet.weight} kg</Text> : null}
                </View>
                <Ionicons name="chevron-forward" size={18} color={Colors.textMuted} />
              </View>
            </GoldCard>
          ))
        )}

        <GoldButton
          label="Excluir cliente"
          variant="outlined"
          onPress={handleDeleteClient}
          fullWidth
          style={{ marginTop: Spacing.xl, borderColor: Colors.error }}
        />
        <View style={{ height: Spacing.xxl }} />
      </ScrollView>
    </View>
  );
}

function InfoRow({ icon, label, value }: { icon: any; label: string; value: string }) {
  return (
    <View style={infoStyles.row}>
      <Ionicons name={icon} size={15} color={Colors.primary} />
      <View style={{ flex: 1 }}>
        <Text style={infoStyles.label}>{label}</Text>
        <Text style={infoStyles.value}>{value}</Text>
      </View>
    </View>
  );
}

const infoStyles = StyleSheet.create({
  row: { flexDirection: 'row', alignItems: 'flex-start', gap: Spacing.sm, paddingVertical: 4 },
  label: { ...Typography.caption, color: Colors.textMuted },
  value: { ...Typography.body },
});

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.background },
  center: { flex: 1, alignItems: 'center', justifyContent: 'center' },
  editBtn: { padding: 6, backgroundColor: Colors.primaryContainer, borderRadius: Radius.sm },
  content: { padding: Spacing.md, gap: Spacing.sm },
  sectionHeader: {
    flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center',
    marginTop: Spacing.lg,
  },
  sectionTitle: { ...Typography.heading3 },
  addPetBtn: { ...Typography.label, fontSize: 14 },
  petCard: { marginVertical: Spacing.xs },
  petRow: { flexDirection: 'row', alignItems: 'center', gap: Spacing.md },
  petIcon: {
    width: 42, height: 42, borderRadius: Radius.sm,
    backgroundColor: Colors.primaryContainer,
    alignItems: 'center', justifyContent: 'center',
  },
  petEmoji: { fontSize: 22 },
  petName: { ...Typography.body, fontWeight: '600' },
  petBreed: { ...Typography.bodySmall, color: Colors.textSecondary },
});
