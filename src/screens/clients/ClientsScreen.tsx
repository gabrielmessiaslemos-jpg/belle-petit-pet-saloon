import React, { useState, useMemo } from 'react';
import {
  StyleSheet, View, Text, FlatList, TextInput, TouchableOpacity,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { AppHeader } from '../../components/AppHeader';
import { ClientCard } from '../../components/ClientCard';
import { EmptyState } from '../../components/EmptyState';
import { useClients, usePets } from '../../hooks/useClients';
import { Colors, Spacing, Radius, Typography } from '../../theme';

function ClientRow({ client, onPress }: any) {
  const { pets } = usePets(client.id);
  return <ClientCard client={client} petsCount={pets.length} onPress={onPress} />;
}

export function ClientsScreen({ navigation }: any) {
  const { clients, loading } = useClients();
  const [search, setSearch] = useState('');

  const filtered = useMemo(
    () =>
      clients.filter(
        (c) =>
          c.name.toLowerCase().includes(search.toLowerCase()) ||
          c.phone.includes(search),
      ),
    [clients, search],
  );

  return (
    <View style={styles.container}>
      <AppHeader
        title="Clientes & Pets"
        rightComponent={
          <TouchableOpacity
            style={styles.addBtn}
            onPress={() => navigation.push('NewClient', {})}
          >
            <Ionicons name="add" size={22} color={Colors.primary} />
          </TouchableOpacity>
        }
      />

      {/* Search */}
      <View style={styles.searchRow}>
        <Ionicons name="search-outline" size={18} color={Colors.textSecondary} style={styles.searchIcon} />
        <TextInput
          style={styles.searchInput}
          placeholder="Buscar por nome ou telefone..."
          placeholderTextColor={Colors.textMuted}
          value={search}
          onChangeText={setSearch}
        />
        {search.length > 0 && (
          <TouchableOpacity onPress={() => setSearch('')}>
            <Ionicons name="close-circle" size={18} color={Colors.textMuted} />
          </TouchableOpacity>
        )}
      </View>

      <Text style={styles.countText}>{filtered.length} cliente{filtered.length !== 1 ? 's' : ''}</Text>

      {filtered.length === 0 && !loading ? (
        <EmptyState
          icon="👤"
          title="Nenhum cliente encontrado"
          description={search ? 'Tente outra busca.' : 'Adicione seu primeiro cliente!'}
        />
      ) : (
        <FlatList
          data={filtered}
          keyExtractor={(item) => item.id}
          renderItem={({ item }) => (
            <ClientRow
              client={item}
              onPress={() => navigation.push('ClientDetail', { clientId: item.id })}
            />
          )}
          contentContainerStyle={styles.list}
          showsVerticalScrollIndicator={false}
        />
      )}

      <TouchableOpacity
        style={styles.fab}
        onPress={() => navigation.push('NewClient', {})}
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
  searchRow: {
    flexDirection: 'row', alignItems: 'center',
    backgroundColor: Colors.surface,
    marginHorizontal: Spacing.md, marginTop: Spacing.md,
    borderRadius: Radius.md, borderWidth: 1, borderColor: Colors.border,
    paddingHorizontal: Spacing.md, paddingVertical: 2,
  },
  searchIcon: { marginRight: Spacing.sm },
  searchInput: {
    flex: 1, color: Colors.text, fontSize: 15,
    paddingVertical: 11,
  },
  countText: {
    ...Typography.caption,
    color: Colors.textMuted,
    paddingHorizontal: Spacing.md, marginTop: Spacing.sm,
  },
  list: { paddingBottom: 100 },
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
