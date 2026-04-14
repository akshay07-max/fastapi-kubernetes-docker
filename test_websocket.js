const WebSocket = require("ws");

const ws = new WebSocket("ws://127.0.0.1:8000/ws");

ws.on("open", () => {
  console.log("Connected to server");
  ws.send("Hello Server");
});

ws.on("message", (data) => {
  console.log("Received:", data.toString());
});

ws.on("close", () => {
  console.log("Disconnected");
});

ws.on("error", (err) => {
  console.error("Error:", err);
});
