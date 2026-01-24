const express = require("express");
const bodyParser = require("body-parser");
const { spawn } = require("child_process");

const app = express();
app.use(bodyParser.json());

app.post("/move", (req, res) => {
  const python = spawn("python", ["backend/api.py"]);

  python.stdin.write(JSON.stringify(req.body));
  python.stdin.end();

  python.stdout.on("data", (data) => {
    res.json(JSON.parse(data.toString()));
  });

  python.stderr.on("data", (err) => {
    console.error(err.toString());
  });
});

app.listen(5000, () => {
  console.log("Node server running on port 5000");
});
