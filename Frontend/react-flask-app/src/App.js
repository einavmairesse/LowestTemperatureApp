
import './App.css';
import React, { Component } from "react";

class App extends Component {
  constructor() {
    super();
    this.state = { data: [] };
  }

  async componentDidMount() {
    const response = await fetch('http://127.0.0.1:5000/get_lowest_temp');
    const json = await response.json();
    this.setState({ data: json });
  }

  render() {
    var text = ""
    console.log(this.state.data)
    for( let prop in this.state.data ){
      text = text + "<li>" + prop + ":" + this.state.data[prop] + "</li>" ; 
    }

    console.log(text)
    
    return (
      <div>
        <ul>
        {text}
         </ul>
      </div>
    );
  }
}


export default App;