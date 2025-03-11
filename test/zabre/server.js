const express = require("express");
const http = require("http");
const socketIo = require("socket.io");
const os = require("os");

const app = express();
const PORT = 3000;

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

const server = http.createServer(app);
const io = socketIo(server, {
    cors: {
        origin: "*",
        methods: ["GET", "POST"]
    }
});

app.use(express.json());

io.on("connection", (socket) => {
    console.log("Client connected");

    socket.on("disconnect", () => {
        console.log("Client disconnected");
    });
});

app.post("/send-action", (req, res) => {
    const action = req.body.action;
    console.log(`Action received: ${action}`);
    io.emit("action", action);
    res.json({ message: `Action "${action}" received` });
});

server.listen(PORT, "0.0.0.0", () => {
    console.log(`Server running at http://${LOCAL_IP}:${PORT}`);
});

const cors = require("cors");

app.use(cors({ 
    origin: "*", 
    methods: ["GET", "POST"],
    allowedHeaders: ["Content-Type"]
}));