import React, { useState, useEffect } from 'react';

const GameList = ({ onSelectGame }) => {
  const [games, setGames] = useState([]);

  useEffect(() => {
    fetch('http://localhost:8080/api/games')
      .then(response => response.json())
      .then(data => setGames(data.GamesList))
      .catch(error => console.error('Error fetching games:', error));
  }, []);

  const handleSelectChange = (event) => {
    onSelectGame(event.target.value);
  };

  return (
    <select onChange={handleSelectChange} defaultValue="">
      <option value="" disabled>Select a game</option>
      {games.map(game => (
        <option key={game.game_id} value={game.game_id}>
          {game.home_team} vs {game.away_team} - {game.game_date} - {game.venue_name}
        </option>
      ))}
    </select>
  );
};

export default GameList;