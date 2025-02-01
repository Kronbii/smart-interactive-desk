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

```
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
    console.log(Action received: ${action});

    // Emit action to all connected clients
    io.emit("action", action);

    res.status(200).json({ message: Action "${action}" received });
});

// Start the server
server.listen(PORT, LOCAL_IP, () => {
    console.log(Server running on http://${LOCAL_IP}:${PORT});
});
```