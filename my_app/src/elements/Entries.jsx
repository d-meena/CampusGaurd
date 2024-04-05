import axios from "axios";
import React, { useEffect, useState } from "react";
// import { Link } from 'react-router-dom'
const BASE_URL = process.env.REACT_APP_BASE_URL;
function Entries() {
  const [data, setData] = useState([]);

  useEffect(() => {
    axios
      .get(`${BASE_URL}/entries`)
      .then((res) => {
        console.log(res);
        setData(res.data);
        console.log(res);
      })
      .catch((err) => console.log(err));
  }, []);

  const formatDate = (date, format) => {
    if (!date) return "Not Done";
    const dateOptions = {
      year: "numeric",
      month: "long",
      day: "numeric",
    };

    const timeOptions = {
      hour: "numeric",
      minute: "numeric",
      second: "numeric",
    };

    return format === "date"
      ? date.toLocaleDateString("en-IN", dateOptions)
      : date.toLocaleString("en-IN", timeOptions);

    // const day = date.getUTCDate();
    // const month = date.getUTCMonth() + 1;
    // const year = date.getUTCFullYear();
    // const hours = date.getUTCHours();
    // const minutes = date.getUTCMinutes();

    // const pad = (num) => (num < 10 ? "0" + num : num);

    // if (format === 'date') {
    //   return `${pad(day)}-${pad(month)}-${year}`;
    // } else if (format === 'time') {
    //   return `${pad(hours)}:${pad(minutes)}`;
    // }
  };

  return (
    <div className="flex flex-col items-center">
      <h2 className="p-4">Entries of the Vehicle</h2>
      <table className="p-2">
        <thead className="bg-slate-700 text-white">
          <tr>
            <th className="p-4" rowSpan={2}>
              S.No.
            </th>
            <th className="p-4" rowSpan={2}>
              Vehicle Number
            </th>
            <th className="p-6" colSpan="2">
              Entry
            </th>
            <th colSpan="2">Exit</th>
          </tr>
          <tr>
            <th className="p-4">Date</th>
            <th>Time</th>
            <th>Date</th>
            <th>Time</th>
          </tr>
        </thead>
        <tbody>
          {data.map((entry, index) => {
            // Parse entry_time string into a Date object
            const entryTime = new Date(entry.entry_time);
            const exitTime = entry.exit_time ? new Date(entry.exit_time) : "";
            const entryDate = formatDate(entryTime, "date");
            const entryTimeString = formatDate(entryTime, "time");
            const exitDate = formatDate(exitTime, "date");
            const exitTimeString = formatDate(exitTime, "time");

            return (
              <tr className="bg-slate-300 text-center" key={entry.id}>
                <td className="p-4 px-10 border">{index + 1}</td>
                <td className="p-4 px-10 border">{entry.vehicle_no}</td>
                <td className="p-4 px-10 border">{entryDate}</td>
                <td className="p-4 px-10 border">{entryTimeString}</td>
                <td className="p-4 px-10 border">{exitDate}</td>
                <td className="p-4 px-10 border">{exitTimeString}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

export default Entries;
