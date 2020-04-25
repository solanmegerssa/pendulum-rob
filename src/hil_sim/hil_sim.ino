#include "serial_parse.h"

//pieces of data
const int numData = 4; // [x_pos, x_vel, pitch, pitch_rate]
float latestData[numData];

void setup() {
    Serial.begin(115200);
    Serial.println("This test expects 4 floats");
    Serial.println("Enter data in this style <1.0, 12.0, 24.7, 3.0>  ");
    Serial.println();
}

void loop() {
    getLatestMessage(latestData);
}