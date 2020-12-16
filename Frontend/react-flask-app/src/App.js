
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
    var text = [];
    console.log(this.state.data)
    for( let prop in this.state.data ){
      text.push([prop, this.state.data[prop]]) ; 
  }
    
    return (
      <table border="1" align="center">
      {text.map(function(key, value) {
        // return <tr><td>{key[0]}</td><td>{key[1]}</td></tr>
        return <tbody><td>{key[0]}</td> <td>{key[1]}</td></tbody>
      })}
      </table>
    );
  }
}

export default App;