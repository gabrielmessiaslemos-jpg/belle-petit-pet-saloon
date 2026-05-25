import { useState, useEffect } from 'react';
import {
  collection, query, where, orderBy, onSnapshot,
  addDoc, updateDoc, deleteDoc, doc, serverTimestamp,
} from 'firebase/firestore';
import { db } from '../config/firebase';
import { Transaction, MonthlySummary } from '../types';
import { format } from 'date-fns';

export function useFinancial(month?: string) {
  // month = 'YYYY-MM', defaults to current month
  const currentMonth = month || format(new Date(), 'yyyy-MM');
  const startDate = `${currentMonth}-01`;
  const endDate = `${currentMonth}-31`;

  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [summary, setSummary] = useState<MonthlySummary>({
    revenue: 0, expenses: 0, balance: 0, month: currentMonth,
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const q = query(
      collection(db, 'transactions'),
      where('date', '>=', startDate),
      where('date', '<=', endDate),
      orderBy('date', 'desc'),
    );

    const unsubscribe = onSnapshot(q, (snap) => {
      const data = snap.docs.map((d) => ({ id: d.id, ...d.data() } as Transaction));
      setTransactions(data);

      // Calcula resumo
      const revenue = data
        .filter((t) => t.type === 'receita')
        .reduce((sum, t) => sum + t.amount, 0);
      const expenses = data
        .filter((t) => t.type === 'despesa')
        .reduce((sum, t) => sum + t.amount, 0);
      setSummary({ revenue, expenses, balance: revenue - expenses, month: currentMonth });
      setLoading(false);
    });
    return unsubscribe;
  }, [currentMonth]);

  async function addTransaction(data: Omit<Transaction, 'id' | 'createdAt'>) {
    return addDoc(collection(db, 'transactions'), {
      ...data,
      createdAt: serverTimestamp(),
    });
  }

  async function updateTransaction(id: string, data: Partial<Transaction>) {
    await updateDoc(doc(db, 'transactions', id), data);
  }

  async function deleteTransaction(id: string) {
    await deleteDoc(doc(db, 'transactions', id));
  }

  return { transactions, summary, loading, addTransaction, updateTransaction, deleteTransaction };
}
