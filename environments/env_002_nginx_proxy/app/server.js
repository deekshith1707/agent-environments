// Minimal upstream server for the Nginx proxy environment
const http = require("http");

const server = http.createServer((req, res) => {
  res.setHeader("X-Powered-By", "Express"); // agent must hide this
  res.setHeader("Content-Type", "application/json");
  res.writeHead(200);
  res.end(JSON.stringify({ status: "ok", path: req.url }));
});

server.listen(3000, "127.0.0.1", () => {
  console.log("Upstream app listening on 127.0.0.1:3000");
});
