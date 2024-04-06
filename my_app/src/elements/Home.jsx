import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import CustomButton from "../customUI/CustomButton";

function Home() {
  const navigate = useNavigate();
  const [isMakeEntryOpen, setIsMakeEntryOpen] = useState(false);

  const [value, setValue] = useState("");


  function handleIn(e) {
    e.preventDefault();
    console.log("handling in");
    const requestBody = {
      vehicle_no: value.toUpperCase(),
      entry_type: "IN",
    };
    axios
      .post(`${process.env.REACT_APP_BASE_URL}/make_entry`, requestBody)
      .then((res) => {
        console.log("Server Response ", res);
      })
      .catch((err) => console.log(err));
  }

  function handleOut(e) {
    e.preventDefault();
    console.log("handling out");
    const requestBody = {
      vehicle_no: value.toUpperCase(),
      entry_type: "OUT",
    };
    axios
      .post(`${process.env.REACT_APP_BASE_URL}/make_entry`, requestBody)
      .then((res) => {
        console.log("Server Response ", res);
      })
      .catch((err) => console.log(err));
  }

  return (
    <div className="text-center min-h-screen flex flex-col">
      <h1 className="text-4xl p-2">Campus Guard</h1>
      <p className="text-lg font-semibold p-2">Entry-Exit System for IITR</p>
      <hr />
      <div className="flex gap-8 justify-center grow items-center">
        <CustomButton type={1} onClick={() => navigate("/entries")}>
          Go to entries
        </CustomButton>
        <CustomButton type={1} onClick={() => setIsMakeEntryOpen(true)}>
          Make an entry
        </CustomButton>
      </div>
      {isMakeEntryOpen && (
        <>
          <div className="absolute inset-0 bg-slate-900/40 backdrop-blur"></div>
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 text-center bg-slate-300 rounded-lg p-12 flex flex-col gap-4">
            <CustomButton
              customClasses={
                "absolute right-0 top-0 m-2 bg-transparent text-slate-900 font-bold hover:text-white"
              }
              onClick={() => {
                setIsMakeEntryOpen(false);
              }}
            >
              X
            </CustomButton>
            <p className="font-medium text-lg uppercase text-slate-700">
              Make an entry
            </p>
            <input
              className="p-2 rounded-md text-lg w-72 uppercase"
              type="text"
              value={value}
              onChange={(e) => setValue(e.target.value)}
            />
            <div className="flex grow gap-2">
              <CustomButton onClick={handleIn} customClasses="grow">
                IN
              </CustomButton>
              <CustomButton onClick={handleOut} customClasses="grow">
                OUT
              </CustomButton>
            </div>
          </div>
        </>
      )}
    </div>
  );
}

export default Home;
