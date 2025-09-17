export interface Message {
  id: string;
  content: string;
  type: 'user' | 'assistant';
  timestamp: Date;
  orchestrationResult?: any; // Store the full orchestration result
  refinementData?: any; // Store refinement information
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
  isSent: boolean;
  currentChat: Chat | null;
  chats: Chat[];
  currentPrompt: string;
  agentRecommendations: AIAgent[];
}