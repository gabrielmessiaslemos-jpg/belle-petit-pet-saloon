// ─── Authentication ───────────────────────────────────────────────────────────
export interface AdminUser {
  uid: string;
  email: string;
  displayName?: string;
}

// ─── Pet & Client ─────────────────────────────────────────────────────────────
export type PetSpecies = 'Cachorro' | 'Gato' | 'Outro';

export interface Pet {
  id: string;
  clientId: string;
  name: string;
  species: PetSpecies;
  breed: string;
  weight?: number;       // kg
  birthDate?: string;    // ISO date string
  notes?: string;
  photoUrl?: string;
  createdAt: string;
}

export interface Client {
  id: string;
  name: string;
  phone: string;
  email?: string;
  address?: string;
  notes?: string;
  createdAt: string;
  // Populated client-side
  pets?: Pet[];
  lastVisit?: string;
}

// ─── Services ────────────────────────────────────────────────────────────────
export type ServiceCategory =
  | 'Banho'
  | 'Tosa'
  | 'Banho + Tosa'
  | 'Consulta'
  | 'Hotel'
  | 'Outros';

export interface Service {
  id: string;
  name: string;
  category: ServiceCategory;
  price: number;
  durationMinutes: number;
  description?: string;
  active: boolean;
}

// ─── Appointments ────────────────────────────────────────────────────────────
export type AppointmentStatus =
  | 'pendente'
  | 'confirmado'
  | 'em_andamento'
  | 'concluido'
  | 'cancelado';

export interface Appointment {
  id: string;
  clientId: string;
  clientName: string;    // denormalizado para facilitar listagem
  petId: string;
  petName: string;       // denormalizado
  serviceId: string;
  serviceName: string;   // denormalizado
  date: string;          // 'YYYY-MM-DD'
  time: string;          // 'HH:mm'
  status: AppointmentStatus;
  price: number;
  notes?: string;
  createdAt: string;
}

// ─── Financial ───────────────────────────────────────────────────────────────
export type TransactionType = 'receita' | 'despesa';

export type TransactionCategory =
  | 'Serviço'
  | 'Produto'
  | 'Aluguel'
  | 'Salário'
  | 'Material'
  | 'Conta'
  | 'Outros';

export interface Transaction {
  id: string;
  type: TransactionType;
  amount: number;
  description: string;
  category: TransactionCategory;
  date: string;          // 'YYYY-MM-DD'
  appointmentId?: string; // link com agendamento, se aplicável
  createdAt: string;
}

export interface MonthlySummary {
  revenue: number;
  expenses: number;
  balance: number;
  month: string; // 'YYYY-MM'
}

// ─── Navigation Param Lists ───────────────────────────────────────────────────
export type AuthStackParamList = {
  Login: undefined;
};

export type AppTabParamList = {
  Dashboard: undefined;
  Appointments: undefined;
  Clients: undefined;
  Financial: undefined;
  Services: undefined;
};

export type AppointmentStackParamList = {
  AppointmentsList: undefined;
  NewAppointment: { appointmentId?: string };
  AppointmentDetail: { appointmentId: string };
};

export type ClientStackParamList = {
  ClientsList: undefined;
  NewClient: { clientId?: string };
  ClientDetail: { clientId: string };
  NewPet: { clientId: string; petId?: string };
  PetDetail: { clientId: string; petId: string };
};

export type ServiceStackParamList = {
  ServicesList: undefined;
  NewService: { serviceId?: string };
};

export type FinancialStackParamList = {
  FinancialOverview: undefined;
  NewTransaction: { transactionId?: string };
};
