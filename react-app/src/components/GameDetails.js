import React, { useState, useEffect, useRef } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

const GameDetails = ({ gameDetails }) => {
    const chartContainerRef = useRef();
    const [chartWidth, setChartWidth] = useState(0);
    const firstSimulation = gameDetails.SimulationsList[0];
    const homeTeamName = firstSimulation.home_team;
    const awayTeamName = firstSimulation.away_team;
  
    const histogramData = gameDetails.SimulationsList.map(simulation => ({
      name: `Run ${simulation.simulation_run}`,
      [homeTeamName]: simulation.home_team_score,
      [awayTeamName]: simulation.away_team_score,
    }));

    useEffect(() => {
      if (chartContainerRef.current) {
          setChartWidth(chartContainerRef.current.offsetWidth);
      }
  }, []);

    return (
      <div className="chart-container" ref={chartContainerRef}>
        <h2>Game Details</h2>
        <p><b>{homeTeamName}</b> Home Team Win Percentage: {gameDetails.HomeTeamWinPercentage}</p>
        
        <BarChart width={chartWidth} 
              height={500} 
              data={histogramData} 
              margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
              barCategoryGap="20%">
            <CartesianGrid strokeDasharray="6 6" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey={homeTeamName} fill="#8884d8" barSize={60} />
            <Bar dataKey={awayTeamName} fill="#82ca9d" barSize={60} />
        </BarChart>
        </div>
    );
  };

  export default GameDetails;