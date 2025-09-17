import React from 'react';
import { motion } from 'framer-motion';
import { Plus, MessageSquare, Edit, Trash2, Castle } from 'lucide-react';
import { Chat } from '../types';

interface SidebarProps {
  chats: Chat[];
  currentChat: Chat | null;
  onNewChat: () => void;
  onSelectChat: (chat: Chat) => void;
  onDeleteChat: (chatId: string) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  chats,
  currentChat,
  onNewChat,
  onSelectChat,
  onDeleteChat
}) => {
  return (
    <aside className="sidebar group fixed top-0 left-0 bottom-0 bg-slate-900/50 backdrop-blur-xl border-r border-slate-700/50 overflow-hidden flex-shrink-0 z-50 w-20 hover:w-64 transition-all duration-300 ease-in-out"
    >
      <div className="p-4 h-full flex flex-col">
        {/* Logo */}
        <a 
          href="https://orchestratex-84388526388.us-central1.run.app"
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center gap-3 mb-6 overflow-hidden cursor-pointer hover:opacity-80 transition-opacity"
        >
          <img 
            src="/finallogo.png" 
            alt="OrchestrateX Logo" 
            className="w-12 h-12 object-contain flex-shrink-0"
          />
          <span className="text-white font-semibold text-lg whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity duration-300">OrchestrateX</span>
        </a>

        {/* New Chat Button */}
        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={onNewChat}
          className="w-full bg-gradient-to-r from-purple-500 to-cyan-500 text-white rounded-lg p-3 mb-3 flex items-center justify-center gap-2 font-medium hover:shadow-lg hover:shadow-purple-500/25 transition-shadow overflow-hidden"
        >
          <Plus size={20} className="flex-shrink-0" />
          <span className="whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity duration-300">New Chat</span>
        </motion.button>

        {/* Enter Infinity Castle Button */}
        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={() => {
            // Play sound effect
            const audio = new Audio('/infinity-castle-sound.mp3');
            audio.volume = 0.5;
            audio.play().catch(e => console.log('Audio play failed:', e));
            // Navigate to Infinity Castle - increased delay to let audio finish
            setTimeout(() => {
              window.location.href = 'http://localhost:8001';
            }, 2000);
          }}
          className="w-full bg-gradient-to-r from-amber-500 via-orange-500 to-red-600 text-white rounded-lg p-3 mb-6 flex items-center justify-center gap-2 font-medium hover:shadow-lg hover:shadow-amber-500/25 transition-shadow overflow-hidden"
        >
          <Castle size={18} className="flex-shrink-0" />
          <span className="whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity duration-300">Infinity Castle</span>
        </motion.button>

        {/* Chat History */}
        <div className="flex-1 overflow-y-auto custom-scrollbar">
          <div className="text-slate-400 text-sm font-medium mb-3 flex items-center gap-2 overflow-hidden">
            <MessageSquare size={16} className="flex-shrink-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
            <span className="whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity duration-300">Recent</span>
          </div>
          
          {chats.length === 0 ? (
            <p className="text-slate-500 text-sm opacity-0 group-hover:opacity-100 transition-opacity duration-300">No recent chats</p>
          ) : (
            <div className="space-y-2">
              {chats.map((chat) => (
                <motion.div
                  key={chat.id}
                  whileHover={{ scale: 1.02 }}
                  className={`group relative p-3 rounded-lg cursor-pointer transition-colors ${
                    currentChat?.id === chat.id
                      ? 'bg-slate-700/50 border border-purple-500/30'
                      : 'bg-slate-800/30 hover:bg-slate-700/30'
                  }`}
                  onClick={() => onSelectChat(chat)}
                >
                  <div className="flex items-center justify-between overflow-hidden">
                    <div className="flex items-center gap-2 flex-1 min-w-0">
                      <MessageSquare size={16} className="text-slate-400 flex-shrink-0 group-hover:opacity-0 transition-opacity duration-300" />
                      <div className="opacity-0 group-hover:opacity-100 transition-opacity duration-300 min-w-0 flex-1">
                        <p className="text-white text-sm font-medium truncate">
                          {chat.title}
                        </p>
                        <p className="text-slate-400 text-xs">
                          {chat.createdAt.toLocaleDateString()}
                        </p>
                      </div>
                    </div>
                    <div className="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                      <button className="p-1 hover:bg-slate-600 rounded">
                        <Edit size={12} className="text-slate-400" />
                      </button>
                      <button 
                        onClick={(e) => {
                          e.stopPropagation();
                          onDeleteChat(chat.id);
                        }}
                        className="p-1 hover:bg-red-500/20 rounded"
                      >
                        <Trash2 size={12} className="text-red-400" />
                      </button>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          )}
        </div>
      </div>
    </aside>
  );
};