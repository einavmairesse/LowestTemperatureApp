import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [weatherData, setWeatherData] = useState([]);

  useEffect(() => {
    // GET request using fetch inside useEffect React hook
    fetch('http://127.0.0.1:5000/get_lowest_temp')
        .then(response => response.json())
        .then(r => setWeatherData(r));
// empty dependency array means this effect will only run once (like componentDidMount in classes)
}, []);



  return (
    <div className="App">
      <header className="App-header">

        hi ...

        <p>city_name: {weatherData.city_name}.</p>
        <p>feels_like: {weatherData.feels_like}.</p>
        <p>grnd_level: {weatherData.grnd_level}.</p>
      </header>
    </div>
  );
}

export default App;