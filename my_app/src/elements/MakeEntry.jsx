import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import BASE_URL from "../apiConfig";

function MakeEntry() {
  const [value, setValue] = useState();

  const navigate = useNavigate();

  function handleIn(e) {
    e.preventDefault();
    console.log("handling in");
    const requestBody = {
      vehicle_no: value,
      entry_type: "IN",
    };
    axios
      .post(`${BASE_URL}/make_entry`, requestBody)
      .then((res) => {
        console.log("Server Response ", res);
      })
      .catch((err) => console.log(err));
  }

  function handleOut(e) {
    e.preventDefault();
    console.log("handling out");
    const requestBody = {
      vehicle_no: value,
      entry_type: "OUT",
    };
    axios
      .post(`${BASE_URL}/make_entry`, requestBody)
      .then((res) => {
        console.log("Server Response ", res);
      })
      .catch((err) => console.log(err));
  }

  return (
    <div>
      Make a entry
      <input
        type="text"
        value={value}
        onChange={(e) => setValue(e.target.value)}
      />
      <button onClick={handleIn}>In</button>
      <button onClick={handleOut}>Out</button>
    </div>
  );
}

export default MakeEntry;
