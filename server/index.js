const express = require("express");
const mysql = require("mysql");
const cors = require("cors");
const path = require("path");
const app = express();

app.use(cors());
app.use(express.json());

const PORT = process.env.PORT;

const db = require("./helper/dbController");

const { getEntries, makeEntry } = require("./helper/entriesController");

app.get("/entries", getEntries);
app.post("/make_entry", makeEntry);

app.listen(PORT, () => {
  console.log(`listening on PORT ${PORT} `);
});

