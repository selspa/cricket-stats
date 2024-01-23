import React, { useState, useEffect } from 'react';
import GameList from './components/GamesList';
import GameDetails from './components/GameDetails';

const App = () => {
  const [selectedGameId, setSelectedGameId] = useState(null);
  const [selectedGameDetails, setSelectedGameDetails] = useState(null);

  useEffect(() => {
    if (selectedGameId !== null) {
      fetch(`http://localhost:8080/api/simulations?game_id=${selectedGameId}`, {port: 8080})
        .then(response => response.json())
        .then(data => setSelectedGameDetails(data))
        .catch(error => console.error('Error:', error));
    }
  }, [selectedGameId]);

  const handleSelectGame = (gameId) => {
    setSelectedGameId(gameId);
  };

  return (
    <div>
      <GameList onSelectGame={handleSelectGame} />
      {selectedGameDetails && <GameDetails gameDetails={selectedGameDetails} />}
    </div>
  );
};

export default App;