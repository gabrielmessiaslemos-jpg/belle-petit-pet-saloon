import { useState, useEffect } from 'react';
import {
  collection, query, orderBy, where, onSnapshot,
  addDoc, updateDoc, deleteDoc, doc, serverTimestamp,
} from 'firebase/firestore';
import { db } from '../config/firebase';
import { Service } from '../types';

export function useServices(onlyActive = false) {
  const [services, setServices] = useState<Service[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const ref = collection(db, 'services');
    const q = onlyActive
      ? query(ref, where('active', '==', true), orderBy('name'))
      : query(ref, orderBy('name'));

    const unsubscribe = onSnapshot(q, (snap) => {
      setServices(snap.docs.map((d) => ({ id: d.id, ...d.data() } as Service)));
      setLoading(false);
    });
    return unsubscribe;
  }, [onlyActive]);

  async function addService(data: Omit<Service, 'id'>) {
    return addDoc(collection(db, 'services'), data);
  }

  async function updateService(id: string, data: Partial<Service>) {
    await updateDoc(doc(db, 'services', id), data);
  }

  async function toggleActive(id: string, active: boolean) {
    await updateDoc(doc(db, 'services', id), { active });
  }

  async function deleteService(id: string) {
    await deleteDoc(doc(db, 'services', id));
  }

  return { services, loading, addService, updateService, toggleActive, deleteService };
}
