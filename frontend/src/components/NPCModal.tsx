import React from 'react';
import { NPC } from '../types';

interface NPCModalProps {
  npc: NPC;
  isOpen: boolean;
  onClose: () => void;
}

const NPCModal: React.FC<NPCModalProps> = ({ npc, isOpen, onClose }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <div className="flex justify-between items-start">
            <h2 className="text-2xl font-bold text-gray-900">{npc.name}</h2>
            <button 
              onClick={onClose}
              className="text-gray-400 hover:text-gray-500"
            >
              <span className="sr-only">Close</span>
              <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          {/* Content sections */}
          <div className="mt-4">
            <div className="mb-4">
              <h3 className="text-lg font-medium text-gray-900">Description</h3>
              <p className="mt-2 text-gray-600">{npc.description}</p>
            </div>

            <div className="mb-4">
              <h3 className="text-lg font-medium text-gray-900">Tactics</h3>
              <p className="mt-2 text-gray-600">{npc.tactics}</p>
            </div>

            {/* Full stats grid */}
            <div className="mb-4">
              <h3 className="text-lg font-medium text-gray-900 mb-2">Stats</h3>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
                {Object.entries(npc.stats).map(([key, value]) => (
                  <div key={key} className="bg-gray-50 p-2 rounded">
                    <div className="font-medium text-gray-500 capitalize">{key}</div>
                    <div className="text-gray-900">{Array.isArray(value) ? value.join(', ') : value}</div>
                  </div>
                ))}
              </div>
            </div>

            {/* Features */}
            <div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">Features</h3>
              <div className="space-y-4">
                <div>
                  <h4 className="font-medium text-gray-700">Base Features</h4>
                  <ul className="mt-1 list-disc list-inside text-gray-600">
                    {npc.features.base.map((feature, index) => (
                      <li key={index}>{feature}</li>
                    ))}
                  </ul>
                </div>
                <div>
                  <h4 className="font-medium text-gray-700">Optional Features</h4>
                  <ul className="mt-1 list-disc list-inside text-gray-600">
                    {npc.features.optional.map((feature, index) => (
                      <li key={index}>{feature}</li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default NPCModal;
