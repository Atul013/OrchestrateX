import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Header } from './components/Header';
import { Sidebar } from './components/Sidebar';
import { InitialPrompt } from './components/InitialPrompt';
import { ConversationView } from './components/ConversationView';
import { Footer } from './components/Footer';
import { useChat } from './hooks/useChat';

function App() {
  const {
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
  } = useChat();

  return (
    <div className={`app h-screen infinity-castle-bg flex flex-col overflow-hidden ${appState.isSent ? 'is-sent' : ''}`}>
      {/* Infinity Castle Video Background */}
      <div className="absolute inset-0 overflow-hidden">
        <video 
          autoPlay 
          loop 
          muted 
          playsInline
          className="absolute inset-0 w-full h-full object-cover opacity-85"
          style={{ filter: 'hue-rotate(20deg) saturate(1.2)' }}
        >
          <source src="/infinity-castle-bg.mp4" type="video/mp4" />
          {/* Fallback gradient if video fails to load */}
        </video>
        {/* Updated overlay gradient with new color scheme */}
        <div className="absolute inset-0 bg-gradient-to-b from-amber-900/30 via-orange-900/40 to-red-950/60" />
      </div>

      <Header 
        isInitialState={appState.isInitialState}
      />

      <div className="flex-1 flex overflow-hidden">
        <Sidebar
          chats={appState.chats}
          currentChat={appState.currentChat}
          onNewChat={startNewChat}
          onSelectChat={selectChat}
          onDeleteChat={deleteChat}
        />

        <main className="flex-1 flex flex-col relative ml-16">
          <AnimatePresence mode="wait">
            {appState.isInitialState ? (
              <motion.div
                key="initial"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                transition={{ duration: 0.3 }}
                className="flex-1 flex flex-col"
              >
                <InitialPrompt onSubmitPrompt={handleInitialPrompt} />
                <Footer />
              </motion.div>
            ) : (
              <motion.div
                key="conversation"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                transition={{ duration: 0.3 }}
                className="flex-1 flex flex-col"
              >
                {/* Always show ConversationView for currentChat, even if empty */}
                {appState.currentChat ? (
                  <ConversationView
                    currentChat={appState.currentChat}
                    agents={appState.agentRecommendations}
                    onSendMessage={sendMessage}
                    onSelectAgent={selectAgent}
                    onRefineMessage={refineMessage}
                  />
                ) : (
                  <div className="flex-1 flex items-center justify-center text-slate-400 select-none">
                    <div className="flex flex-col items-center">
                      <span className="text-3xl md:text-4xl mb-4">💬</span>
                      <p className="text-lg md:text-xl font-medium">Select a chat or start a new one.</p>
                    </div>
                  </div>
                )}
              </motion.div>
            )}
          </AnimatePresence>
        </main>
      </div>
    </div>
  );
}

export default App;