<div align="center">

🧠 ESP32 + MPU6050 Embedded AI Motion Classifier

🎯 Real-Time STILL / MOVING Classification on ESP32

<img src="https://img.shields.io/badge/Embedded%20AI-ESP32-6f42c1?style=for-the-badge&logo=espressif&logoColor=white">
<img src="https://img.shields.io/badge/Sensor-MPU6050-00a67d?style=for-the-badge">
<img src="https://img.shields.io/badge/ML-Scikit--Learn-f7931e?style=for-the-badge&logo=scikit-learn&logoColor=white">
<img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white">
<img src="https://img.shields.io/badge/C%2FC%2B%2B-ESP32-00599C?style=for-the-badge&logo=cplusplus&logoColor=white">

<br><br>

Sensor → Data Collection → Machine Learning → Model Deployment → Embedded AI → Real-Time Prediction

<br>

A practical Embedded AI project where a trained neural network runs directly on an ESP32 to classify MPU6050 motion as STILL or MOVING.

</div>

🌟 Project Overview

This project combines an ESP32, MPU6050 accelerometer, and a lightweight Neural Network to create a real-time Embedded AI motion classifier.

The system learns from acceleration data and classifies the sensor state into:

🟢 STILL

🔵 MOVING

The Machine Learning model is trained on a computer using Python. The trained model parameters are then exported into C/C++ and deployed directly to the ESP32.

The final AI inference happens on the ESP32 itself.

🎯 Project Objective

The goal of this project is to demonstrate the complete Embedded AI workflow:

             🌍 PHYSICAL WORLD
                    │
                    ▼
              ┌──────────┐
              │ MPU6050  │
              └────┬─────┘
                   │
                  I²C
                   │
                   ▼
              ┌──────────┐
              │  ESP32   │
              └────┬─────┘
                   │
                   ▼
             Sensor Data
                   │
                   ▼
              📄 Dataset
                   │
                   ▼
          🧠 ML Model Training
                   │
                   ▼
           📦 Model Parameters
                   │
                   ▼
                ESP32
                   │
                   ▼
          ⚡ AI Inference
                   │
             ┌─────┴─────┐
             ▼           ▼
          🟢 STILL    🔵 MOVING
             │           │
             ▼           ▼
          💡 LED ON    💡 LED OFF

✨ Key Features

Feature

Description

🧠 Embedded AI

AI inference runs directly on the ESP32

📡 Motion Sensing

MPU6050 provides real-time acceleration data

🔌 I²C Communication

ESP32 communicates with MPU6050 through I²C

🐍 Python ML Pipeline

Dataset creation and model training

🤖 Neural Network

Lightweight MLP classifier

⚡ Real-Time Inference

Continuous prediction on ESP32

💡 Physical Output

LED indicates the AI result

☁️ No Cloud

Final prediction does not require cloud services

💻 No PC for Inference

ESP32 can operate independently after deployment

🔥 Why Is This an Embedded AI Project?

The important question is:

Where is the AI model running?

❌ Traditional PC-Based Machine Learning

MPU6050
   ↓
ESP32
   ↓
USB Serial
   ↓
Python
   ↓
ML Model
   ↓
Prediction

In this architecture, the computer performs the inference.

✅ This Project — Embedded AI

MPU6050
   ↓
ESP32
   ↓
Embedded Neural Network
   ↓
Prediction
   ↓
LED

The AI model is running directly on the ESP32.

The computer is only required during development for:

📊 Dataset Collection
        +
🧠 Model Training
        +
📦 Model Export

After deployment:

MPU6050
   ↓
ESP32
   ↓
AI Model
   ↓
Prediction
   ↓
LED

No Python application is required for the final inference.

🛠️ Hardware Requirements

Component

Purpose

🟦 ESP32

Embedded controller and AI inference

🟩 MPU6050

Motion/acceleration sensor

💡 LED

Visual indication of prediction

🔌 USB Cable

Programming and serial monitoring

🔗 Jumper Wires

Hardware connections

🔌 Circuit Connections

MPU6050 → ESP32

The MPU6050 uses the I²C protocol.

MPU6050

ESP32

VCC

3.3V

GND

GND

SDA

GPIO 21

SCL

GPIO 22

              ┌───────────────┐
              │    MPU6050    │
              │               │
       3.3V ──┤ VCC           │
       GND  ──┤ GND           │
       SDA  ──┤ SDA           │
       SCL  ──┤ SCL           │
              └───────┬───────┘
                      │
                      │ I²C
                      │
              ┌───────▼───────┐
              │     ESP32     │
              │               │
              │ GPIO 21 = SDA │
              │ GPIO 22 = SCL │
              └───────────────┘

