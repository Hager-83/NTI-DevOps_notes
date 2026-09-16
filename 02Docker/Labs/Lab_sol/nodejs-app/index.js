const express = require("express");
const os = require("os");

const app = express();
const port = process.env.PORT || 3000;

app.get("/", (req, res) => {
  res.json({
    message: "Hello from the Node.js app!",
    nodeVersion: process.version,
    hostname: os.hostname(),
  });
});

app.get("/health", (req, res) => {
  res.json({ status: "ok" });
});

app.listen(port, "0.0.0.0", () => {
  console.log(`Server listening on port ${port}`);
});
