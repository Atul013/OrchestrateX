import React from 'react';
import { motion } from 'framer-motion';
import { Plus, ArrowLeft } from 'lucide-react';
import { Chat } from '../types';

interface SidebarProps {
  chats: Chat[];
  currentChat: Chat | null;
  onNewChat: () => void;
  onSelectChat: (chat: Chat) => void;
  onDeleteChat: (chatId: string) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  onNewChat
}) => {
  return (
    <aside className="sidebar fixed top-0 left-0 bottom-0 bg-gradient-to-b from-amber-900/40 via-orange-900/30 to-red-950/40 backdrop-blur-xl border-r border-yellow-500/30 overflow-hidden flex-shrink-0 z-50 w-16 transition-all duration-300 ease-in-out"
    >
      <div className="p-3 h-full flex flex-col items-center">
        {/* Minimal New Chat Button */}
        <motion.button
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.95 }}
          onClick={onNewChat}
          className="w-10 h-10 bg-gradient-to-br from-yellow-400 to-orange-500 hover:from-orange-500 hover:to-red-500 text-brown-900 rounded-xl flex items-center justify-center shadow-lg hover:shadow-xl hover:shadow-yellow-500/30 transition-all duration-300 mt-4 infinity-button"
          style={{
            boxShadow: '0 4px 15px rgba(228, 138, 50, 0.4)'
          }}
        >
          <Plus size={20} className="font-bold" />
        </motion.button>

        {/* Exit Infinity Castle Button */}
        <motion.button
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => {
            // Play exit sound effect (reverse/different sound)
            const audio = new Audio('/infinity-castle-sound.mp3');
            audio.volume = 0.3;
            audio.playbackRate = 0.8; // Slower playback for exit effect
            audio.play().catch(e => console.log('Audio play failed:', e));
            // Navigate back to original - increased delay to let audio finish
            setTimeout(() => {
              window.location.href = 'http://localhost:3000';
            }, 2500);
          }}
          className="w-10 h-10 bg-gradient-to-br from-slate-600 to-slate-800 hover:from-slate-500 hover:to-slate-700 text-white rounded-xl flex items-center justify-center shadow-lg hover:shadow-xl hover:shadow-slate-500/30 transition-all duration-300 mt-3"
          style={{
            boxShadow: '0 4px 15px rgba(100, 116, 139, 0.4)'
          }}
          title="Exit Infinity Castle"
        >
          <ArrowLeft size={18} className="font-bold" />
        </motion.button>
      </div>
    </aside>
  );
};