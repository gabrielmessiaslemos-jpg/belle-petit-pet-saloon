import { useState, useEffect } from 'react';
import {
  collection, query, orderBy, onSnapshot,
  addDoc, updateDoc, deleteDoc, doc,
  serverTimestamp, getDocs,
} from 'firebase/firestore';
import { db } from '../config/firebase';
import { Client, Pet } from '../types';

// ─── Clients ─────────────────────────────────────────────────────────────────
export function useClients() {
  const [clients, setClients] = useState<Client[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const q = query(collection(db, 'clients'), orderBy('name'));
    const unsubscribe = onSnapshot(q, (snap) => {
      setClients(snap.docs.map((d) => ({ id: d.id, ...d.data() } as Client)));
      setLoading(false);
    });
    return unsubscribe;
  }, []);

  async function addClient(data: Omit<Client, 'id' | 'createdAt' | 'pets'>) {
    return addDoc(collection(db, 'clients'), {
      ...data,
      createdAt: serverTimestamp(),
    });
  }

  async function updateClient(id: string, data: Partial<Client>) {
    await updateDoc(doc(db, 'clients', id), data);
  }

  async function deleteClient(id: string) {
    await deleteDoc(doc(db, 'clients', id));
  }

  return { clients, loading, addClient, updateClient, deleteClient };
}

// ─── Pets (subcoleção de um cliente) ─────────────────────────────────────────
export function usePets(clientId: string) {
  const [pets, setPets] = useState<Pet[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!clientId) return;
    const q = query(
      collection(db, 'clients', clientId, 'pets'),
      orderBy('name'),
    );
    const unsubscribe = onSnapshot(q, (snap) => {
      setPets(snap.docs.map((d) => ({ id: d.id, ...d.data() } as Pet)));
      setLoading(false);
    });
    return unsubscribe;
  }, [clientId]);

  async function addPet(data: Omit<Pet, 'id' | 'createdAt'>) {
    return addDoc(collection(db, 'clients', clientId, 'pets'), {
      ...data,
      createdAt: serverTimestamp(),
    });
  }

  async function updatePet(petId: string, data: Partial<Pet>) {
    await updateDoc(doc(db, 'clients', clientId, 'pets', petId), data);
  }

  async function deletePet(petId: string) {
    await deleteDoc(doc(db, 'clients', clientId, 'pets', petId));
  }

  return { pets, loading, addPet, updatePet, deletePet };
}
