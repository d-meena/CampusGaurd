import React from "react";

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
};

const CustomTable = ({ data , offset }) => {
  return (
    <div className="flex flex-col items-center">
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
                <td className="p-4 px-10 border">{index + 1 + offset}</td>
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
};

export default CustomTable;
