# **Smart Learning Table For Classrooms**

## **Members**
- Rami Kronbi
- Bassam Kousa
- Ali Daaboul
- Mohamad Berjawi
- Mohamad Hariri

## **Google Drive Link**
[Project Resources](https://drive.google.com/drive/folders/1InH4OToC-3ZCmpd2p8zu-zYlxD98OoeB?usp=drive_link)

#### **Subdirectories**
- **Reports**

## **Repository Structure**
```bash
├── CAD
│   └── readme.md
├── final-report
│   └── readme.md
├── mems
│   └── readme.md
├── progress-reports
│   └── readme.md
├── prototype-video
│   └── readme.md
├── README.md
├── Report
│   └── readme.md
├── src
│   ├── arduino
│   │   └── readme.md
│   └── python
│       └── readme.md
└── tree.sh
```

---

## **Initializing Node.js Web Application**

### **1️⃣ Create Project Folder**
```bash
mkdir myexpress-app && cd myexpress-app
```

### **2️⃣ Initialize Node.js Project**
```bash
npm init -y
```

### **3️⃣ Install Required Dependencies**
```bash
npm install express socket.io
```

### **4️⃣ Create Backend Server**
Create `server.js` and paste the following code:

```javascript
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
                return config.address;
            }
        }
    }
    return "127.0.0.1";
}

const LOCAL_IP = getLocalIP();
const server = http.createServer(app);
const io = socketIo(server);

app.use(express.static("public"));
app.use(express.json());

app.post("/send-action", (req, res) => {
    const action = req.body.action;
    console.log(`Action received: ${action}`);
    io.emit("action", action);
    res.status(200).json({ message: `Action "${action}" received` });
});

app.get("/server-ip", (req, res) => {
    res.json({ ip: LOCAL_IP });
});

server.listen(PORT, LOCAL_IP, () => {
    console.log(`Server running on http://${LOCAL_IP}:${PORT}`);
});
```

---

## **Frontend Setup**

### **1️⃣ Create Public Folder**
```bash
mkdir public
```

### **2️⃣ Create Frontend HTML File**
```bash
touch public/front.html
```

Paste the following content into `public/front.html`:

```html
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

    <script src="https://cdn.socket.io/4.0.0/socket.io.min.js"></script>
    <script>
        async function getServerIP() {
            try {
                const response = await fetch("/server-ip");
                const data = await response.json();
                return data.ip;
            } catch (error) {
                console.error("Error fetching server IP:", error);
                return "127.0.0.1";
            }
        }

        async function initializeSocket() {
            const serverIP = await getServerIP();
            const socket = io(`http://${serverIP}:3000`);

            socket.on("action", (action) => {
                document.getElementById("actionDisplay").innerText = `Action: ${action}`;
            });

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

            document.getElementById("upBtn").addEventListener("click", () => sendAction("up"));
            document.getElementById("downBtn").addEventListener("click", () => sendAction("down"));
            document.getElementById("tiltUpBtn").addEventListener("click", () => sendAction("tilting up"));
            document.getElementById("tiltDownBtn").addEventListener("click", () => sendAction("tilting down"));
        }

        initializeSocket();
    </script>
</body>
</html>
```

---

## **Running the Server**
```bash
node server.js
```
You should see:
```bash
Server running on http://your_ip:your_port
```

## **Connecting a Client Device**
Open the following URL on any browser:
```bash
http://your_ip:your_port/front.html
```

---

## **ESP32 Boards Repo**
```
https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
```