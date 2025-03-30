// Get the local IP automatically
const serverIP = window.location.hostname;
const socket = io(`http://${serverIP}:3000`);

// Listen for actions from the server
socket.on("action", (action) => {
    document.getElementById("actionDisplay").innerText = `Action: ${action}`;
});

// Function to send button action to the server (up, down, tilt)
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

// Function to send the numerical inputs to the server only when 'Send Inputs' is pressed
function sendInputs() {
    const input1 = document.getElementById("input1").value;
    const input2 = document.getElementById("input2").value;
    const input3 = document.getElementById("input3").value;
    const input4 = document.getElementById("input4").value;

    // Check if inputs are not empty and are valid numbers
    if (input1 && input2 && input3 && input4) {
        const inputs = {
            input1: parseInt(input1, 10),
            input2: parseInt(input2, 10),
            input3: parseInt(input3, 10),
            input4: parseInt(input4, 10)
        };

        // Send the numerical inputs as a JSON string
        fetch(`http://${serverIP}:3000/send-action`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ action: JSON.stringify(inputs) })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data.message);
            alert('Inputs sent successfully!');
        })
        .catch(error => {
            console.error("Error:", error);
            alert('Error sending inputs.');
        });
    } else {
        alert("Please fill out all the input fields!");
    }
}

// Utility function to add event listeners for press and release
function addButtonEvents(buttonId, actionOnPress, actionOnRelease) {
    const button = document.getElementById(buttonId);

    button.addEventListener("pointerdown", (event) => {
        event.preventDefault(); // Prevent unwanted behaviors on touch
        sendAction(actionOnPress); // Send only action related to the button
    });

    button.addEventListener("pointerup", () => {
        sendAction(actionOnRelease); // Send action when button is released
    });

    // Handle pointer cancel (e.g., dragging finger off the button)
    button.addEventListener("pointercancel", () => {
        sendAction(actionOnRelease); // Send action when pointer is cancelled
    });
}

// Add events for each button (up, down, tilt)
addButtonEvents("upBtn", "u", "s"); // 'u' for up, 's' for stop
addButtonEvents("downBtn", "d", "s"); // 'd' for down, 's' for stop
addButtonEvents("tiltUpBtn", "tu", "s"); // 'tu' for tilt up, 's' for stop
addButtonEvents("tiltDownBtn", "td", "s"); // 'td' for tilt down, 's' for stop

// Add event listener to Send Inputs button
document.getElementById("sendInputsBtn").addEventListener("click", sendInputs);

console.log(`Connecting to server at http://${serverIP}:3000`);