LED

The current firmware uses:

GPIO 2

for the LED output.

For an external LED:

ESP32 GPIO 2
      │
      ▼
  Resistor
      │
      ▼
     LED
      │
      ▼
     GND

📡 MPU6050 Sensor

The MPU6050 provides:

Accelerometer

Ax
Ay
Az

Gyroscope

Gx
Gy
Gz

The current project uses:

Ax
Ay
Az

as Machine Learning input features.

📊 Sensor Data

The MPU6050 produces numerical measurements rather than directly telling us whether the sensor is still or moving.

Example:

Ax       Ay       Az
-------------------------
0.12     0.04     9.71
0.18     0.07     9.65
0.31    -0.02     9.81

When the sensor moves, the acceleration pattern changes.

The neural network learns these patterns and predicts:

STILL

or:

MOVING

🧩 Complete AI Pipeline

             📡 MPU6050
                  │
                  ▼
               ESP32
                  │
                  ▼
          📥 Data Collection
                  │
                  ▼
              📄 CSV
                  │
                  ▼
         🏷️ Features + Labels
                  │
                  ▼
          📏 Feature Scaling
                  │
                  ▼
          🧠 Model Training
                  │
                  ▼
           🤖 Trained Model
                  │
                  ▼
          📦 Model Export
                  │
                  ▼
                ESP32
                  │
                  ▼
          ⚡ AI Inference
                  │
          ┌───────┴───────┐
          ▼               ▼
       🟢 STILL        🔵 MOVING
          │               │
          ▼               ▼
       💡 LED ON       💡 LED OFF

📁 Project Structure

mpu6050-embedded-ai/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── dataset/
│   └── mpu6050_dataset.csv
│
├── model/
│   ├── mlp_model.pkl
│   └── scaler.pkl
│
├── python/
│   ├── collect_dataset.py
│   └── train_model.py
│
└── arduino/
    │
    ├── sensor_stream/
    │   └── sensor_stream.ino
    │
    └── embedded_ai/
        ├── embedded_ai.ino
        └── model_data.h

💻 Software Requirements

Development Tools

Arduino IDE

ESP32 Board Package

Python 3.x

VS Code

Python Libraries

pyserial
pandas
numpy
scikit-learn
joblib

Install all dependencies:

pip install -r requirements.txt

Or manually:

pip install pyserial pandas numpy scikit-learn joblib

🚀 Getting Started

1️⃣ Clone the Repository

git clone https://github.com/YOUR_USERNAME/mpu6050-embedded-ai.git
cd mpu6050-embedded-ai

2️⃣ Install Dependencies

pip install -r requirements.txt

3️⃣ Connect the Hardware

Connect:

MPU6050 → ESP32

VCC → 3.3V
GND → GND
SDA → GPIO 21
SCL → GPIO 22

4️⃣ Upload Sensor Streaming Firmware

Open:

arduino/sensor_stream/sensor_stream.ino

Upload it to the ESP32.

This firmware is used for collecting training data.

The ESP32 sends:

Ax,Ay,Az

through Serial.

Serial Settings

Baud Rate: 115200

5️⃣ Collect the Dataset

Open:

python/collect_dataset.py

Change the COM port:

PORT = "COM14"

For example:

PORT = "COM5"

Run:

python python/collect_dataset.py

Select:

1 - Still
2 - Moving

Collect samples for both classes.

The dataset is saved to:

dataset/mpu6050_dataset.csv

📄 Dataset Format

The CSV contains:

Ax,Ay,Az,Label

Example:

0.12,0.04,9.71,Still
0.18,0.07,9.65,Still
2.51,-1.34,7.83,Moving
4.20,2.11,6.52,Moving

Features

Ax
Ay
Az

Labels

Still
Moving

6️⃣ Train the Neural Network

Run:

python python/train_model.py

The training process is:

Load Dataset
     ↓
Extract Features
     ↓
Extract Labels
     ↓
Train/Test Split
     ↓
StandardScaler
     ↓
MLP Neural Network
     ↓
Training
     ↓
Evaluation
     ↓
Save Model
     ↓
Generate model_data.h

The script generates:

model/
├── mlp_model.pkl
└── scaler.pkl

and:

arduino/embedded_ai/model_data.h

🤖 Neural Network Architecture

The project uses a small Multi-Layer Perceptron (MLP).

              INPUT
                │
        ┌───────┼───────┐
        │       │       │
       Ax      Ay      Az
        │       │       │
        └───────┼───────┘
                │
                ▼
       ┌─────────────────┐
       │ Hidden Layer    │
       │ 8 Neurons       │
       │ ReLU Activation │
       └────────┬────────┘
                │
                ▼
       ┌─────────────────┐
       │ Output Layer    │
       │ Binary Class    │
       └────────┬────────┘
                │
                ▼
          STILL / MOVING

