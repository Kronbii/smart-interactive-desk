const express = require("express");
const http = require("http");
const socketIo = require("socket.io");
const cors = require("cors");
const os = require("os");
const { spawn } = require("child_process");

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

// CORS needs to be BEFORE routes and sockets
app.use(cors({ 
    origin: "*", 
    methods: ["GET", "POST"],
    allowedHeaders: ["Content-Type"]
}));

app.use(express.json());
app.use(express.static("public"));
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

app.post("/send-action", (req, res) => {
    const action = req.body.action;
    console.log(`Action received: ${action}`);

    io.emit("action", action);

    const pythonProcess = spawn("python3", ["anh.py"]);
    pythonProcess.stdin.write(action + "\n");
    pythonProcess.stdin.end();

    pythonProcess.stdout.on("data", (data) => {
        console.log(`${data.toString()}`);
        res.status(200).json({ message: `Action "${action}" processed by Python`, response: data.toString() });
    });

    pythonProcess.stderr.on("data", (data) => {
        console.error(`stderr: ${data.toString()}`);
        res.status(500).json({ message: "Error processing action", error: data.toString() });
    });
});

app.get("/server-ip", (req, res) => {
    res.json({ ip: LOCAL_IP });
});

server.listen(PORT, "0.0.0.0", () => {
    console.log(`Server running at http://${LOCAL_IP}:${PORT}`);
});
