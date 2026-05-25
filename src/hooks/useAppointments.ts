import { useState, useEffect } from 'react';
import {
  collection, query, where, orderBy,
  onSnapshot, addDoc, updateDoc, deleteDoc,
  doc, serverTimestamp,
} from 'firebase/firestore';
import { db } from '../config/firebase';
import { Appointment, AppointmentStatus } from '../types';

export function useAppointments(dateFilter?: string) {
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    const ref = collection(db, 'appointments');
    const q = dateFilter
      ? query(ref, where('date', '==', dateFilter), orderBy('time'))
      : query(ref, orderBy('date', 'desc'), orderBy('time', 'desc'));

    const unsubscribe = onSnapshot(
      q,
      (snapshot) => {
        const data = snapshot.docs.map((d) => ({ id: d.id, ...d.data() } as Appointment));
        setAppointments(data);
        setLoading(false);
      },
      (err) => {
        setError(err.message);
        setLoading(false);
      },
    );
    return unsubscribe;
  }, [dateFilter]);

  async function addAppointment(data: Omit<Appointment, 'id' | 'createdAt'>) {
    await addDoc(collection(db, 'appointments'), {
      ...data,
      createdAt: serverTimestamp(),
    });
  }

  async function updateAppointment(id: string, data: Partial<Appointment>) {
    await updateDoc(doc(db, 'appointments', id), data);
  }

  async function updateStatus(id: string, status: AppointmentStatus) {
    await updateDoc(doc(db, 'appointments', id), { status });
  }

  async function deleteAppointment(id: string) {
    await deleteDoc(doc(db, 'appointments', id));
  }

  return { appointments, loading, error, addAppointment, updateAppointment, updateStatus, deleteAppointment };
}

export function useTodayAppointments() {
  const today = new Date().toISOString().split('T')[0];
  return useAppointments(today);
}
