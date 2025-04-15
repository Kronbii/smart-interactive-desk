const express = require("express");
const http = require("http");
const socketIo = require("socket.io");
const cors = require("cors");
const os = require("os");
const fs = require("fs");
const path = require("path");

const app = express();
const PORT = process.env.PORT || 3000;

// Get local IP address
function getLocalIP() {
    const interfaces = os.networkInterfaces();
    for (const iface of Object.values(interfaces)) {
        for (const config of iface) {
            if (config.family === "IPv4" && !config.internal) {
                return config.address;
            }
        }
    }
    return "127.0.0.1";
}

const LOCAL_IP = getLocalIP();

// CORS setup
app.use(cors({
    origin: "*",
    methods: ["GET", "POST"],
    allowedHeaders: ["Content-Type"]
}));

app.use(express.json());
app.use(express.static("public"));

// Serve web interface
app.get("/", (req, res) => {
    res.sendFile(__dirname + "/public/index.html");
});

const server = http.createServer(app);

const io = socketIo(server, {
    cors: {
        origin: "*",
        methods: ["GET", "POST"],
        credentials: true
    }
});

io.on("connection", (socket) => {
    console.log("Client connected");

    socket.on("disconnect", () => {
        console.log("Client disconnected");
    });
});

// Path to control.json
const CONTROL_FILE = path.join(__dirname, "..", "control.json");


// Helper to load control.json safely
function loadControl() {
    try {
        const raw = fs.readFileSync(CONTROL_FILE, "utf8").trim();
        if (!raw) throw new Error("Empty control.json");
        return JSON.parse(raw);
    } catch (err) {
        console.error("Failed to read control.json:", err);
        return null;
    }
}

// Helper to save control.json
function saveControl(control) {
    try {
        fs.writeFileSync(CONTROL_FILE, JSON.stringify(control, null, 2));
    } catch (err) {
        console.error("Failed to write control.json:", err);
    }
}

// Endpoint to receive control commands (from GUI or mobile)
app.post("/send-action", (req, res) => {
    const action = req.body.action;
    if (!action) return res.status(400).json({ error: "Missing action" });

    console.log(`Action received: ${action}`);
    io.emit("action", action);

    const control = loadControl();
    if (!control) return res.status(500).json({ error: "Could not load control.json" });

    // Respect posture mode and emergency stop
    if (control.mode === "posture") {
        return res.status(403).json({ message: "System in posture mode. Action denied." });
    }
    if (control.emergency_stop) {
        return res.status(403).json({ message: "Emergency stop active. Action denied." });
    }

    // Update the command
    control.command = action;
    saveControl(control);

    return res.status(200).json({ message: `Action "${action}" written to control.json` });
});

// Emergency stop toggle
app.post("/emergency", (req, res) => {
    const control = loadControl();
    if (!control) return res.status(500).json({ error: "Could not load control.json" });

    const { state } = req.body;
    control.emergency_stop = !!state;
    saveControl(control);

    return res.status(200).json({ message: `Emergency stop set to ${state}` });
});

// Get current IP (for mobile apps)
app.get("/server-ip", (req, res) => {
    res.json({ ip: LOCAL_IP });
});

server.listen(PORT, "0.0.0.0", () => {
    console.log(`Server running at http://${LOCAL_IP}:${PORT}`);
});
