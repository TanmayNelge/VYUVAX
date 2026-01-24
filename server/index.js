const express = require("express");
const bodyParser = require("body-parser");
const cors = require("cors");
const { spawn } = require("child_process");

const app = express();
app.use(bodyParser.json());
app.use(cors()); 

app.post("/move", (req, res) => {
  const python = spawn("python", ["../backend/api.py"]);

  python.stdin.write(JSON.stringify(req.body));
  python.stdin.end();

  let result = "";
  python.stdout.on("data", (data) => {
    result += data.toString();
  });

  python.stderr.on("data", (err) => {
    console.error(err.toString());
  });

  python.on("close", () => {
    console.log("Python finished, result:", result);
    try {
      res.json(JSON.parse(result));
    } catch (e) {
      res.status(500).json({ error: "Failed to parse Python output" });
    }
  });
});

app.listen(5000, () => console.log("Server running on port 5000"));
