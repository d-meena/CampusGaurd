const mysql = require('mysql');

const pool = mysql.createPool({
  host: process.env.DB_IP,
  database: process.env.DB_NAME,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
});

module.exports = pool;
