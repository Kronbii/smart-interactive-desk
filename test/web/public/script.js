// Get the local IP automatically
const serverIP = window.location.hostname;
const socket = io(`http://${serverIP}:3000`);

// Listen for actions from the server
socket.on("action", (action) => {
    document.getElementById("actionDisplay").innerText = `Action: ${action}`;
});

// Function to send button action to the server
function sendAction(action) {
    fetch(`http://${serverIP}:3000/send-action`, {
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

// Handle form submission for numerical inputs
document.getElementById("inputsForm").addEventListener("submit", function(event) {
    event.preventDefault();  // Prevent form from reloading the page

    // Get the values from the input fields
    const input1 = document.getElementById("input1").value;
    const input2 = document.getElementById("input2").value;
    const input3 = document.getElementById("input3").value;
    const input4 = document.getElementById("input4").value;

    // Send the inputs to the server
    sendInputs(input1, input2, input3, input4);
});

// Function to send the input values to the server
function sendInputs(input1, input2, input3, input4) {
    fetch(`http://${serverIP}:3000/send-action`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            action: "process_inputs",  // Placeholder action name
            input1: input1,
            input2: input2,
            input3: input3,
            input4: input4
        })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("actionDisplay").innerText = `Inputs sent: ${JSON.stringify(data.response)}`;
    })
    .catch(error => console.error("Error:", error));
}

console.log(`Connecting to server at http://${serverIP}:3000`);
