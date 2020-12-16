
import './App.css';

 function App() {
  let weatherData = fetchWeatheData();
  console.log(weatherData);
 
  return <p> einav</p>;
}



async function fetchWeatheData() {
  const response = await fetch ('http://127.0.0.1:5000/get_lowest_temp');
  const weatherData = await response.json();
  return weatherData;
}


export default App;