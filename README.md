# 🐾 Belle Petit Pet Saloon — App Administrativo

> App mobile exclusivo para gestão interna da **Belle Petit Pet Saloon**.  
> Desenvolvido com React Native (Expo) + Firebase.

---

## 📱 Funcionalidades

| Módulo | Funcionalidades |
|--------|----------------|
| **Dashboard** | Visão geral do dia, agendamentos, receita, ações rápidas |
| **Agenda** | Agendamentos por dia, criar/editar/cancelar, mudar status |
| **Clientes & Pets** | Cadastro de tutores e seus animais, histórico |
| **Financeiro** | Receitas, despesas, saldo mensal, gráfico |
| **Serviços** | Tabela de serviços com preços e duração |

---

## 🚀 Como executar o projeto

### 1. Pré-requisitos

- [Node.js](https://nodejs.org/) (v18+)
- [Expo CLI](https://expo.dev/): `npm install -g expo-cli`
- App **Expo Go** no celular ([iOS](https://apps.apple.com/app/expo-go/id982107779) | [Android](https://play.google.com/store/apps/details?id=host.exp.exponent))
- Conta no [Firebase](https://console.firebase.google.com/)

### 2. Instalar dependências

```bash
cd belle-petit-pet-saloon
npm install
```

### 3. Configurar Firebase

1. Acesse [console.firebase.google.com](https://console.firebase.google.com/)
2. Clique em **"Adicionar projeto"** → nome: `belle-petit-admin`
3. Vá em **Authentication** → **Sign-in method** → ative **Email/Senha**
4. Crie uma conta admin: Authentication → Users → **Add user**
   - Email: `admin@bellepetit.com.br`
   - Senha: (escolha uma senha segura)
5. Vá em **Firestore Database** → **Criar banco de dados** → modo produção
6. Vá em **Configurações do projeto** → **Seus apps** → adicione um app **Web** (`</>`)
7. Copie as credenciais e preencha o arquivo `.env`:

```bash
cp .env.example .env
# Abra o .env e preencha com seus valores do Firebase
```

```env
EXPO_PUBLIC_FIREBASE_API_KEY=AIzaSy...
EXPO_PUBLIC_FIREBASE_AUTH_DOMAIN=belle-petit-admin.firebaseapp.com
EXPO_PUBLIC_FIREBASE_PROJECT_ID=belle-petit-admin
EXPO_PUBLIC_FIREBASE_STORAGE_BUCKET=belle-petit-admin.appspot.com
EXPO_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=123456789
EXPO_PUBLIC_FIREBASE_APP_ID=1:123456789:web:abc123
```

### 4. Regras do Firestore

No console do Firebase → **Firestore** → **Regras**, cole:

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write: if request.auth != null;
    }
  }
}
```

### 5. Executar o app

```bash
npx expo start
```

Escaneie o QR Code com o **Expo Go** no celular.

---

## 🎨 Identidade Visual

| Cor | Hex | Uso |
|-----|-----|-----|
| Preto profundo | `#121212` | Fundo principal |
| Cinza escuro | `#1E1E1E` | Cards e superfícies |
| **Dourado** | `#C9A84C` | Cor primária (brand) |
| Dourado claro | `#E8C97A` | Destaque e ênfase |
| Branco | `#FFFFFF` | Texto principal |
| Cinza | `#9E9E9E` | Texto secundário |

---

## 📂 Estrutura do Projeto

```
src/
├── theme/         # 🎨 Cores, fontes, espaçamentos
├── types/         # 📝 Interfaces TypeScript
├── config/        # 🔥 Configuração Firebase
├── context/       # 🔄 Estado global (Auth)
├── hooks/         # 🎣 Lógica de dados (Firestore)
├── navigation/    # 🗺️ Estrutura de navegação
├── components/    # 🧩 Componentes reutilizáveis
└── screens/       # 📱 Telas do app
    ├── auth/
    ├── dashboard/
    ├── appointments/
    ├── clients/
    ├── financial/
    └── services/
```

---

## 🎓 Guia de Aprendizado (para o estudante de Eng. de Software)

Este app foi construído com tecnologias amplamente usadas no mercado. Aqui está o caminho de aprendizado recomendado:

### 1. Fundamentos (já sendo ensinados na faculdade)
- **JavaScript** — linguagem base de tudo neste projeto
- **TypeScript** — JavaScript com tipos, evita erros e facilita manutenção
  - Veja: [TypeScript em 5 minutos](https://www.typescriptlang.org/docs/handbook/typescript-in-5-minutes.html)

### 2. React (a biblioteca UI)
- Este app usa **React** para construir a interface
- Conceitos essenciais: componentes, props, state (`useState`), efeitos (`useEffect`)
  - Curso gratuito: [react.dev/learn](https://react.dev/learn)

### 3. React Native (React para mobile)
- React Native transforma código JavaScript em apps iOS e Android nativos
- **Expo** facilita o desenvolvimento sem precisar configurar Xcode/Android Studio
  - Docs: [docs.expo.dev](https://docs.expo.dev)
  - Guides: [reactnative.dev](https://reactnative.dev/docs/getting-started)

### 4. Firebase (backend)
- **Firestore** = banco de dados NoSQL em tempo real na nuvem
- **Authentication** = login seguro sem gerenciar senhas manualmente
  - Docs: [firebase.google.com/docs](https://firebase.google.com/docs)

### 5. Padrões usados neste projeto

| Padrão | Arquivo exemplo | O que aprenderá |
|--------|----------------|-----------------|
| Custom Hooks | `src/hooks/useClients.ts` | Reutilizar lógica de dados |
| Context API | `src/context/AuthContext.tsx` | Estado global sem Redux |
| TypeScript Interfaces | `src/types/index.ts` | Tipagem forte |
| Componentes compostos | `src/components/GoldCard.tsx` | Reutilização de UI |
| Stack + Tab Navigation | `src/navigation/` | Arquitetura de navegação |

### 6. Próximos passos após dominar este app
- [ ] Adicionar notificações push (Expo Notifications)
- [ ] Upload de fotos dos pets (Expo Image Picker + Firebase Storage)
- [ ] Exportar relatório em PDF
- [ ] Enviar confirmação de agendamento por WhatsApp
- [ ] Publicar na Play Store / App Store

---

## 🛠️ Tecnologias utilizadas

| Tecnologia | Versão | Para que serve |
|-----------|--------|---------------|
| React Native | 0.76 | Framework mobile cross-platform |
| Expo SDK | 52 | Ferramentas e APIs para React Native |
| TypeScript | 5.3 | Tipagem estática |
| Firebase | 10.x | Backend (auth + banco de dados) |
| React Navigation | 6.x | Navegação entre telas |
| React Native Paper | 5.x | Componentes UI com tema |
| date-fns | 3.x | Manipulação de datas |

---

## 📞 Suporte

Dúvidas ou problemas? Consulte a [documentação do Expo](https://docs.expo.dev) ou abra uma issue no repositório.

---

*Feito com ❤️ para a Belle Petit Pet Saloon*
