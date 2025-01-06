import React, { useState } from 'react';
import NPCCard from './components/NPCCard';
import { NPC, Encounter } from './types';

const App: React.FC = () => {
  const [players, setPlayers] = useState<number>(1);
  const [licenceLevel, setLicenceLevel] = useState<number>(1);
  const [encounter, setEncounter] = useState<Encounter | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    try {
      const response = await fetch(
        `http://127.0.0.1:5000/api/encounter?players=${players}&level=${licenceLevel}`
      );
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to generate encounter');
      }

      const data = await response.json();
      setEncounter(data);
    } catch (error) {
      setError(error instanceof Error ? error.message : 'An error occurred');
    }
  };

  const validParty = players >= 1 && players <= 6 && licenceLevel >= 0 && licenceLevel <= 12;

  return (
    <div className="min-h-screen bg-gray-100 py-6 flex flex-col">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-8 bg-white shadow-lg rounded-lg p-6">
          <h1 className="text-3xl font-bold mb-8 text-center text-gray-900">
            Lancer Encounter Generator
          </h1>
          
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700">
                Number of Players
              </label>
              <input
                type="number"
                value={players}
                onChange={(e) => setPlayers(Number(e.target.value))}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                min="1"
                max="6"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">
                License Level
              </label>
              <input
                type="number"
                value={licenceLevel}
                onChange={(e) => setLicenceLevel(Number(e.target.value))}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                min="0"
                max="12"
              />
            </div>

            <button
              type="submit"
              disabled={!validParty}
              className={`w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white 
                ${validParty 
                  ? 'bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500'
                  : 'bg-gray-300 cursor-not-allowed'}`}
            >
              Generate Encounter
            </button>
          </form>

          {error && (
            <div className="mt-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
              {error}
            </div>
          )}
        </div>

        {encounter && (
          <div className="mt-8">
            <h2 className="text-2xl font-bold mb-4">
              Generated Encounter (Tier {encounter.tier})
            </h2>
            
            {Object.entries(encounter.npcs_by_role).map(([role, npcs]) => (
              <div key={role} className="mb-8">
                <h3 className="text-xl font-semibold mb-4 capitalize">
                  {role} ({npcs.length})
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {npcs.map((npc, index) => (
                    <NPCCard key={`${npc.name}-${index}`} npc={npc} />
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default App;
