#include <Wire.h>
#include <math.h>

#include "model_data.h"


// ============================================================
// MPU6050
// ============================================================

#define MPU6050_ADDR 0x68
#define ACCEL_XOUT_H 0x3B

#define SDA_PIN 21
#define SCL_PIN 22


// ============================================================
// OUTPUT
// ============================================================

#define LED_PIN 2


// ============================================================
// TIMING
// ============================================================

unsigned long lastInference = 0;

const unsigned long INFERENCE_INTERVAL = 100;


// ============================================================
// RELU
// ============================================================

float relu(
    float value
)
{
    if (value > 0.0f)
    {
        return value;
    }

    return 0.0f;
}


// ============================================================
// SIGMOID
// ============================================================

float sigmoid(
    float value
)
{
    return 1.0f /
           (
               1.0f +
               expf(-value)
           );
}


// ============================================================
// READ MPU6050
// ============================================================

bool readAccelerometer(
    float &Ax,
    float &Ay,
    float &Az
)
{
    Wire.beginTransmission(
        MPU6050_ADDR
    );

    Wire.write(
        ACCEL_XOUT_H
    );

    Wire.endTransmission(false);


    uint8_t bytesRead =
        Wire.requestFrom(
            MPU6050_ADDR,
            6,
            true
        );


    if (bytesRead != 6)
    {
        return false;
    }


    int16_t rawAx =
        (Wire.read() << 8) |
        Wire.read();


    int16_t rawAy =
        (Wire.read() << 8) |
        Wire.read();


    int16_t rawAz =
        (Wire.read() << 8) |
        Wire.read();


    // MPU6050 default:
    // ±2g → 16384 LSB/g

    float Ax_g =
        rawAx / 16384.0f;

    float Ay_g =
        rawAy / 16384.0f;

    float Az_g =
        rawAz / 16384.0f;


    // Convert g → m/s²

    Ax =
        Ax_g * 9.81f;

    Ay =
        Ay_g * 9.81f;

    Az =
        Az_g * 9.81f;


    return true;
}


// ============================================================
// RUN NEURAL NETWORK
// ============================================================

int runNeuralNetwork(
    float Ax,
    float Ay,
    float Az,
    float &confidence
)
{
    float input[3];

    // -----------------------------------------------
    // StandardScaler
    // -----------------------------------------------

    input[0] =
        (
            Ax -
            INPUT_MEAN[0]
        )
        /
        INPUT_SCALE[0];


    input[1] =
        (
            Ay -
            INPUT_MEAN[1]
        )
        /
        INPUT_SCALE[1];


    input[2] =
        (
            Az -
            INPUT_MEAN[2]
        )
        /
        INPUT_SCALE[2];


    // -----------------------------------------------
    // Hidden layer
    // -----------------------------------------------

    float hidden[
        MODEL_HIDDEN_SIZE
    ];


    for (
        int j = 0;
        j < MODEL_HIDDEN_SIZE;
        j++
    )
    {
        float sum =
            BIAS_HIDDEN[j];


        for (
            int i = 0;
            i < MODEL_INPUT_SIZE;
            i++
        )
        {
            sum +=
                input[i] *
                WEIGHTS_INPUT_HIDDEN[i][j];
        }


        // ReLU
        hidden[j] =
            relu(sum);
    }


    // -----------------------------------------------
    // Output layer
    // -----------------------------------------------

    float output =
        BIAS_OUTPUT;


    for (
        int j = 0;
        j < MODEL_HIDDEN_SIZE;
        j++
    )
    {
        output +=
            hidden[j] *
            WEIGHTS_HIDDEN_OUTPUT[j];
    }


    // -----------------------------------------------
    // Sigmoid
    // -----------------------------------------------

    float probability =
        sigmoid(output);


    // Scikit-learn binary MLP:
    //
    // probability >= 0.5
    // → class 1
    //
    // probability < 0.5
    // → class 0

    int predictedClass;


    if (probability >= 0.5f)
    {
        predictedClass = 1;

        confidence =
            probability;
    }
    else
    {
        predictedClass = 0;

        confidence =
            1.0f -
            probability;
    }


    return predictedClass;
}


// ============================================================
// SETUP
// ============================================================

void setup()
{
    Serial.begin(
        115200
    );


    // I2C
    Wire.begin(
        SDA_PIN,
        SCL_PIN
    );


    // Wake up MPU6050

    Wire.beginTransmission(
        MPU6050_ADDR
    );

    Wire.write(
        0x6B
    );

    Wire.write(
        0x00
    );

    Wire.endTransmission();


    delay(100);


    // LED
    pinMode(
        LED_PIN,
        OUTPUT
    );

    digitalWrite(
        LED_PIN,
        LOW
    );


    Serial.println();
    Serial.println(
        "======================================"
    );

    Serial.println(
        "      ESP32 EMBEDDED AI"
    );

    Serial.println(
        "      MPU6050 MOTION CLASSIFIER"
    );

    Serial.println(
        "======================================"
    );

    Serial.println();

    Serial.print(
        "Class 0: "
    );

    Serial.println(
        CLASS_0
    );


    Serial.print(
        "Class 1: "
    );

    Serial.println(
        CLASS_1
    );


    Serial.println();

    Serial.println(
        "AI inference running on ESP32..."
    );

    Serial.println();
}


// ============================================================
// LOOP
// ============================================================

void loop()
{
    if (
        millis() -
        lastInference <
        INFERENCE_INTERVAL
    )
    {
        return;
    }


    lastInference =
        millis();


    float Ax;
    float Ay;
    float Az;


    // -----------------------------------------------
    // Read sensor
    // -----------------------------------------------

    if (
        !readAccelerometer(
            Ax,
            Ay,
            Az
        )
    )
    {
        Serial.println(
            "MPU6050 read error"
        );

        return;
    }


    // -----------------------------------------------
    // AI inference
    // -----------------------------------------------

    float confidence = 0.0f;


    int prediction =
        runNeuralNetwork(
            Ax,
            Ay,
            Az,
            confidence
        );


    const char* label;


    if (prediction == 0)
    {
        label = CLASS_0;
    }
    else
    {
        label = CLASS_1;
    }


    // -----------------------------------------------
    // LED
    //
    // Moving = LED ON
    // Still  = LED OFF
    //
    // Change this logic if needed.
    // -----------------------------------------------

    if (
        prediction == 0
    )
    {
        digitalWrite(
            LED_PIN,
            LOW
        );
    }
    else
    {
        digitalWrite(
            LED_PIN,
            HIGH
        );
    }


    // -----------------------------------------------
    // Serial output
    // -----------------------------------------------

    Serial.print(
        "Ax="
    );

    Serial.print(
        Ax,
        2
    );


    Serial.print(
        "  Ay="
    );

    Serial.print(
        Ay,
        2
    );


    Serial.print(
        "  Az="
    );

    Serial.print(
        Az,
        2
    );


    Serial.print(
        "  -> "
    );

    Serial.print(
        label
    );


    Serial.print(
        "  Confidence="
    );

    Serial.print(
        confidence * 100.0f,
        1
    );

    Serial.println(
        "%"
    );
}