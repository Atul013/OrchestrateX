import { useState, useCallback } from 'react';
import { Chat, Message, AppState, AIAgent } from '../types';
import { AI_AGENTS } from '../constants/agents';

export const useChat = () => {
  const [appState, setAppState] = useState<AppState>({
    isInitialState: true,
    isSidebarOpen: true,
    currentChat: null,
    chats: [],
    currentPrompt: '',
    agentRecommendations: AI_AGENTS
  });

  const generateId = () => Math.random().toString(36).substr(2, 9);

  const createNewChat = useCallback((initialPrompt?: string) => {
    const chatId = generateId();
    const now = new Date();
    let messages: Message[] = [];
    let title = 'New Chat';
    
    if (initialPrompt) {
      messages = [
        {
          id: generateId(),
          content: initialPrompt,
          type: 'user',
          timestamp: now
        },
        {
          id: generateId(),
          content: `🚀 **OrchestrateX Response:**\n\nI received your message: "${initialPrompt}"\n\n*This is currently a demo response. The backend integration is being set up to route your query to the best AI model and provide real responses with critiques.*\n\n**Next Steps:**\n- ✅ Frontend UI working\n- 🔧 Backend API integration in progress\n- 🎯 Multi-model orchestration ready`,
          type: 'assistant',
          timestamp: new Date(now.getTime() + 1000)
        }
      ];
      title = initialPrompt.slice(0, 50) + (initialPrompt.length > 50 ? '...' : '');
    }

    const newChat: Chat = {
      id: chatId,
      title,
      messages,
      createdAt: now
    };

    setAppState(prev => ({
      ...prev,
      isInitialState: false,
      currentChat: newChat,
      chats: [newChat, ...prev.chats]
    }));

    return newChat;
  }, []);

  const startNewChat = useCallback(() => {
    setAppState(prev => ({ 
      ...prev, 
      isInitialState: true, 
      currentChat: null 
    }));
  }, []);

  const sendMessage = useCallback((content: string) => {
    if (!appState.currentChat) return;

    const userMessage: Message = {
      id: generateId(),
      content,
      type: 'user',
      timestamp: new Date()
    };

    const assistantMessage: Message = {
      id: generateId(),
      content: `🤖 **Demo Response:**\n\nThank you for: "${content}"\n\n*This is a demo response. The full backend integration with multi-model orchestration is ready to be activated. It will route your query to the best AI model (GPT-OSS, TNG DeepSeek, GLM4.5, etc.) and provide real responses with model critiques.*\n\n💡 **When activated, you'll see:**\n- Smart model selection\n- Real AI responses  \n- Ultra-short critiques for UI tooltips\n- Cost & performance metrics`,
      type: 'assistant',
      timestamp: new Date(Date.now() + 1000)
    };

    setAppState(prev => {
      const isFirstMessage = prev.currentChat && prev.currentChat.messages.length === 0;
      const updatedCurrentChat = {
        ...prev.currentChat!,
        title: isFirstMessage ? content.slice(0, 50) + (content.length > 50 ? '...' : '') : prev.currentChat!.title,
        messages: [...prev.currentChat!.messages, userMessage, assistantMessage]
      };
      return {
        ...prev,
        currentChat: updatedCurrentChat,
        chats: prev.chats.map(chat =>
          chat.id === prev.currentChat!.id
            ? updatedCurrentChat
            : chat
        )
      };
    });
  }, [appState.currentChat]);

  const selectChat = useCallback((chat: Chat) => {
    setAppState(prev => ({
      ...prev,
      isInitialState: false,
      currentChat: chat
    }));
  }, []);

  const deleteChat = useCallback((chatId: string) => {
    setAppState(prev => ({
      ...prev,
      chats: prev.chats.filter(chat => chat.id !== chatId),
      currentChat: prev.currentChat?.id === chatId ? null : prev.currentChat,
      isInitialState: prev.currentChat?.id === chatId ? true : prev.isInitialState
    }));
  }, []);

  const toggleSidebar = useCallback(() => {
    setAppState(prev => ({
      ...prev,
      isSidebarOpen: !prev.isSidebarOpen
    }));
  }, []);

  const handleInitialPrompt = useCallback((prompt: string) => {
    createNewChat(prompt);
  }, [createNewChat]);

  const selectAgent = useCallback((agent: AIAgent) => {
    console.log('Selected agent:', agent.name);
    // Here you would implement the logic to apply the agent's suggestion
  }, []);

  return {
    appState,
    createNewChat,
    startNewChat,
    sendMessage,
    selectChat,
    deleteChat,
    toggleSidebar,
    handleInitialPrompt,
    selectAgent
  };
};
