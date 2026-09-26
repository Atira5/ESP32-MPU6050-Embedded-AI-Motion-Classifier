#include <Wire.h>

#define MPU6050_ADDR 0x68
#define ACCEL_XOUT_H 0x3B

#define SDA_PIN 21
#define SCL_PIN 22

void setup()
{
    Serial.begin(115200);

    Wire.begin(
        SDA_PIN,
        SCL_PIN
    );

    // Wake up MPU6050
    Wire.beginTransmission(MPU6050_ADDR);

    Wire.write(0x6B);
    Wire.write(0x00);

    Wire.endTransmission();

    delay(100);

    Serial.println("Ax,Ay,Az");
}


void loop()
{
    int16_t rawAx;
    int16_t rawAy;
    int16_t rawAz;


    // Request accelerometer data
    Wire.beginTransmission(MPU6050_ADDR);

    Wire.write(ACCEL_XOUT_H);

    Wire.endTransmission(false);


    uint8_t bytesRead =
        Wire.requestFrom(
            MPU6050_ADDR,
            6,
            true
        );


    if (bytesRead != 6)
    {
        delay(100);

        return;
    }


    // Read X
    rawAx =
        (Wire.read() << 8) |
        Wire.read();


    // Read Y
    rawAy =
        (Wire.read() << 8) |
        Wire.read();


    // Read Z
    rawAz =
        (Wire.read() << 8) |
        Wire.read();


    // MPU6050 default ±2g
    float Ax_g =
        rawAx / 16384.0f;

    float Ay_g =
        rawAy / 16384.0f;

    float Az_g =
        rawAz / 16384.0f;


    // Convert g → m/s²
    float Ax =
        Ax_g * 9.81f;

    float Ay =
        Ay_g * 9.81f;

    float Az =
        Az_g * 9.81f;


    // Send CSV
    Serial.print(Ax, 2);
    Serial.print(",");

    Serial.print(Ay, 2);
    Serial.print(",");

    Serial.println(Az, 2);


    delay(100);
}