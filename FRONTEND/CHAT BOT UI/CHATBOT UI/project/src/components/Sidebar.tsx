import React from 'react';
import { motion } from 'framer-motion';
import { Plus, Sparkles, MessageCircle, Edit2, Trash2 } from 'lucide-react';
import { Chat } from '../types';

interface SidebarProps {
  chats: Chat[];
  currentChatId?: string;
  onNewChat: () => void;
  onSelectChat: (chatId: string) => void;
  onDeleteChat?: (chatId: string) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  chats,
  currentChatId,
  onNewChat,
  onSelectChat,
  onDeleteChat
}) => {
  return (
    <aside className="w-72 bg-slate-900/50 backdrop-blur-md border-r border-white/10 flex flex-col">
      {/* Logo */}
      <div className="p-6 border-b border-white/10">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-purple-500 to-cyan-400 flex items-center justify-center">
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          <h2 className="text-lg font-bold bg-gradient-to-r from-purple-400 to-cyan-400 bg-clip-text text-transparent">
            OrchestrateX
          </h2>
        </div>
      </div>

      {/* New Chat Button */}
      <div className="p-4">
        <motion.button
          onClick={onNewChat}
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          className="w-full flex items-center justify-center space-x-3 px-4 py-3 rounded-full bg-gradient-to-r from-purple-600 to-cyan-500 hover:from-purple-500 hover:to-cyan-400 text-white font-medium transition-all duration-300 shadow-lg hover:shadow-purple-500/20"
        >
          <Plus className="w-5 h-5" />
          <span>New Chat</span>
        </motion.button>
      </div>

      {/* Recent Chats */}
      <div className="flex-1 px-4 pb-4">
        <div className="mb-3">
          <h3 className="text-sm font-medium text-gray-400 mb-2">Recent</h3>
        </div>
        
        <div className="space-y-2">
          {chats.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              <MessageCircle className="w-8 h-8 mx-auto mb-2 opacity-50" />
              <p className="text-sm">No recent chats</p>
            </div>
          ) : (
            chats.map((chat) => (
              <motion.div
                key={chat.id}
                whileHover={{ x: 4 }}
                className={`group relative p-3 rounded-lg cursor-pointer transition-all duration-200 ${
                  currentChatId === chat.id 
                    ? 'bg-white/10 border border-white/20' 
                    : 'hover:bg-white/5'
                }`}
                onClick={() => onSelectChat(chat.id)}
              >
                <div className="flex items-center justify-between">
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-200 truncate">
                      {chat.title}
                    </p>
                    <p className="text-xs text-gray-500">
                      {chat.lastMessage.toLocaleDateString()}
                    </p>
                  </div>
                  
                  <div className="flex opacity-0 group-hover:opacity-100 transition-opacity duration-200 space-x-1 ml-2">
                    <motion.button
                      whileHover={{ scale: 1.1 }}
                      className="p-1 rounded text-gray-400 hover:text-cyan-400"
                    >
                      <Edit2 className="w-3 h-3" />
                    </motion.button>
                    {onDeleteChat && (
                      <motion.button
                        whileHover={{ scale: 1.1 }}
                        onClick={(e) => {
                          e.stopPropagation();
                          onDeleteChat(chat.id);
                        }}
                        className="p-1 rounded text-gray-400 hover:text-red-400"
                      >
                        <Trash2 className="w-3 h-3" />
                      </motion.button>
                    )}
                  </div>
                </div>
              </motion.div>
            ))
          )}
        </div>
      </div>
    </aside>
  );
};