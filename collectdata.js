const mqtt = require("mqtt");
const fs = require("fs");

const brokerUrl = "mqtt://13.250.198.67";
const topic = "data/GAIPOM";
const topic2 = "data/PalmGroupSterilizer";
const username = "sm365";
const password = "Nov@flow6889";

const client = mqtt.connect(brokerUrl, {
  username: username,
  password: password,
});

client.on("connect", () => {
  console.log("Connected to MQTT broker");
  client.subscribe(topic2);
});

client.on("message", (topic, message) => {
  console.log(`Received message on topic: ${topic}`);
  console.log(`Message: ${message.toString()}`);

  // Store the message into a text file
  fs.appendFile("file.txt", message.toString(), (err) => {
    if (err) {
      console.error("Error writing to file:", err);
    } else {
      console.log("Message stored in file");
    }
  });
});

client.on("error", (error) => {
  console.error("MQTT client error:", error);
});
