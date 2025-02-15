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

[Server Code](src/web-app-test/server.js)

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