Model Configuration

Parameter

Value

Input features

3

Input

Ax, Ay, Az

Hidden layer

8 neurons

Activation

ReLU

Task

Binary Classification

Classes

Still, Moving

Preprocessing

StandardScaler

📏 Feature Scaling

The sensor values are standardized before entering the neural network.

Training

Raw Sensor Data
       ↓
StandardScaler
       ↓
Scaled Data
       ↓
Neural Network

Inference

New Sensor Data
       ↓
Same Scaling Parameters
       ↓
Neural Network
       ↓
Prediction

The same scaling parameters used during training are embedded into the ESP32.

📦 Model Deployment

After training, train_model.py automatically creates:

arduino/embedded_ai/model_data.h

The generated header contains:

🧮 Neural Network Weights
🧮 Bias Values
📏 Scaling Parameters
🏷️ Class Names

The deployment process is:

Python Model
     ↓
Weights + Biases
     ↓
C++ Header
     ↓
ESP32 Firmware

🚀 Deploy AI to ESP32

Open:

arduino/embedded_ai/embedded_ai.ino

Make sure:

embedded_ai/
├── embedded_ai.ino
└── model_data.h

Then upload the firmware to the ESP32.

⚡ On-Device AI Inference

After uploading the final firmware, the ESP32 performs:

MPU6050
   ↓
Sensor Reading
   ↓
Feature Scaling
   ↓
Neural Network
   ↓
Prediction

Everything happens directly on the ESP32.

Example — STILL

Ax=0.21
Ay=-0.10
Az=9.72

        ↓

Prediction: STILL
Confidence: 98.5%

        ↓

LED ON

Example — MOVING

Ax=4.12
Ay=2.53
Az=6.81

        ↓

Prediction: MOVING
Confidence: 96.8%

        ↓

LED OFF

💡 LED Behavior

AI Prediction

LED

🟢 STILL

💡 ON

🔵 MOVING

💡 OFF

This provides a simple physical output from the AI model.

🔍 Serial Monitor

Open Arduino Serial Monitor at:

115200 baud

Initial output:

======================================
      ESP32 EMBEDDED AI
      MPU6050 MOTION CLASSIFIER
======================================

Class 0: Moving
Class 1: Still

AI inference running on ESP32...

Example:

Ax=0.21  Ay=-0.10  Az=9.72
-> Still
Confidence=98.5%

When the sensor is moved:

Ax=4.12  Ay=2.53  Az=6.81
-> Moving
Confidence=96.8%

🆚 Before vs After

❌ PC-Based Inference

MPU6050
   ↓
ESP32
   ↓
USB Serial
   ↓
Python
   ↓
ML Model
   ↓
Prediction

The PC performs the prediction.

✅ Embedded AI

MPU6050
   ↓
ESP32
   ↓
Embedded Neural Network
   ↓
Prediction
   ↓
LED

The ESP32 performs the prediction locally.

🌐 Does the Final System Need Internet?

Internet

❌ Not required

Python

❌ Not required for final inference

Cloud

❌ Not required

PC

❌ Not required after deployment

The ESP32 can perform the deployed AI model locally.

🧠 Training vs Inference

🏋️ Training

The computer handles:

Dataset
   ↓
Preprocessing
   ↓
Model Training
   ↓
Model Evaluation
   ↓
Model Export

⚡ Inference

The ESP32 handles:

Sensor
   ↓
Preprocessing
   ↓
Neural Network
   ↓
Prediction

Simple explanation

The computer teaches the model. The ESP32 uses what it learned.

📚 Concepts Demonstrated

🔌 Embedded Systems

ESP32

GPIO

I²C

Serial communication

Sensor interfacing

Real-time processing

📊 Sensor Data

Accelerometer

Sensor readings

Sampling

Data collection

CSV datasets

🧠 Machine Learning

Features

Labels

Classification

Training

Testing

Standardization

Neural networks

Inference

🤖 Embedded AI

Model deployment

On-device inference

Local decision making

Resource-constrained AI

Sensor-based intelligence

📈 Model Performance

Model performance depends on the quality and diversity of the dataset.

It can be affected by:

Sensor orientation

Number of samples

Movement style

Sensor placement

Noise

Dataset balance

Training/test split

A high test accuracy does not guarantee perfect performance for every real-world movement.

For better generalization, collect data from different orientations and movement patterns.

🚀 Future Improvements

1. 🧩 Add More Motion Classes

STILL
MOVING
SHAKE
TILT

or:

