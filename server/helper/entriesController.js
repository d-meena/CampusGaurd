const db = require("./dbController"); // Replace 'yourDbModule' with the module that handles your database connection

async function getEntries(req, res) {
  const defaultPage = 1;
  const defaultLimit = 10;

  const { page = defaultPage, limit = defaultLimit } = req.query;

  const offset = (page - 1) * limit;

  const get_query = `SELECT * FROM entry ORDER BY entry_time DESC LIMIT ${limit} OFFSET ${offset}`;
  const page_query = `SELECT CEIL(COUNT(*)/${limit}) AS total_pages FROM entry`;

  db.query(page_query, (err, total_pages) => {
    if (err) res.json({ message: "Server error", error: err });
    db.query(get_query, (err, result) => {
      if (err) res.json({ message: "Server error", error: err });
      pagination = {
        page: page,
        limit: limit,
        total_pages: total_pages[0].total_pages,
      };
      return res.json({ result, pagination });
    });
  });
}

function makeEntry(req, res) {
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
}

// app.get("/entries/:vehicle_no", (req, res) => {
//   const vehicle_no = req.params.vehicle_no;
//   const sql = "SELECT * FROM entry WHERE `vehicle_no`= ?";
//   db.query(sql, [vehicle_no], (err, result) => {
//     if (err) res.json({ message: "Server error" });
//     return res.json(result);
//   });
// });

module.exports = { getEntries, makeEntry };

/*

app.get("/entries", (req, res) => {
  const sql = "SELECT * FROM entry order by entry_time desc";
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

*/
