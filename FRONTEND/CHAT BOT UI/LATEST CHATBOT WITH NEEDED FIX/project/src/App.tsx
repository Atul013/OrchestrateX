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
    sendMessage,
    selectChat,
    deleteChat,
    toggleSidebar,
    handleInitialPrompt,
    selectAgent
  } = useChat();

  return (
    <div className="h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 flex flex-col overflow-hidden">
      {/* Background Effects */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-purple-900/20 via-transparent to-cyan-900/20 pointer-events-none" />
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_bottom_left,_var(--tw-gradient-stops))] from-pink-900/20 via-transparent to-blue-900/20 pointer-events-none" />
      
      <Header 
        onToggleSidebar={toggleSidebar}
        isSidebarOpen={appState.isSidebarOpen}
        isInitialState={appState.isInitialState}
      />
      
      <div className="flex-1 flex overflow-hidden">
        <Sidebar
          isOpen={appState.isSidebarOpen}
          chats={appState.chats}
          currentChat={appState.currentChat}
          onNewChat={createNewChat}
          onSelectChat={selectChat}
          onDeleteChat={deleteChat}
        />
        
        <main className="flex-1 flex flex-col relative">
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
                {appState.currentChat && (
                  <ConversationView
                    currentChat={appState.currentChat}
                    agents={appState.agentRecommendations}
                    onSendMessage={sendMessage}
                    onSelectAgent={selectAgent}
                  />
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