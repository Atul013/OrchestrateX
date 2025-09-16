import { useState, useCallback } from 'react';
import { Chat, Message, AppState, AIAgent } from '../types';
import { AI_AGENTS } from '../constants/agents';
import { orchestrateAPI, OrchestrateResponse } from '../services/orchestrateAPI';
import { getModelConfig } from '../utils/logos';

export const useChat = () => {
  const [appState, setAppState] = useState<AppState>({
    isInitialState: true,
    isSidebarOpen: true,
    isSent: false,
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
      isSent: prev.isSent, // Keep existing sent state (don't reset)
      currentChat: newChat,
      chats: [newChat, ...prev.chats]
    }));

    return newChat;
  }, []);

  const startNewChat = useCallback(() => {
    // Log analytics event
    console.log('Analytics: new_chat_started', { 
      timestamp: new Date().toISOString(),
      conversationId: null 
    });
    
    setAppState(prev => ({ 
      ...prev, 
      isInitialState: true, 
      isSent: prev.isSent, // Keep existing sent state (don't reset)
      currentChat: null 
    }));
  }, []);
  const sendMessage = useCallback(async (content: string) => {
    try {
      console.log('🚀 [DEBUG] sendMessage called with content:', content);
      console.log('🚀 [DEBUG] appState.currentChat:', appState.currentChat);
      
      if (!appState.currentChat) {
        console.error('❌ [DEBUG] No currentChat found, returning early');
        return;
      }

      console.log('🚀 [DEBUG] Creating user message...');
      const userMessage: Message = {
        id: generateId(),
        content,
        type: 'user',
        timestamp: new Date()
      };
      console.log('🚀 [DEBUG] User message created:', userMessage);

      // Add user message immediately and set sent state
      console.log('🚀 [DEBUG] Adding user message to state...');
      setAppState(prev => {
        const isFirstMessage = prev.currentChat && prev.currentChat.messages.length === 0;
        const updatedCurrentChat = {
          ...prev.currentChat!,
          title: isFirstMessage ? content.slice(0, 50) + (content.length > 50 ? '...' : '') : prev.currentChat!.title,
          messages: [...prev.currentChat!.messages, userMessage]
        };
        return {
          ...prev,
          isSent: true, // Set sent state when message is sent
          currentChat: updatedCurrentChat,
          chats: prev.chats.map(chat =>
            chat.id === prev.currentChat!.id
              ? updatedCurrentChat
              : chat
          )
        };
      });
      
      console.log('🚀 [DEBUG] User message added to state');

      // Add loading message
      console.log('🚀 [DEBUG] Creating loading message...');
      const loadingMessage: Message = {
        id: generateId(),
        content: '🤖 Routing to the best model and generating response...',
        type: 'assistant',
        timestamp: new Date()
      };
      console.log('🚀 [DEBUG] Loading message created:', loadingMessage);

    console.log('🚀 [DEBUG] Adding loading message to state...');
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
    console.log('🚀 [DEBUG] Loading message added to state');

    // Update loading message to show critique generation progress
    const updateLoadingMessage = (message: string) => {
      console.log('🚀 [DEBUG] Updating loading message:', message);
      setAppState(prev => {
        const messages = [...prev.currentChat!.messages];
        const loadingIndex = messages.findIndex(msg => msg.id === loadingMessage.id);
        if (loadingIndex !== -1) {
          messages[loadingIndex] = { ...messages[loadingIndex], content: message };
        }
        const updatedCurrentChat = { ...prev.currentChat!, messages };
        return {
          ...prev,
          currentChat: updatedCurrentChat,
          chats: prev.chats.map(chat =>
            chat.id === prev.currentChat!.id ? updatedCurrentChat : chat
          )
        };
      });
    };

    // Show progress updates
    console.log('🚀 [DEBUG] About to update loading message...');
    updateLoadingMessage('🎯 Best model selected, generating primary response...');
    
    try {
      console.log('🚀 [DEBUG] About to call orchestrateAPI.orchestrateQuery...');
      // Call the backend API
      const response: OrchestrateResponse = await orchestrateAPI.orchestrateQuery(content);
      console.log('✅ [DEBUG] orchestrateAPI.orchestrateQuery completed successfully:', response);
      
      // Update to show critique generation
      updateLoadingMessage('🔍 Generating critiques from other models...');

      // Immediately show the primary response
      const assistantMessage: Message = {
        id: generateId(),
        content: response.primary_response.response_text,
        type: 'assistant',
        timestamp: new Date(),
        orchestrationResult: response
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
            chat.id === prev.currentChat!.id ? updatedCurrentChat : chat
          )
        };
      });

      // Create recommendations that include ALL 6 models (primary + critiques + failed ones)
      const allModels = ["GLM4.5", "TNG DeepSeek", "MoonshotAI Kimi", "GPT-OSS", "Llama 4 Maverick", "Qwen3"];
      
      // Create final agent recommendations with ALL 6 models
      const finalAgentRecommendations: AIAgent[] = allModels.map((modelName, index) => {
        const modelConfig = getModelConfig(modelName);
        const critique = response.critiques.find(c => c.model_name === modelName);
        const isPrimary = response.primary_response.model_name === modelName;
        
        let detailedSuggestion = "";
        if (isPrimary) {
          detailedSuggestion = "✅ Primary Response Provider";
        } else if (critique) {
          detailedSuggestion = critique.critique_text;
        } else {
          detailedSuggestion = "❌ Model unavailable (rate limit or error)";
        }
        
        return {
          id: `ai-agent-${index}`,
          name: modelName,
          shortDescription: isPrimary ? "Primary Response" : "AI Analysis & Feedback",
          detailedSuggestion: detailedSuggestion,
          color: modelConfig.color,
          gradient: modelConfig.gradient,
          icon: modelConfig.icon,
          specialties: isPrimary ? ["Primary Model", "Response Generation"] : ["AI Analysis", "Response Critique", "Model Feedback"]
        };
      });
      
      // Set the final agent recommendations with all 6 models
      setAppState(prev => ({
        ...prev,
        agentRecommendations: finalAgentRecommendations
      }));

    } catch (error) {
      console.error('❌ [DEBUG] Failed to get response from backend:', error);
      console.error('❌ [DEBUG] Error type:', typeof error);
      console.error('❌ [DEBUG] Error details:', error instanceof Error ? error.message : String(error));
      console.error('❌ [DEBUG] Error stack:', error instanceof Error ? error.stack : 'No stack trace');
      
      // Show error message
      const errorMessage: Message = {
        id: generateId(),
        content: '❌ **Connection Error**: Unable to connect to OrchestrateX backend. Please check your internet connection and try again.\n\n**Features:** Multi-model orchestration, intelligent routing, real-time critiques, and advanced AI analysis.',
        type: 'assistant',
        timestamp: new Date()
      };

      console.log('❌ [DEBUG] Creating error message:', errorMessage);

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
    } catch (outerError) {
      console.error('❌ [DEBUG] CRITICAL ERROR in sendMessage:', outerError);
      console.error('❌ [DEBUG] This is a critical frontend error that crashed the component');
      // Try to recover by showing a simple error
      alert(`Critical error in chat: ${outerError instanceof Error ? outerError.message : String(outerError)}`);
    }
  }, [appState.currentChat]);

  const refineMessage = useCallback(async (messageId: string, refinementRequest: any) => {
    try {
      // For now, just add a placeholder refined message
      // The refinement functionality would need to be implemented in orchestrateAPI
      const refinedMessage: Message = {
        id: generateId(),
        content: "Refinement feature is being developed. This would show an improved response based on the selected critique.",
        type: 'assistant',
        timestamp: new Date(),
        refinementData: {
          originalMessageId: messageId,
          refinementResponse: refinementRequest,
          isRefined: true
        }
      };

      // Add refined message after the original
      setAppState(prev => {
        const messageIndex = prev.currentChat!.messages.findIndex(m => m.id === messageId);
        if (messageIndex === -1) return prev;

        const newMessages = [...prev.currentChat!.messages];
        newMessages.splice(messageIndex + 1, 0, refinedMessage);

        const updatedCurrentChat = {
          ...prev.currentChat!,
          messages: newMessages
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
      console.error('Failed to refine response:', error);
      // Could add error handling here
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
    // Create a new chat with the initial prompt already included
    const newChat = createNewChat(prompt);
    
    // Log analytics event
    console.log('Analytics: new_chat_started', { 
      timestamp: new Date().toISOString(),
      conversationId: newChat.id 
    });
    
    // Set the current chat and immediately process the prompt
    setAppState(prev => ({
      ...prev,
      isInitialState: false,
      currentChat: newChat
    }));
    
    // Now add the user message and process it
    const userMessage: Message = {
      id: generateId(),
      content: prompt,
      type: 'user',
      timestamp: new Date()
    };

    // Update the chat with the user message
    const updatedChat = {
      ...newChat,
      messages: [userMessage]
    };

    setAppState(prev => ({
      ...prev,
      isSent: true, // Set sent state when initial message is sent
      currentChat: updatedChat,
      chats: prev.chats.map(chat =>
        chat.id === newChat.id ? updatedChat : chat
      )
    }));

    // Add loading message
    const loadingMessage: Message = {
      id: generateId(),
      content: '🤖 Routing to the best model and generating response...',
      type: 'assistant',
      timestamp: new Date()
    };

    setAppState(prev => {
      const currentChat = prev.currentChat!;
      const updatedCurrentChat = {
        ...currentChat,
        messages: [...currentChat.messages, loadingMessage]
      };
      return {
        ...prev,
        currentChat: updatedCurrentChat,
        chats: prev.chats.map(chat =>
          chat.id === currentChat.id ? updatedCurrentChat : chat
        )
      };
    });

    // Process the prompt through the backend
    try {
      // Update loading message to show critique generation progress
      const updateLoadingMessage = (message: string) => {
        setAppState(prev => {
          const messages = [...prev.currentChat!.messages];
          const loadingIndex = messages.findIndex(msg => msg.id === loadingMessage.id);
          if (loadingIndex !== -1) {
            messages[loadingIndex] = { ...messages[loadingIndex], content: message };
          }
          const updatedCurrentChat = { ...prev.currentChat!, messages };
          return {
            ...prev,
            currentChat: updatedCurrentChat,
            chats: prev.chats.map(chat =>
              chat.id === prev.currentChat!.id ? updatedCurrentChat : chat
            )
          };
        });
      };

      // Show progress updates
      updateLoadingMessage('🎯 Best model selected, generating primary response...');
      
      // Call the backend API
      const response = await orchestrateAPI.orchestrateQuery(prompt);
      
      // Update to show critique generation
      updateLoadingMessage('🔍 Generating critiques from other models...');
      
      // Create the assistant response
      const assistantMessage: Message = {
        id: generateId(),
        content: response.primary_response.response_text,
        type: 'assistant',
        timestamp: new Date(),
        orchestrationResult: response
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
            chat.id === prev.currentChat!.id ? updatedCurrentChat : chat
          )
        };
      });

      // Progressively show critiques for better UX
      let critiquesProcessed = 0;
      
      for (let i = 0; i < response.critiques.length; i++) {
        await new Promise(resolve => setTimeout(resolve, 200 * i)); // Stagger critique appearance
        
        critiquesProcessed++;
        const aiAgentRecommendations = response.critiques.slice(0, critiquesProcessed).map((critique, index) => {
          const modelConfig = getModelConfig(critique.model_name);
          return {
            id: `ai-agent-${index}`,
            name: critique.model_name,
            shortDescription: "AI Analysis & Feedback",
            detailedSuggestion: critique.critique_text,
            color: modelConfig.color,
            gradient: modelConfig.gradient,
            icon: modelConfig.icon,
            specialties: ["AI Analysis", "Response Critique", "Model Feedback"]
          };
        });
        
        setAppState(prev => ({
          ...prev,
          agentRecommendations: aiAgentRecommendations
        }));
      }

      // Final update with all critiques
      const finalAgentRecommendations = response.critiques.map((critique, index) => {
        const modelConfig = getModelConfig(critique.model_name);
        return {
          id: `ai-agent-${index}`,
          name: critique.model_name,
          shortDescription: "AI Analysis & Feedback", 
          detailedSuggestion: critique.critique_text,
          color: modelConfig.color,
          gradient: modelConfig.gradient,
          icon: modelConfig.icon,
          specialties: ["AI Analysis", "Response Critique", "Model Feedback"]
        };
      });
      
      setAppState(prev => ({
        ...prev,
        agentRecommendations: finalAgentRecommendations.length > 0 ? finalAgentRecommendations : prev.agentRecommendations
      }));

    } catch (error) {
      console.error('Failed to get response from backend:', error);
      
      // Show error message
      const errorMessage: Message = {
        id: generateId(),
        content: '❌ **Connection Error**: Unable to connect to OrchestrateX backend. Please check your internet connection and try again.\n\n**Features:** Multi-model orchestration, intelligent routing, real-time critiques, and advanced AI analysis.',
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
            chat.id === prev.currentChat!.id ? updatedCurrentChat : chat
          )
        };
      });
    }
  }, [createNewChat, generateId]);

  const selectAgent = useCallback(async (agent: AIAgent) => {
    console.log('Selected agent:', agent.name);
    
    // Store a reference to get the current chat state
    let currentMessages: Message[] = [];
    
    // Add loading message first and capture current state
    setAppState(prev => {
      if (!prev.currentChat) {
        console.log('No current chat available');
        return prev;
      }
      
      currentMessages = prev.currentChat.messages; // Capture current messages
      
      // Add loading message for refinement
      const loadingMessage: Message = {
        id: generateId(),
        content: `🔄 Applying ${agent.name} suggestion: "${agent.detailedSuggestion}"\n\nGenerating improved response...`,
        type: 'assistant',
        timestamp: new Date()
      };

      const updatedCurrentChat = {
        ...prev.currentChat,
        messages: [...prev.currentChat.messages, loadingMessage]
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

    // Check if we have enough messages to work with
    if (currentMessages.length < 2) {
      console.log('Insufficient messages for refinement');
      return;
    }
    
    // Find the most recent user message
    const userMessages = currentMessages.filter((m: Message) => m.type === 'user');
    const lastUserMessage = userMessages[userMessages.length - 1];
    
    if (!lastUserMessage) {
      console.log('No user message found');
      return;
    }

    try {
      // Generate a refined response using the critique as guidance
      const refinedPrompt = `Based on this feedback: "${agent.detailedSuggestion}", please provide an improved and more comprehensive response to: "${lastUserMessage.content}"`;
      
      const response = await orchestrateAPI.orchestrateQuery(refinedPrompt);
      
      // Create refined response message
      const refinedMessage: Message = {
        id: generateId(),
        content: response.primary_response.response_text,
        type: 'assistant',
        timestamp: new Date(),
        orchestrationResult: response,
        refinementData: {
          originalMessageId: lastUserMessage.id,
          appliedSuggestion: agent.detailedSuggestion,
          isRefined: true
        }
      };

      // Replace loading message with refined response
      setAppState(prev => {
        if (!prev.currentChat) return prev;
        
        const updatedMessages = prev.currentChat.messages.slice(0, -1); // Remove loading message
        const updatedCurrentChat = {
          ...prev.currentChat,
          messages: [...updatedMessages, refinedMessage]
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
      console.error('Failed to refine response:', error);
      
      // Show error message
      setAppState(prev => {
        if (!prev.currentChat) return prev;
        
        const errorMessage: Message = {
          id: generateId(),
          content: `❌ Failed to generate refined response. Applied suggestion was: "${agent.detailedSuggestion}"`,
          type: 'assistant',
          timestamp: new Date()
        };

        const updatedMessages = prev.currentChat.messages.slice(0, -1); // Remove loading message
        const updatedCurrentChat = {
          ...prev.currentChat,
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
    selectAgent,
    refineMessage
  };
};