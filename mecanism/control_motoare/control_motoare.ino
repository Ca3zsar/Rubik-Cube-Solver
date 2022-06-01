#include <Stepper.h>

const int stepsPerRevolution = 200;
const byte numChars = 200;
char receivedChars[numChars];   // an array to store the received data

boolean newData = false;
int moves[100];
int numberOfMoves = 0;

Stepper *steppers[6];
String command;
int int_comm;

void setStepperIdle(int motor) {
  int start = 22;
  digitalWrite(start + motor*4, LOW);
  digitalWrite(start + motor*4 + 1, LOW);
  digitalWrite(start + motor*4 + 2, LOW);
  digitalWrite(start + motor*4 + 3, LOW);
}

void setup() {
  Serial.begin(9600);
  Serial.println("Begin configuring motors");

  int start = 22;
//  for(int i=0;i<6;i++)
//  {
//    steppers[i] = new Stepper(stepsPerRevolution, start + i*4, start + i*4 + 1, start + i*4 + 2, start + i*4 + 3);
//    steppers[i]->setSpeed(20);
//  }
}

void loop() {
    numberOfMoves = 0;
    recvWithEndMarker();
    parseData();
//    if(numberOfMoves)
//    {
//      solveCube();   
//    }
}

void solveCube()
{
  for(int i = 0 ; i < numberOfMoves; i++)
  {
    int command = moves[i];
    if(command < 18 && command >= 0 )
    {
      int face = command / 3;
      int turns = command % 3;
      int steps = 0;
      switch(turns)
      {
        case 0: steps = stepsPerRevolution / 4;break;
        case 1: steps = stepsPerRevolution / 2;break;
        case 2: steps = -stepsPerRevolution / 4;break;
        default : break;
      }
      steppers[face]->step(steps);
      setStepperIdle(face);
    }
  }
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

void parseData() {
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
