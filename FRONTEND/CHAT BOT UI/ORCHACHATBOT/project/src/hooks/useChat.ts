import { useState, useCallback } from 'react';
import { Chat, Message, AppState, AIAgent } from '../types';
import { AI_AGENTS } from '../constants/agents';
import { orchestrateAPI, OrchestrateResponse } from '../services/orchestrateAPI';

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
    
    // Don't add any messages automatically - let sendMessage handle the backend call
    if (initialPrompt) {
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
  const sendMessage = useCallback(async (content: string) => {
    if (!appState.currentChat) return;

    const userMessage: Message = {
      id: generateId(),
      content,
      type: 'user',
      timestamp: new Date()
    };

    // Add user message immediately
    setAppState(prev => {
      const isFirstMessage = prev.currentChat && prev.currentChat.messages.length === 0;
      const updatedCurrentChat = {
        ...prev.currentChat!,
        title: isFirstMessage ? content.slice(0, 50) + (content.length > 50 ? '...' : '') : prev.currentChat!.title,
        messages: [...prev.currentChat!.messages, userMessage]
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

    // Add loading message
    const loadingMessage: Message = {
      id: generateId(),
      content: '🤖 Routing to the best model and generating response...',
      type: 'assistant',
      timestamp: new Date()
    };

    setAppState(prev => {
      const updatedCurrentChat = {
        ...prev.currentChat!,
        messages: [...prev.currentChat!.messages, loadingMessage]
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

    try {
      // Call the backend API
      const response: OrchestrateResponse = await orchestrateAPI.orchestrateQuery(content);
      
      // Create response message with model info and critiques
      let responseContent = `**✅ ${response.primary_response.model_name}** responded:\n\n`;
      responseContent += response.primary_response.response_text;
      
      if (response.critiques && response.critiques.length > 0) {
        responseContent += '\n\n**🔍 Model Critiques:**\n';
        response.critiques.forEach(critique => {
          responseContent += `• **${critique.model_name}**: ${critique.critique_text}\n`;
        });
      }
      
      responseContent += `\n\n💰 **Cost**: $${response.total_cost.toFixed(4)} | ⚡ **Latency**: ${response.primary_response.latency_ms}ms | 🎯 **Success Rate**: ${response.success_rate.toFixed(1)}%`;

      const assistantMessage: Message = {
        id: generateId(),
        content: responseContent,
        type: 'assistant',
        timestamp: new Date()
      };

      // Replace loading message with actual response
      setAppState(prev => {
        const updatedMessages = prev.currentChat!.messages.slice(0, -1); // Remove loading message
        const updatedCurrentChat = {
          ...prev.currentChat!,
          messages: [...updatedMessages, assistantMessage]
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

    } catch (error) {
      console.error('Failed to get response from backend:', error);
      
      // Show error message
      const errorMessage: Message = {
        id: generateId(),
        content: '❌ **Connection Error**: Unable to connect to OrchestrateX backend. Please make sure the backend server is running on localhost:8000.\n\n**To start the backend:**\n```\ncd E:\\Projects\\OrchestrateX\npython api_server.py\n```',
        type: 'assistant',
        timestamp: new Date()
      };

      setAppState(prev => {
        const updatedMessages = prev.currentChat!.messages.slice(0, -1); // Remove loading message
        const updatedCurrentChat = {
          ...prev.currentChat!,
          messages: [...updatedMessages, errorMessage]
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
    }
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

  const handleInitialPrompt = useCallback(async (prompt: string) => {
    const newChat = createNewChat(); // Create empty chat first
    
    // Switch to the new chat and send the message
    setAppState(prev => ({
      ...prev,
      isInitialState: false,
      currentChat: newChat
    }));
    
    // Use sendMessage to handle the backend integration
    await sendMessage(prompt);
  }, [createNewChat, sendMessage]);

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