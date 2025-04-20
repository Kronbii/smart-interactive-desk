const express = require("express");
const http = require("http");
const socketIo = require("socket.io");
const cors = require("cors");
const os = require("os");
const axios = require("axios");

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

// Middleware
app.use(cors({
    origin: "*",
    methods: ["GET", "POST"],
    allowedHeaders: ["Content-Type"]
}));

app.use(express.json());
const path = require("path");
app.use(express.static(path.join(__dirname, "public")));


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
    console.log("⚡ Client connected");
    socket.on("disconnect", () => {
        console.log("🛑 Client disconnected");
    });
});

// === Replaces old Python spawn method ===
app.post("/send-action", async (req, res) => {
    const action = req.body.action;
    if (!action) return res.status(400).json({ error: "Missing action" });

    console.log(`🖱️ Action received: "${action}"`);
    io.emit("action", action);

    try {
        const response = await axios.post("http://localhost:5001/send-command", {
            command: action
        }, { timeout: 2000 }); // add timeout just in case

        console.log("✅ Flask response:", response.data);
        res.status(200).json({
            message: `Action "${action}" processed`,
            response: response.data
        });
    } catch (err) {
        console.error("❌ Flask error:", err.message);
        res.status(500).json({ error: "Bridge error", details: err.message });
    }
});

app.get("/server-ip", (req, res) => {
    res.json({ ip: LOCAL_IP });
});

server.listen(PORT, "0.0.0.0", () => {
    console.log("=======================================");
    console.log("🚀  Node.js Web Control Server Started");
    console.log(`🌐  Access it from: http://${LOCAL_IP}:${PORT}`);
    console.log("=======================================");
});
