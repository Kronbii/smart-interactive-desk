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

    // Button event listeners for press and release
    document.getElementById("upBtn").addEventListener("mousedown", () => sendAction("u")); // Action on press
    document.getElementById("upBtn").addEventListener("mouseup", () => sendAction("s")); // Action on release
    
    document.getElementById("downBtn").addEventListener("mousedown", () => sendAction("d")); // Action on press
    document.getElementById("downBtn").addEventListener("mouseup", () => sendAction("s")); // Action on release

    document.getElementById("tiltUpBtn").addEventListener("mousedown", () => sendAction("tu")); // Action on press
    document.getElementById("tiltUpBtn").addEventListener("mouseup", () => sendAction("s")); // Action on release

    document.getElementById("tiltDownBtn").addEventListener("mousedown", () => sendAction("td")); // Action on press
    document.getElementById("tiltDownBtn").addEventListener("mouseup", () => sendAction("s")); // Action on release
}

// Call the function to initialize the WebSocket connection
initializeSocket();
