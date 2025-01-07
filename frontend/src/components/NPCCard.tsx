import React from 'react';
import { NPC } from '../types';
import { useState } from 'react';
import NPCModal from './NPCModal';
interface NPCCardProps {
  npc: NPC;
}

const NPCCard: React.FC<NPCCardProps> = ({ npc }) => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  
  return (
    <div className="bg-white shadow-lg rounded-lg p-6 mb-4">
      <div className="flex justify-between items-start">
        <h3 className="text-xl font-bold text-gray-900">{npc.name}</h3>
        <span className="px-2 py-1 text-sm rounded bg-gray-200 text-gray-700">
          Tier {npc.tier}
        </span>
      </div>
      
      <div className="mt-2">
        <span className="text-sm font-medium text-indigo-600 capitalize">
          {npc.role}
        </span>
      </div>

      <div className="mt-4 grid grid-cols-4 gap-2 text-sm">
        <div className="text-center p-1 bg-gray-50 rounded">
          <div className="font-semibold">HP</div>
          <div>{npc.stats.hp}</div>
        </div>
        <div className="text-center p-1 bg-gray-50 rounded">
          <div className="font-semibold">Armor</div>
          <div>{npc.stats.armor}</div>
        </div>
        <div className="text-center p-1 bg-gray-50 rounded">
          <div className="font-semibold">Evade</div>
          <div>{npc.stats.evade}</div>
        </div>
        <div className="text-center p-1 bg-gray-50 rounded">
          <div className="font-semibold">E-Def</div>
          <div>{npc.stats.edef}</div>
        </div>
      </div>

      <div className="mt-4">
        <h4 className="font-semibold text-sm text-gray-700">Features</h4>
        <div className="mt-1">
          <div className="text-sm">
            <span className="font-medium">Base: </span>
            {npc.features.base.join(', ')}
          </div>
          <div className="text-sm mt-1">
            <span className="font-medium">Optional: </span>
            {npc.features.optional.join(', ')}
          </div>
        </div>
      </div>

      <button 
        onClick={() => setIsModalOpen(true)}
        className="mt-4 text-sm text-indigo-600 hover:text-indigo-800"
      >
        Show full details
      </button>

      <NPCModal 
        npc={npc}
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
      />
    </div>
  );
};

export default NPCCard; 