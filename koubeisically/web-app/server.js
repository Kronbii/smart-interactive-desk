const express = require("express");
const http = require("http");
const socketIo = require("socket.io");
const os = require("os");

const app = express();
const PORT = process.env.PORT || 3000;

// Function to get the local IP address dynamically
function getLocalIP() {
    const interfaces = os.networkInterfaces();
    for (const iface of Object.values(interfaces)) {
        for (const config of iface) {
            if (config.family === "IPv4" && !config.internal) {
                return config.address;  // Return first non-internal IPv4 address
            }
        }
    }
    return "127.0.0.1"; // Fallback to localhost
}

const LOCAL_IP = getLocalIP();

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

    res.status(200).json({ message: `Action "${action}" received` });
});

// API to serve the server's IP dynamically
app.get("/server-ip", (req, res) => {
    res.json({ ip: LOCAL_IP });
});

// Start the server
server.listen(PORT, LOCAL_IP, () => {
    console.log(`Server running on http://${LOCAL_IP}:${PORT}`);
});