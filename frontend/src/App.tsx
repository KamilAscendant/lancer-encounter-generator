import React, { useState } from 'react';

const App: React.FC = () => {
  const [players, setPlayers] = useState<number>(1);
  const [licenceLevel, setLicenceLevel] = useState<number>(1);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    alert(`Players: ${players}, Licence Level: ${licenceLevel}`);
  };

  return (
    <div className="flex items-center justify-center h-screen bg-gray-100">
      <form onSubmit={handleSubmit} className="bg-white p-6 rounded shadow-md">
        <h1 className="text-2xl font-bold mb-4">Lancer Encounter Generator</h1>
        <div className="mb-4">
          <label className="block text-gray-700">Number of Players</label>
          <input
            type="number"
            value={players}
            onChange={(e) => setPlayers(parseInt(e.target.value))}
            className="w-full px-3 py-2 border rounded"
            min="1"
          />
        </div>
        <div className="mb-4">
          <label className="block text-gray-700">Party Licence Level</label>
          <input
            type="number"
            value={licenceLevel}
            onChange={(e) => setLicenceLevel(parseInt(e.target.value))}
            className="w-full px-3 py-2 border rounded"
            min="1"
          />
        </div>
        <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded">
          Generate Encounter
        </button>
      </form>
    </div>
  );
};

export default App;
