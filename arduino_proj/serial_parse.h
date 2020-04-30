#include "constants.h"

// message size
const byte numChars = 32;
char receivedChars[numChars];
char tempChars[numChars];        // temporary array for use when parsing
boolean newData = false;

void recvWithStartEndMarkers() {
    static boolean recvInProgress = false;
    static byte ndx = 0;
    char startMarker = '<';
    char endMarker = '>';
    char rc;

    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();
        if (recvInProgress == true) {
            if (rc != endMarker) {
                receivedChars[ndx] = rc;
                ndx++;
                if (ndx >= numChars) {
                    ndx = numChars - 1;
                }
            }
            else {
                receivedChars[ndx] = '\0'; // terminate the string
                recvInProgress = false;
                ndx = 0;
                newData = true;
            }
        }

        else if (rc == startMarker) {
            recvInProgress = true;
        }
    }
}

void parseData(float result[]) {      // split the data into its parts

    char * strtokIndx; // this is used by strtok() as an index
    strtokIndx = strtok(tempChars,",");
    for (int i = 0; i < SIZE_STATE; i++) {
        result[i] = atof(strtokIndx);
        strtokIndx = strtok(NULL, ",");
    }
}

void showParsedData(float result[]) {
    // convenience print
    Serial.print("x-pos ");
    Serial.println(result[0], 6);
    Serial.print("x-vel ");
    Serial.println(result[1], 6);
    Serial.print("pitch ");
    Serial.println(result[2], 6);
    Serial.print("pitch_rate ");
    Serial.println(result[3], 6);
    Serial.println();
}

void getLatestMessage(float result[]) {
    recvWithStartEndMarkers();
    if (newData == true) {
        strcpy(tempChars, receivedChars);
            // this temporary copy is necessary to protect the original data
            //   because strtok() used in parseData() replaces the commas with \0
        parseData(result);
        newData = false;
        // showParsedData(result);
    }
}

void publishControlMessage(float my_float) {
    Serial.print("<@");
    Serial.print(my_float, 4);
    Serial.println(">");
}

