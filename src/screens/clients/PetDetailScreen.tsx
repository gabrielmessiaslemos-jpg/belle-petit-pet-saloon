import React from 'react';
import { StyleSheet, View, Text, ScrollView, TouchableOpacity, Alert } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { format, parseISO, differenceInYears, differenceInMonths } from 'date-fns';
import { ptBR } from 'date-fns/locale';
import { AppHeader } from '../../components/AppHeader';
import { GoldCard } from '../../components/GoldCard';
import { GoldButton } from '../../components/GoldButton';
import { usePets } from '../../hooks/useClients';
import { Colors, Spacing, Typography, Radius } from '../../theme';

function petAge(birthDate?: string) {
  if (!birthDate) return null;
  const birth = parseISO(birthDate);
  const years = differenceInYears(new Date(), birth);
  if (years >= 1) return `${years} ano${years > 1 ? 's' : ''}`;
  const months = differenceInMonths(new Date(), birth);
  return `${months} mês${months !== 1 ? 'es' : ''}`;
}

export function PetDetailScreen({ navigation, route }: any) {
  const { clientId, petId } = route.params;
  const { pets, deletePet } = usePets(clientId);
  const pet = pets.find((p) => p.id === petId);

  if (!pet) {
    return (
      <View style={styles.container}>
        <AppHeader title="Pet" onBack={() => navigation.goBack()} />
        <View style={styles.center}><Text style={{ color: Colors.textSecondary }}>Pet não encontrado.</Text></View>
      </View>
    );
  }

  const age = petAge(pet.birthDate);

  function handleDelete() {
    Alert.alert('Excluir pet', `Excluir ${pet!.name}?`, [
      { text: 'Cancelar', style: 'cancel' },
      {
        text: 'Excluir', style: 'destructive',
        onPress: async () => { await deletePet(petId); navigation.goBack(); },
      },
    ]);
  }

  return (
    <View style={styles.container}>
      <AppHeader
        title={pet.name}
        onBack={() => navigation.goBack()}
        rightComponent={
          <TouchableOpacity
            onPress={() => navigation.push('NewPet', { clientId, petId })}
            style={styles.editBtn}
          >
            <Ionicons name="pencil-outline" size={18} color={Colors.primary} />
          </TouchableOpacity>
        }
      />
      <ScrollView contentContainerStyle={styles.content}>
        <View style={styles.heroRow}>
          <View style={styles.petIcon}>
            <Text style={styles.petEmoji}>{pet.species === 'Gato' ? '🐱' : '🐶'}</Text>
          </View>
          <View>
            <Text style={styles.petName}>{pet.name}</Text>
            <Text style={styles.petMeta}>{pet.species} · {pet.breed}</Text>
          </View>
        </View>

        <GoldCard goldBorder style={styles.infoCard}>
          {pet.weight ? <InfoRow icon="barbell-outline" label="Peso" value={`${pet.weight} kg`} /> : null}
          {age ? <InfoRow icon="calendar-outline" label="Idade" value={age} /> : null}
          {pet.birthDate ? (
            <InfoRow
              icon="gift-outline"
              label="Nascimento"
              value={format(parseISO(pet.birthDate), "dd 'de' MMMM 'de' yyyy", { locale: ptBR })}
            />
          ) : null}
          {pet.notes ? <InfoRow icon="document-text-outline" label="Obs." value={pet.notes} /> : null}
        </GoldCard>

        <GoldButton
          label="Excluir pet"
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

function InfoRow({ icon, label, value }: { icon: any; label: string; value: string }) {
  return (
    <View style={rowStyles.row}>
      <Ionicons name={icon} size={16} color={Colors.primary} />
      <View style={{ flex: 1 }}>
        <Text style={rowStyles.label}>{label}</Text>
        <Text style={rowStyles.value}>{value}</Text>
      </View>
    </View>
  );
}

const rowStyles = StyleSheet.create({
  row: { flexDirection: 'row', gap: Spacing.sm, alignItems: 'flex-start', paddingVertical: 5 },
  label: { ...Typography.caption, color: Colors.textMuted },
  value: { ...Typography.body },
});

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.background },
  center: { flex: 1, alignItems: 'center', justifyContent: 'center' },
  editBtn: { padding: 6, backgroundColor: Colors.primaryContainer, borderRadius: Radius.sm },
  content: { padding: Spacing.md, gap: Spacing.md },
  heroRow: { flexDirection: 'row', alignItems: 'center', gap: Spacing.md },
  petIcon: {
    width: 72, height: 72, borderRadius: 36,
    backgroundColor: Colors.primaryContainer,
    borderWidth: 2, borderColor: Colors.primary,
    alignItems: 'center', justifyContent: 'center',
  },
  petEmoji: { fontSize: 36 },
  petName: { ...Typography.heading2 },
  petMeta: { ...Typography.bodySmall, color: Colors.textSecondary },
  infoCard: { gap: 4 },
});
