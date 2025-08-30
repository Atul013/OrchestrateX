import React from 'react';
import { motion } from 'framer-motion';
import { Plus, MessageSquare, Edit, Trash2 } from 'lucide-react';
import { Chat } from '../types';

interface SidebarProps {
  isOpen: boolean;
  chats: Chat[];
  currentChat: Chat | null;
  onNewChat: () => void;
  onSelectChat: (chat: Chat) => void;
  onDeleteChat: (chatId: string) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  isOpen,
  chats,
  currentChat,
  onNewChat,
  onSelectChat,
  onDeleteChat
}) => {
  return (
    <motion.aside
      initial={false}
      animate={{
        width: isOpen ? 280 : 0,
        opacity: isOpen ? 1 : 0
      }}
      transition={{ duration: 0.3, ease: "easeInOut" }}
      className="bg-slate-900/50 backdrop-blur-xl border-r border-slate-700/50 overflow-hidden flex-shrink-0 h-screen sticky top-0"
    >
      <div className="p-4 h-full flex flex-col">
        {/* Logo */}
        <div className="flex items-center gap-3 mb-6">
          <div className="w-8 h-8 bg-gradient-to-br from-purple-500 to-cyan-500 rounded-lg flex items-center justify-center">
            <span className="text-white font-bold text-sm">OX</span>
          </div>
          <span className="text-white font-semibold text-lg">OrchestrateX</span>
        </div>

        {/* New Chat Button */}
        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={onNewChat}
          className="w-full bg-gradient-to-r from-purple-500 to-cyan-500 text-white rounded-lg p-3 mb-6 flex items-center justify-center gap-2 font-medium hover:shadow-lg hover:shadow-purple-500/25 transition-shadow"
        >
          <Plus size={18} />
          New Chat
        </motion.button>

        {/* Chat History */}
        <div className="flex-1 overflow-y-auto custom-scrollbar">
          <div className="text-slate-400 text-sm font-medium mb-3 flex items-center gap-2">
            <MessageSquare size={16} />
            Recent
          </div>
          
          {chats.length === 0 ? (
            <p className="text-slate-500 text-sm">No recent chats</p>
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
                  <div className="flex items-center justify-between">
                    <div className="flex-1 min-w-0">
                      <p className="text-white text-sm font-medium truncate">
                        {chat.title}
                      </p>
                      <p className="text-slate-400 text-xs">
                        {chat.createdAt.toLocaleDateString()}
                      </p>
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
    </motion.aside>
  );
};