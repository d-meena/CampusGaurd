import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./elements/Home";
import Entries from "./elements/Entries";
function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/entries" element={<Entries />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
