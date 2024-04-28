// import React, { useState } from "react";
// import axios from "axios";
// import CustomButton from "../customUI/CustomButton";

// function MakeEntry() {
//   const BASE_URL = process.env.REACT_APP_BASE_URL;
//   const [value, setValue] = useState();

//   function handleIn(e) {
//     e.preventDefault();
//     console.log("handling in");
//     const requestBody = {
//       vehicle_no: value,
//       entry_type: "IN",
//     };
//     axios
//       .post(`${process.env.REACT_APP_BASE_URL}/make_entry`, requestBody)
//       .then((res) => {
//         console.log("Server Response ", res);
//       })
//       .catch((err) => console.log(err));
//   }

//   function handleOut(e) {
//     e.preventDefault();
//     console.log("handling out");
//     const requestBody = {
//       vehicle_no: value,
//       entry_type: "OUT",
//     };
//     axios
//       .post(`${BASE_URL}/make_entry`, requestBody)
//       .then((res) => {
//         console.log("Server Response ", res);
//       })
//       .catch((err) => console.log(err));
//   }

//   return (
//     <div className="text-center">
//       Make a entry
//       <input
//         className="p-2 rounded-md text-lg"
//         type="text"
//         value={value}
//         onChange={(e) => setValue(e.target.value)}
//       />
//       <CustomButton onClick={handleIn}>In</CustomButton>
//       <CustomButton onClick={handleOut}>Out</CustomButton>
//     </div>
//   );
// }

// export default MakeEntry;
