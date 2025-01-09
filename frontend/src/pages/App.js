import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import Pricing from './Pricing';
import Transparency from './Transparency';
import Home from './Home';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/pricing" element={<Pricing />} />
        <Route path="/transparency" element={<Transparency />} />
      </Routes>
    </Router>
  );
}

export default App;