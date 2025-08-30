import { useState, useCallback } from 'react';
import { Chat, Message, AppState } from '../types';

export const useChat = () => {
  const [state, setState] = useState<AppState>({
    currentChat: null,
    chats: [],
    isConversationMode: false,
    showModelPanel: false
  });

  const createNewChat = useCallback(() => {
    setState(prev => ({
      ...prev,
      currentChat: null,
      isConversationMode: false,
      showModelPanel: false
    }));
  }, []);

  const submitPrompt = useCallback((prompt: string) => {
    const chatId = `chat-${Date.now()}`;
    const userMessage: Message = {
      id: `msg-${Date.now()}-user`,
      content: prompt,
      sender: 'user',
      timestamp: new Date()
    };

    const botMessage: Message = {
      id: `msg-${Date.now()}-bot`,
      content: `I understand you're asking: "${prompt}". Let me help you explore this with the right model routing approach. Based on your query, I'd recommend considering GLM-4.5 for complex reasoning or Claude for clear dialogue.`,
      sender: 'orchestrate',
      timestamp: new Date()
    };

    const newChat: Chat = {
      id: chatId,
      title: prompt.slice(0, 50) + (prompt.length > 50 ? '...' : ''),
      messages: [userMessage, botMessage],
      lastMessage: new Date(),
      routedModel: 'LLaMA 3',
      confidence: 82
    };

    setState(prev => ({
      ...prev,
      currentChat: newChat,
      chats: [newChat, ...prev.chats],
      isConversationMode: true,
      showModelPanel: true
    }));
  }, []);

  const continueConversation = useCallback((message: string) => {
    if (!state.currentChat) return;

    const userMessage: Message = {
      id: `msg-${Date.now()}-user`,
      content: message,
      sender: 'user',
      timestamp: new Date()
    };

    const botMessage: Message = {
      id: `msg-${Date.now()}-bot`,
      content: `Thank you for continuing the conversation. I'll process this follow-up and route it appropriately based on our previous context.`,
      sender: 'orchestrate',
      timestamp: new Date()
    };

    const updatedChat: Chat = {
      ...state.currentChat,
      messages: [...state.currentChat.messages, userMessage, botMessage],
      lastMessage: new Date()
    };

    setState(prev => ({
      ...prev,
      currentChat: updatedChat,
      chats: prev.chats.map(chat => 
        chat.id === updatedChat.id ? updatedChat : chat
      )
    }));
  }, [state.currentChat]);

  const selectChat = useCallback((chatId: string) => {
    const chat = state.chats.find(c => c.id === chatId);
    if (chat) {
      setState(prev => ({
        ...prev,
        currentChat: chat,
        isConversationMode: true,
        showModelPanel: true
      }));
    }
  }, [state.chats]);

  const deleteChat = useCallback((chatId: string) => {
    setState(prev => {
      const newChats = prev.chats.filter(c => c.id !== chatId);
      const isCurrentChat = prev.currentChat?.id === chatId;
      
      return {
        ...prev,
        chats: newChats,
        currentChat: isCurrentChat ? null : prev.currentChat,
        isConversationMode: isCurrentChat ? false : prev.isConversationMode,
        showModelPanel: isCurrentChat ? false : prev.showModelPanel
      };
    });
  }, []);

  const applyModelSuggestion = useCallback((modelId: string) => {
    console.log(`Applied suggestion from model: ${modelId}`);
    // In a real app, this would trigger a new API call with the selected model
  }, []);

  const toggleModelPanel = useCallback(() => {
    setState(prev => ({
      ...prev,
      showModelPanel: !prev.showModelPanel
    }));
  }, []);

  return {
    ...state,
    createNewChat,
    submitPrompt,
    continueConversation,
    selectChat,
    deleteChat,
    applyModelSuggestion,
    toggleModelPanel
  };
};