STILL
WALKING
RUNNING
FALL

2. 📦 Use All Six MPU6050 Channels

Current:

Ax
Ay
Az

Future:

Ax
Ay
Az
Gx
Gy
Gz

3. ⏱️ Use a Sensor Window

Instead of one reading:

Ax Ay Az

use a sequence:

Sample 1
Sample 2
Sample 3
...
Sample 100

Then:

100 Samples
      ↓
Motion Pattern
      ↓
AI Model
      ↓
Prediction

This can provide better motion recognition.

4. 🔊 Add a Buzzer

MOVING
   ↓
Buzzer ON

5. ⚙️ Add a Servo

STILL  → Servo Position 1
MOVING → Servo Position 2

6. 📱 Add Wireless Communication

The ESP32 can send predictions using:

Wi-Fi

Bluetooth

MQTT

while keeping inference local.

7. 🧠 Explore TensorFlow Lite Micro

A future version can replace the custom C/C++ neural-network implementation with a standard TinyML framework such as TensorFlow Lite for Microcontrollers.

Possible architecture:

Python / TensorFlow
        ↓
Model Training
        ↓
TFLite Conversion
        ↓
Quantization
        ↓
TensorFlow Lite Micro
        ↓
ESP32
        ↓
On-Device Inference

🎓 Learning Outcome

This project demonstrates the complete path from sensor data to intelligent embedded decision-making:

🌍 Physical World
        ↓
📡 Sensor
        ↓
📊 Sensor Data
        ↓
📄 Dataset
        ↓
🏷️ Features + Labels
        ↓
🧠 ML Training
        ↓
🤖 Neural Network
        ↓
📦 Model Deployment
        ↓
🔌 ESP32
        ↓
⚡ Embedded AI Inference
        ↓
🎯 Prediction
        ↓
💡 Physical Output

🧰 Technologies Used

Technology

Purpose

🟦 ESP32

Embedded controller + AI inference

🟩 MPU6050

Motion sensing

🔵 I²C

Sensor communication

🟨 Arduino IDE

ESP32 firmware

🐍 Python

Data collection + ML training

🐼 Pandas

Dataset processing

🔢 NumPy

Numerical processing

🤖 Scikit-learn

Machine Learning

🧠 MLPClassifier

Neural Network

📦 Joblib

Model storage

💻 C/C++

On-device inference

📋 Quick Start

# 1. Install dependencies
pip install -r requirements.txt

# 2. Collect dataset
python python/collect_dataset.py

# 3. Train model
python python/train_model.py

Then upload:

arduino/embedded_ai/embedded_ai.ino

to the ESP32.

Open Serial Monitor:

115200

Test:

🟢 STILL  → LED ON
🔵 MOVING → LED OFF

🗂️ Important Files

File

Purpose

collect_dataset.py

Collect labeled MPU6050 data

train_model.py

Train the neural network

sensor_stream.ino

Stream sensor data

embedded_ai.ino

Final Embedded AI firmware

model_data.h

Embedded neural-network parameters

mpu6050_dataset.csv

Training dataset

mlp_model.pkl

Python-side trained model

scaler.pkl

Scaling parameters

⚠️ Important Notes

Change the COM port before collecting data.

Use 115200 baud.

Close Arduino Serial Monitor before running the Python collector.

Keep model_data.h in the same directory as embedded_ai.ino.

Regenerate model_data.h whenever you retrain the model.

Retrain the model after significantly changing the dataset.

Real-world accuracy depends strongly on dataset quality.

🌱 Project Evolution

This project demonstrates the progression from basic embedded programming to Embedded AI:

LEVEL 1
Sensor Reading
      ↓
ESP32
      ↓

LEVEL 2
Data Collection
      ↓
CSV Dataset
      ↓

LEVEL 3
Machine Learning
      ↓
PC Training
      ↓

LEVEL 4
Model Export
      ↓
C / C++
      ↓

LEVEL 5
Embedded AI
      ↓
ESP32 Inference
      ↓
AI Decision

⭐ Project Highlights

✔ ESP32 + MPU6050
✔ Real sensor data
✔ Machine Learning
✔ Neural Network
✔ Model deployment
✔ On-device inference
✔ Local decision making
✔ No cloud required for prediction
✔ Real-time physical output

👩‍💻 Author

<div align="center">

Athira B

Embedded Systems • Embedded AI • IoT • Machine Learning

</div>

📜 License

This project is created for educational and learning purposes.

Add your preferred open-source license to this repository.

<div align="center">

🚀 Build. Train. Deploy. Predict.

🧠 From Sensor Data to Embedded AI.

⭐ If you found this project useful, consider giving the repository a star!

</div>
