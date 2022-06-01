const byte numChars = 200;
char receivedChars[numChars];   // an array to store the received data

boolean newData = false;
int moves[100];
int numberOfMoves = 0;

void setup() {
  Serial.begin(9600);
}

void loop() {
    numberOfMoves = 0;
    recvWithEndMarker();
    showNewData();
}

void recvWithEndMarker() {
    static byte ndx = 0;
    char endMarker = '\n';
    char rc;
    
    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();

        if (rc != endMarker) {
            receivedChars[ndx] = rc;
            ndx++;
            if (ndx >= numChars) {
                ndx = numChars - 1;
            }
        }
        else {
            receivedChars[ndx] = '\0'; // terminate the string
            ndx = 0;
            newData = true;
        }
    }
}

void showNewData() {
    if (newData == true) {
        char * pch;
        pch = strtok (receivedChars," ");
        moves[numberOfMoves++] = atoi(pch);
        Serial.println(pch);
        while (pch != NULL)
        {
          pch = strtok (NULL, " ,.-");
          if(pch != NULL){
            Serial.println(pch);
            moves[numberOfMoves++] = atoi(pch);
          }
        }
        Serial.println(String(numberOfMoves));
        newData = false;
    }
}
