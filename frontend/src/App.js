import React from 'react';
import Wad from 'web-audio-daw';

class App extends React.Component {
  constructor(props) {
    super(props)
    this.state = { beats: [] };
  }

  async componentDidMount() {
    try {
      const res = await fetch('/api/beats/');
      const beats = await res.json();
      this.setState({beats: beats});
    } catch (e) {
      console.log(e);
    }
  }

  render() {
    return (
      <div>
        <h1>Beats</h1>
        {this.state.beats.map(item => (
          <div key={item.id}>
            <h2>{item.name} <SongPreview file={item.file}/></h2>
            <span>BPM: {item.bpm}</span>
          </div>
        ))}
      </div>
    );
  }
}

function SongPreview(props){
    const song = new Wad({source : props.file});
    return(
      <span>
        <button onClick={() => {song.play()}}>Play</button>
        <button onClick={() => {song.stop()}}>Stop</button>
      </span>
    );
  }

export default App;