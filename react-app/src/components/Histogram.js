import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

const Histogram = ({ data }) => {
    return (
        <BarChart width={600} height={300} data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="value" fill="#8884d8" />
        </BarChart>
    );
}

export default Histogram;


// in App.js 

// import React from 'react';
// import Histogram from './components/Histogram';

// const data = [
//     {name: 'Category A', value: 400},
//     {name: 'Category B', value: 300},
//     // ... more data
// ];

// function App() {
//   return (
//     <div>
//       <Histogram data={data} />
//     </div>
//   );
// }

// export default App;
