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
    
    const messages: Message[] = initialPrompt ? [
      {
        id: generateId(),
        content: initialPrompt,
        type: 'user',
        timestamp: now
      },
      {
        id: generateId(),
        content: `I understand you're asking: "${initialPrompt}". Let me help you explore this with the right model routing approach. Based on your query, I'd recommend considering GLM-4.5 for complex reasoning or Claude for clear dialogue.`,
        type: 'assistant',
        timestamp: new Date(now.getTime() + 1000)
      }
    ] : [];

    const newChat: Chat = {
      id: chatId,
      title: initialPrompt || 'New Chat',
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
      content: `Thank you for your message: "${content}". I'm processing this and will route it to the most appropriate model for the best response.`,
      type: 'assistant',
      timestamp: new Date(Date.now() + 1000)
    };

    setAppState(prev => ({
      ...prev,
      currentChat: {
        ...prev.currentChat!,
        messages: [...prev.currentChat!.messages, userMessage, assistantMessage]
      },
      chats: prev.chats.map(chat => 
        chat.id === prev.currentChat!.id 
          ? { ...chat, messages: [...chat.messages, userMessage, assistantMessage] }
          : chat
      )
    }));
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
    // For now, we'll just add a message indicating the selection
    if (appState.currentChat) {
      const agentMessage: Message = {
        id: generateId(),
        content: `Applied ${agent.name} suggestion: ${agent.detailedSuggestion}`,
        type: 'assistant',
        timestamp: new Date()
      };

      setAppState(prev => ({
        ...prev,
        currentChat: {
          ...prev.currentChat!,
          messages: [...prev.currentChat!.messages, agentMessage]
        },
        chats: prev.chats.map(chat => 
          chat.id === prev.currentChat!.id 
            ? { ...chat, messages: [...chat.messages, agentMessage] }
            : chat
        )
      }));
    }
  }, [appState.currentChat]);

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