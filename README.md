# **Smart Learning Table For Classrooms**

## **Members**
- Rami Kronbi
- Bassam Kousa
- Ali Daaboul
- Mohamad Berjawi
- Mohamad Hariri

## **Project Resources**
Check the following link to access the resouces and reports used in this project.

[Project Resources](https://drive.google.com/drive/folders/1InH4OToC-3ZCmpd2p8zu-zYlxD98OoeB?usp=drive_link)

# Smart Interactive Desk

An interactive, dynamic, and intelligent desk that merges hardware control, computer vision, and ergonomic assistance into a single integrated system.

---

## 🧑‍💻 Public Overview

### What is Smart Interactive Desk?

The **Smart Interactive Desk** is an IoT-enabled, height-adjustable workstation designed to bring interactive learning and ergonomic benefits to classrooms, offices, and homes.  
It combines sensors, motors, and smart software to allow users to control and monitor the desk via multiple interfaces (web app, game controller, etc.).

By adjusting to user needs and promoting healthy movement, the desk aims to improve engagement, well-being, and posture during long hours of work or study.

#### 📚 Why It Matters
Studies show that adjustable desks and posture-monitoring can:
- Reduce back pain
- Improve concentration
- Encourage healthy movement habits  
*(Sources: [matellio.com](https://www.matellio.com) | [healthline.com](https://www.healthline.com))*

---

### 🎥 Demo / Preview (Concept)

> **Note**: No real product images yet — these stock illustrations demonstrate the vision of an interactive, sensor-equipped smart desk.

- **Image 1**: A modern, smart workstation with adjustable height and integrated computer interfaces.
- **Image 2**: An imagined setup showing screens, sensors, and ergonomic controls on a desk surface.

---

### ✨ Features

- **Motorized Height and Tilt**:  
  Adjust desk surface for sitting or standing with motorized actuators.

- **Posture Monitoring**:  
  Real-time feedback using computer vision and/or ultrasonic sensors.

- **Interactive Controls**:  
  Web-based dashboard + Bluetooth PS4 controller support.

- **Visual Feedback**:  
  LCD or LED indicators display desk status, timers, or posture alerts.

- **Computer Vision Capability**:  
  OpenCV-based vision algorithms track posture, movement, or interaction.

- **Data Logging and Analysis**:  
  Usage stats and posture data can be collected for insight.

- **Connectivity**:  
  ESP32 microcontroller linked to a host computer via Serial or MQTT.

---

## 🧑‍💻 Developer Section

### 🚀 Getting Started

#### Clone the Repository
```bash
git clone https://github.com/Kronbii/smart-interactive-desk.git
cd smart-interactive-desk
```

#### Install requirements
```bash
pip install -r requirements.txt
```
```bash
cd model/web-app
npm install
```
### Repository Structure
```bash
Directory | Status | Description
model/ | ✅ Final Model | Only this should be used for production.
test/ | ❌ Deprecated | Experimental testing modules (to be ignored).
koubeissicly/ | ❌ Deprecated | Early architecture drafts (to be ignored).
stable/ | ❌ Deprecated | Older stable version (before model/ finalization).
```