export interface Message {
  id: string;
  content: string;
  type: 'user' | 'assistant';
  timestamp: Date;
}

export interface Chat {
  id: string;
  title: string;
  messages: Message[];
  createdAt: Date;
}

export interface AIAgent {
  id: string;
  name: string;
  shortDescription: string;
  detailedSuggestion: string;
  color: string;
  gradient: string;
  icon: string;
  specialties: string[];
}

export interface AppState {
  isInitialState: boolean;
  isSidebarOpen: boolean;
  currentChat: Chat | null;
  chats: Chat[];
  currentPrompt: string;
  agentRecommendations: AIAgent[];
}