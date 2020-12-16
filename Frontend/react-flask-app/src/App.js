
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
    // for (let prop in this.state.data){
    //   text = text + prop + ": " +this.state.data[prop];
    // }
   for( let prop in this.state.data ){
     text.push([prop, "  ", this.state.data[prop]]) ; 
  }
    
    return (
      <ul>
      {text.map(function(key, value) {
        return <li key={key}>{key}</li>
      })}
      </ul>
    );
  }
}

function makeUL(array) {
  // Create the list element:
  var list = document.createElement('ul');

  for (var i = 0; i < array.length; i++) {
      // Create the list item:
      var item = document.createElement('li');

      // Set its contents:
      item.appendChild(document.createTextNode(array[i]));

      // Add it to the list:
      list.appendChild(item);
  }

  // Finally, return the constructed list:
  return list;
}


export default App;