import React, { useState } from 'react';
import { StyleSheet, View, Text, FlatList, TouchableOpacity } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { AppHeader } from '../../components/AppHeader';
import { ServiceCard } from '../../components/ServiceCard';
import { EmptyState } from '../../components/EmptyState';
import { useServices } from '../../hooks/useServices';
import { Colors, Spacing, Radius, Typography } from '../../theme';
import { ServiceCategory } from '../../types';

const ALL_CATEGORIES = ['Todos', 'Banho', 'Tosa', 'Banho + Tosa', 'Consulta', 'Hotel', 'Outros'];

export function ServicesScreen({ navigation }: any) {
  const { services, loading, toggleActive } = useServices();
  const [activeFilter, setActiveFilter] = useState('Todos');

  const filtered = activeFilter === 'Todos'
    ? services
    : services.filter((s) => s.category === activeFilter);

  return (
    <View style={styles.container}>
      <AppHeader
        title="Serviços & Preços"
        rightComponent={
          <TouchableOpacity
            style={styles.addBtn}
            onPress={() => navigation.push('NewService', {})}
          >
            <Ionicons name="add" size={22} color={Colors.primary} />
          </TouchableOpacity>
        }
      />

      {/* Category filter */}
      <FlatList
        horizontal
        data={ALL_CATEGORIES}
        keyExtractor={(c) => c}
        showsHorizontalScrollIndicator={false}
        contentContainerStyle={styles.filterList}
        renderItem={({ item }) => (
          <TouchableOpacity
            style={[styles.filterChip, activeFilter === item && styles.filterChipActive]}
            onPress={() => setActiveFilter(item)}
          >
            <Text style={[styles.filterLabel, activeFilter === item && styles.filterLabelActive]}>
              {item}
            </Text>
          </TouchableOpacity>
        )}
      />

      <Text style={styles.countText}>{filtered.length} serviço{filtered.length !== 1 ? 's' : ''}</Text>

      {filtered.length === 0 && !loading ? (
        <EmptyState icon="✂️" title="Nenhum serviço encontrado" description="Adicione os serviços da sua petshop!" />
      ) : (
        <FlatList
          data={filtered}
          keyExtractor={(item) => item.id}
          renderItem={({ item }) => (
            <ServiceCard
              service={item}
              onPress={() => navigation.push('NewService', { serviceId: item.id })}
            />
          )}
          contentContainerStyle={styles.list}
          showsVerticalScrollIndicator={false}
        />
      )}

      <TouchableOpacity style={styles.fab} onPress={() => navigation.push('NewService', {})}>
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
  filterList: { paddingHorizontal: Spacing.md, paddingVertical: Spacing.sm, gap: Spacing.sm },
  filterChip: {
    paddingHorizontal: 14, paddingVertical: 7,
    borderRadius: Radius.full,
    borderWidth: 1, borderColor: Colors.border,
    backgroundColor: Colors.surface,
  },
  filterChipActive: { backgroundColor: Colors.primary, borderColor: Colors.primary },
  filterLabel: { fontSize: 13, fontWeight: '500', color: Colors.textSecondary },
  filterLabelActive: { color: Colors.onPrimary, fontWeight: '700' },
  countText: { ...Typography.caption, color: Colors.textMuted, paddingHorizontal: Spacing.md, marginBottom: Spacing.xs },
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
