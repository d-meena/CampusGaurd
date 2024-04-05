const express = require("express");
const mysql = require("mysql");
const cors = require("cors");
const path = require("path");
const app = express();

app.use(cors());
app.use(express.json());


const HOST = process.env.HOST;
const APPUSER = process.env.APPUSER;
const PASSWORD = process.env.PASSWORD;
const PORT = process.env.PORT;

console.log("hello", APPUSER, PASSWORD, PORT);


const db = mysql.createConnection({
  host: {HOST},
  user: 'root',
  password: "Deep@2002",
  database: "btp1",
});

app.get("/entries", (req, res) => {
  const sql = "SELECT * FROM entry";
  db.query(sql, (err, result) => {
    if (err) res.json({ message: "Server error" });
    return res.json(result);
  });
});

app.post("/make_entry", (req, res) => {
  // console.log("body", req.body);
  const { vehicle_no, entry_type } = req.body;

  // format current time to mysql datetime
  const current_time = new Date();
  const tzo = current_time.getTimezoneOffset();
  const tzo_in_ms = tzo * 60 * 1000;
  const current_time_with_tzo = current_time - tzo_in_ms;
  const current_datetime = new Date(current_time_with_tzo)
    .toISOString()
    .slice(0, 19)
    .replace("T", " ");
  const query_vehicle = `select vehicle_no from entry where vehicle_no = "${vehicle_no}" and exit_time is NULL`;

  db.query(query_vehicle, (err, result) => {
    if (err) throw err;
    if (result.length == 0) {
      if (entry_type == "IN") {
        //inserting new entry
        const sql =
          "INSERT INTO entry (`vehicle_no`,`entry_time`,`exit_time`) VALUES (?, ?, ?)";
        const values = [vehicle_no, current_datetime, null];
        db.query(sql, values, (err, result) => {
          if (err) throw err;
          return res.json({
            success: true,
            message: "Entry added successfully",
          });
        });
      } else {
        // entry_tpye is out and entry is not there
        return res.json({ success: false, message: "entry not found" });
      }
    } else {
      if (entry_type == "IN") {
        //entry is already there
        return res.json({
          success: false,
          message: "Entry is already there",
        });
      } else {
        //making a exit of a entry
        const sql = `update entry set exit_time = "${current_datetime}" where vehicle_no = "${vehicle_no}" and exit_time is NULL`;
        db.query(sql, (err, result) => {
          if (err) throw err;
          return res.json({ success: true, message: "updated exit time" });
        });
      }
    }
  });
});

app.get("/entries/:vehicle_no", (req, res) => {
  const vehicle_no = req.params.vehicle_no;
  const sql = "SELECT * FROM entry WHERE `vehicle_no`= ?";
  db.query(sql, [vehicle_no], (err, result) => {
    if (err) res.json({ message: "Server error" });
    return res.json(result);
  });
});

//   app.post("/edit_user/:id", (req, res) => {
//     const id = req.params.id;
//     const sql =
//       "UPDATE student_details SET `name`=?, `email`=?, `age`=?, `gender`=? WHERE id=?";
//     const values = [
//       req.body.name,
//       req.body.email,
//       req.body.age,
//       req.body.gender,
//       id,
//     ];
//     db.query(sql, values, (err, result) => {
//       if (err)
//         return res.json({ message: "Something unexpected has occured" + err });
//       return res.json({ success: "Student updated successfully" });
//     });
//   });

//   app.delete("/delete/:id", (req, res) => {
//     const id = req.params.id;
//     const sql = "DELETE FROM student_details WHERE id=?";
//     const values = [id];
//     db.query(sql, values, (err, result) => {
//       if (err)
//         return res.json({ message: "Something unexpected has occured" + err });
//       return res.json({ success: "Student updated successfully" });
//     });
//   });

app.listen(PORT, () => {
  console.log(`listening on PORT ${PORT} `);
});
