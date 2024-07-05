const mqtt = require("mqtt");
const express = require("express");
const WebSocket = require("ws");

const app = express();
const port = 3001;

const brokerUrl = "mqtt://13.250.198.67";
const topic = "data/GAIPOM";
const topic2 = "data/PalmGroupSterilizer";
const username = "sm365";
const password = "Nov@flow6889";

const client = mqtt.connect(brokerUrl, {
  username: username,
  password: password,
});

// Create a WebSocket server
const wss = new WebSocket.Server({ noServer: true });

wss.on("connection", (ws) => {
  console.log("WebSocket connection established");

  client.on("message", (topic, message) => {
    console.log(`Received message on topic: ${topic}`);
    console.log(`Message: ${message.toString()}`);

    // Send message to all connected WebSocket clients
    ws.send(message.toString());
  });
});

client.on("connect", () => {
  console.log("Connected to MQTT broker");
  client.subscribe(topic2);
});

client.on("error", (error) => {
  console.error("MQTT client error:", error);
});

// Serve static files from the public directory
app.use(express.static("public"));

// Upgrade HTTP server to WebSocket
const server = app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}/`);
});

server.on("upgrade", (request, socket, head) => {
  wss.handleUpgrade(request, socket, head, (ws) => {
    wss.emit("connection", ws, request);
  });
});
