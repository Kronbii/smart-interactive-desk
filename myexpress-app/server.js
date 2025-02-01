const express = require("express");
const http = require("http");
const socketIo = require("socket.io");

const app = express();
const PORT = process.env.PORT || 3000;
const LOCAL_IP = "192.168.1.122";  // Replace this with your actual local IP

// Create the HTTP server
const server = http.createServer(app);

// Initialize Socket.io
const io = socketIo(server);

// Serve static files from the "public" folder
app.use(express.static("public"));

// Middleware to parse JSON
app.use(express.json());

// API Route to receive button presses from frontend
app.post("/send-action", (req, res) => {
    const action = req.body.action;
    console.log(`Action received: ${action}`);

    // Emit action to all connected clients
    io.emit("action", action);

    res.status(200).json({message:`Action ${action} received`});
});

// Start the server
server.listen(PORT, LOCAL_IP, () => {
    console.log(`Server running on http://${LOCAL_IP}:${PORT}`);
});