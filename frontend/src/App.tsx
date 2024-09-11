import React, { useState } from 'react';

const App: React.FC = () => {
  const [players, setPlayers] = useState<number>(1);
  const [licenceLevel, setLicenceLevel] = useState<number>(1);
  const [encounter, setEncounter] = useState<any>(null);  // Change state to store full response

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Try to fetch the encounter data from the Flask backend
    try {
      const response = await fetch('http://127.0.0.1:5000/api/encounter');
      const data = await response.json();
      setEncounter(data);  // Store the entire response
    } catch (error) {
      console.error('Error fetching the encounter:', error);
    }
  };

  const validParty = players >=1 && players <= 6 && licenceLevel >=0 && licenceLevel <= 12;

  return (
    <div className="flex items-center justify-center h-screen bg-gray-100">
      <form onSubmit={handleSubmit} className="bg-white p-6 rounded shadow-md">
        <h1 className="text-2xl font-bold mb-4">Lancer Encounter Generator</h1>
        <div className="mb-4">
          <label className="block text-gray-700">Number of Players</label>
          <input
            type="number"
            value={players}
            onChange={(e) => {
              const playerNo = parseInt(e.target.value);
              if (playerNo >= 1 && playerNo <= 6) {
                setPlayers(playerNo);
              }
            }}

            className="w-full px-3 py-2 border rounded"
            min="1"
          />
        </div>
        <div className="mb-4">
          <label className="block text-gray-700">Party Licence Level</label>
          <input
            type="number"
            value={licenceLevel}
            onChange={(e) => {
              const value = parseInt(e.target.value);
              // Ensure the value stays between 0 and 12
              if (value >= 0 && value <= 12) {
                setLicenceLevel(value);}
              }}
            className="w-full px-3 py-2 border rounded"
            min="1"
          />
        </div>
        <button 
          type="submit" 
          className="bg-blue-500 text-white px-4 py-2 rounded"
          disabled={!validParty}>
          Generate Encounter
        </button>
        {encounter && (
          <div className="mt-4 p-4 bg-green-100 border rounded">
            <h2 className="font-bold">Encounter Generated:</h2>
            <p><strong>Message:</strong> {encounter.message}</p>
            <p><strong>Name:</strong> {encounter.name}</p>
            <p><strong>Difficulty:</strong> {encounter.difficulty}</p>
            <p><strong>Details:</strong> {encounter.details}</p>
          </div>
        )}
      </form>
    </div>
  );
};

export default App;
