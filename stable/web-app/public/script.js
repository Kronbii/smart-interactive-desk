//const serverIP = await getServerIP();
const socket = io("http://192.168.0.5:3000");

// Listen for actions from the server
socket.on("action", (action) => {
    document.getElementById("actionDisplay").innerText = `Action: ${action}`;
});

// Function to send button action to the server
function sendAction(action) {
    fetch("http://192.168.0.5:3000/send-action", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ action: action })
    })
    .then(response => response.json())
    .then(data => console.log(data.message))
    .catch(error => console.error("Error:", error));
}

// Utility function to add event listeners for press and release
function addButtonEvents(buttonId, actionOnPress, actionOnRelease) {
    const button = document.getElementById(buttonId);
    
    button.addEventListener("pointerdown", (event) => {
        event.preventDefault(); // Prevent unwanted behaviors on touch
        sendAction(actionOnPress);
    });

    button.addEventListener("pointerup", () => {
        sendAction(actionOnRelease);
    });

    // Handle pointer cancel (e.g., dragging finger off the button)
    button.addEventListener("pointercancel", () => {
        sendAction(actionOnRelease);
    });
}

// Add events for each button
addButtonEvents("upBtn", "u", "s");
addButtonEvents("downBtn", "d", "s");
addButtonEvents("tiltUpBtn", "tu", "s");
addButtonEvents("tiltDownBtn", "td", "s");
