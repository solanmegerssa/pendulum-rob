// Example 5 - Receive with start- and end-markers combined with parsing

const byte numChars = 32;
char receivedChars[numChars];
char tempChars[numChars];        // temporary array for use when parsing


float x_pos = 0.0;
float x_vel = 0.0;
float pitch = 0.0;
float pitch_rate = 0.0;

boolean newData = false;

//============

void setup() {
    Serial.begin(115200);
    Serial.println("This test expects 4 floats");
    Serial.println("Enter data in this style <1.0, 12.0, 24.7, 3.0>  ");
    Serial.println();
}

//============

void loop() {
    recvWithStartEndMarkers();
    if (newData == true) {
        strcpy(tempChars, receivedChars);
            // this temporary copy is necessary to protect the original data
            //   because strtok() used in parseData() replaces the commas with \0
        parseData();
        showParsedData();
        newData = false;
    }
}

//============

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

//============

void parseData() {      // split the data into its parts

    char * strtokIndx; // this is used by strtok() as an index

    strtokIndx = strtok(tempChars,",");
    x_pos = atof(strtokIndx);
 
    strtokIndx = strtok(NULL, ",");
    x_vel = atof(strtokIndx);

    strtokIndx = strtok(NULL, ",");
    pitch = atof(strtokIndx);     // convert this part to a float

    strtokIndx = strtok(NULL, ",");
    pitch_rate = atof(strtokIndx);     // convert this part to a float


}

//============

void showParsedData() {
    Serial.print("x-pos ");
    Serial.println(x_pos);
    Serial.print("x-vel ");
    Serial.println(x_vel);
    Serial.print("pitch ");
    Serial.println(pitch);
    Serial.print("pitch_rate ");
    Serial.println(pitch_rate);
    Serial.println();
}
