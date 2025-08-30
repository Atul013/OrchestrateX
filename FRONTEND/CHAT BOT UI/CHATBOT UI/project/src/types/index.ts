export interface Message {
  id: string;
  content: string;
  sender: 'user' | 'orchestrate';
  timestamp: Date;
}

export interface Chat {
  id: string;
  title: string;
  messages: Message[];
  lastMessage: Date;
  routedModel?: string;
  confidence?: number;
}

export interface AIModel {
  id: string;
  name: string;
  specialty: string;
  description: string;
  color: string;
  icon: string;
  suggestion?: string;
  strengths: string[];
}

export interface AppState {
  currentChat: Chat | null;
  chats: Chat[];
  isConversationMode: boolean;
  selectedModel?: string;
  showModelPanel: boolean;
}