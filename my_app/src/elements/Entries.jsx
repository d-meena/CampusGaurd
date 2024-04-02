import axios from "axios";
import React, { useEffect, useState } from "react";
import BASE_URL from "../apiConfig";
// import { Link } from 'react-router-dom'

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

    return format == "date"
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
    <div>
      <h3>Entries of the Vehicle</h3>
      <table>
        <thead>
          <tr>
            <th>Vehicle Number</th>
            <th colSpan="2">Entry</th>
            <th colSpan="2">Exit</th>
          </tr>
          <tr>
            <th></th>
            <th>Date</th>
            <th>Time</th>
            <th>Date</th>
            <th>Time</th>
          </tr>
        </thead>
        <tbody>
          {data.map((entry) => {
            // Parse entry_time string into a Date object
            const entryTime = new Date(entry.entry_time);
            const exitTime = entry.exit_time ? new Date(entry.exit_time) : "";
            const entryDate = formatDate(entryTime, "date");
            const entryTimeString = formatDate(entryTime, "time");
            const exitDate = formatDate(exitTime, "date");
            const exitTimeString = formatDate(exitTime, "time");

            return (
              <tr key={entry.id}>
                <td>{entry.vehicle_no}</td>
                <td>{entryDate}</td>
                <td>{entryTimeString}</td>
                <td>{exitDate}</td>
                <td>{exitTimeString}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

export default Entries;
