# Smart Learning Table For Classrooms
## Members
- Rami Kronbi
- Bassam Kousa
- ALi Daaboul
- Mohamad Berjawi
- Mohamad Hariri

## Google Drive Link
https://drive.google.com/drive/folders/1InH4OToC-3ZCmpd2p8zu-zYlxD98OoeB?usp=drive_link
#### Subdirectories 
* Reports

## Repo Tree
``` bash
├── CAD
│   └── readme.md
├── final-report
│   └── readme.md
├── mems
│   └── readme.md
├── progress-reports
│   └── readme.md
├── prototype-video
│   └── readme.md
├── README.md
├── Report
│   └── readme.md
├── src
│   ├── arduino
│   │   └── readme.md
│   └── python
│       └── readme.md
└── tree.sh
```

## Intializing Node.js Web App
### Initialize Project Folder
mkdir myexpress-app && cd myexpress-app
### Initialize Node.js Project
npm init -y
### Install Required Dependencies
npm install express socket.io
### Create Backend Server
touch server.js
open server.js and paste the following code

``` js
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
```

### Create Front End File
create public folder in the project directory
``` bash
mkdir public
```

create front.html file inside public directory
``` bash
touch public/front.html
```
Open public/front.html and paste the following
``` html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Control Panel</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            margin-top: 50px;
        }
        button {
            margin: 10px;
            padding: 15px;
            font-size: 16px;
            cursor: pointer;
        }
        #actionDisplay {
            margin-top: 20px;
            font-size: 20px;
            color: blue;
        }
    </style>
</head>
<body>
    <h1>Control Panel</h1>
    <button id="upBtn">Up</button>
    <button id="downBtn">Down</button>
    <button id="tiltUpBtn">Tilting Up</button>
    <button id="tiltDownBtn">Tilting Down</button>

    <div id="actionDisplay"></div>

    <!-- Include Socket.io client library -->
    <script src="https://cdn.socket.io/4.0.0/socket.io.min.js"></script>

    <script>
        // Function to fetch server IP dynamically
        async function getServerIP() {
            try {
                const response = await fetch("/server-ip");
                const data = await response.json();
                return data.ip;  // Get the dynamically retrieved IP
            } catch (error) {
                console.error("Error fetching server IP:", error);
                return "127.0.0.1";  // Fallback to localhost
            }
        }

        // Initialize WebSocket connection dynamically
        async function initializeSocket() {
            const serverIP = await getServerIP();
            const socket = io(`http://${serverIP}:3000`);

            // Listen for actions from the server
            socket.on("action", (action) => {
                document.getElementById("actionDisplay").innerText = `Action: ${action}`;
            });

            // Function to send button action to the server
            function sendAction(action) {
                fetch("/send-action", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ action: action })
                })
                .then(response => response.json())
                .then(data => console.log(data.message))
                .catch(error => console.error("Error:", error));
            }

            // Button event listeners
            document.getElementById("upBtn").addEventListener("click", () => sendAction("up"));
            document.getElementById("downBtn").addEventListener("click", () => sendAction("down"));
            document.getElementById("tiltUpBtn").addEventListener("click", () => sendAction("tilting up"));
            document.getElementById("tiltDownBtn").addEventListener("click", () => sendAction("tilting down"));
        }

        // Call the function to initialize the WebSocket connection
        initializeSocket();
    </script>
</body>
</html>
```

### Run the server
``` bash
node server.js
```
you should see
``` bash
Server running on http://your_ip:your_port
```
### Connect Client Device
visit the following link
``` bash
http://your_ip:your_port/front.html
```

### Final Project Structure
``` bash
myexpress-app/
├── server.js           # Backend server
├── public/             # Frontend folder
│   └── front.html      # Frontend HTML file
├── node_modules/       # Installed dependencies
├── package.json        # Project config
└── package-lock.json   # Lock file
```