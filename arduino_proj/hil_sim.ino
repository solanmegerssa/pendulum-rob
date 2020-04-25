#include "serial_parse.h"
// #include "/home/solan/solan/pendulum-rob/arduino_proj/balance_lqr.h"

//pieces of data
float latestData[SIZE_STATE];  // [x_pos, x_vel, pitch, pitch_rate]
float desired_wheel_omega = 0.0;

void setup() {
    Serial.begin(9600);
    Serial.println("This test expects 4 floats");
    Serial.println("Enter data in this style <1.0, 12.0, 24.7, 3.0>  ");
    Serial.println();
}

void loop() {
    getLatestMessage(latestData);
    desired_wheel_omega = computeLQRResponse(latestData);
    publishControlMessage(desired_wheel_omega);
}