import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Header } from './components/Header';
import { Sidebar } from './components/Sidebar';
import { PromptEntry } from './components/PromptEntry';
import { Conversation } from './components/Conversation';
import { ModelRecommendations } from './components/ModelRecommendations';
import { Footer } from './components/Footer';
import { useChat } from './hooks/useChat';

function App() {
  const {
    currentChat,
    chats,
    isConversationMode,
    showModelPanel,
    createNewChat,
    submitPrompt,
    continueConversation,
    selectChat,
    deleteChat,
    applyModelSuggestion,
    toggleModelPanel
  } = useChat();

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white flex flex-col overflow-hidden">
      {/* Animated background elements */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <motion.div
          className="absolute top-1/4 left-1/4 w-96 h-96 bg-purple-600/10 rounded-full blur-3xl"
          animate={{
            scale: [1, 1.2, 1],
            opacity: [0.3, 0.5, 0.3]
          }}
          transition={{
            duration: 8,
            repeat: Infinity,
            ease: "easeInOut"
          }}
        />
        <motion.div
          className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl"
          animate={{
            scale: [1.2, 1, 1.2],
            opacity: [0.5, 0.3, 0.5]
          }}
          transition={{
            duration: 10,
            repeat: Infinity,
            ease: "easeInOut"
          }}
        />
      </div>

      <Header />
      
      <div className="flex flex-1 relative">
        <Sidebar
          chats={chats}
          currentChatId={currentChat?.id}
          onNewChat={createNewChat}
          onSelectChat={selectChat}
          onDeleteChat={deleteChat}
        />
        
        <div className="flex-1 flex flex-col relative">
          <AnimatePresence mode="wait">
            {!isConversationMode ? (
              <motion.div
                key="prompt-entry"
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 1.05 }}
                transition={{ duration: 0.4, ease: "easeInOut" }}
                className="flex-1 flex flex-col"
              >
                <PromptEntry onSubmitPrompt={submitPrompt} />
              </motion.div>
            ) : (
              <motion.div
                key="conversation"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                transition={{ duration: 0.4, ease: "easeInOut" }}
                className="flex-1 flex flex-col"
              >
                <Conversation
                  messages={currentChat?.messages || []}
                  routedModel={currentChat?.routedModel}
                  confidence={currentChat?.confidence}
                  onContinue={continueConversation}
                />
              </motion.div>
            )}
          </AnimatePresence>
          
          <Footer />
        </div>

        {/* Model Recommendations Panel */}
        <ModelRecommendations
          isVisible={showModelPanel && isConversationMode}
          onClose={toggleModelPanel}
          onApplyModel={applyModelSuggestion}
        />
      </div>

      {/* Mobile overlay when model panel is open */}
      <AnimatePresence>
        {showModelPanel && isConversationMode && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/50 backdrop-blur-sm z-40 lg:hidden"
            onClick={toggleModelPanel}
          />
        )}
      </AnimatePresence>
    </div>
  );
}

export default App;