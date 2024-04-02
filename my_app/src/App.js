import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
// import "bootstrap/dist/css/bootstrap.min.css";
import Home from "./elements/Home";
import Entries from "./elements/Entries";
import MakeEntry from "./elements/MakeEntry";
// import Read from "./elements/Read";
function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/entries" element={<Entries />} />
        <Route path="/make_entry" element={<MakeEntry />} />
        {/* <Route path="/entries/:vehicle_no" element={<VehicleEntries />} />  */}
        {/* <Route path="/read/:id" element={<Read />} /> */}
      </Routes>
    </BrowserRouter>
  );
}

export default App;

