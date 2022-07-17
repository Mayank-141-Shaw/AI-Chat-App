import { Provider, connect } from 'react-redux';
import { createStore } from 'redux';

import HistoryBox from './components/HistoryBox';
import './App.css';

function App() {

  //const store = createStore()

  return (
    <div>
      <h2 className="app-heading">ChatBot for Customer Service</h2>
      <div className="App">
        <HistoryBox />
      </div>
    </div>
  );
}

export default App;
