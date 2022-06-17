#include <Stepper.h>

const int stepsPerRevolution = 200;
const byte numChars = 2000;
char receivedChars[numChars];   // an array to store the received data

boolean newData = false;
int moves[400];
int numberOfMoves = 0;

int faces[] = {0, 4, 5, 2 , 1, 3  };

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

  int start = 22;
  for(int i=0;i<6;i++)
  {
    steppers[i] = new Stepper(stepsPerRevolution, start + i*4, start + i*4 + 1, start + i*4 + 2, start + i*4 + 3);
    steppers[i]->setSpeed(80);
    steppers[i]->step(0);
  }
}

void loop() {
    numberOfMoves = 0;
    recvWithEndMarker();
    parseData();
    if(numberOfMoves)
    {
      solveCube();   
    }
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
      int sign = turns == 2?1:-1;
      switch(turns)
      {
        case 0: steps =-  stepsPerRevolution / 4 ;break;
        case 1: steps = - stepsPerRevolution / 2 ;break;
        case 2: steps = stepsPerRevolution / 4 ;break;
        default : break;
      }
//      steppers[faces[face]]->step(1);
//      steppers[faces[face]]->step(-1);
//      delay(100);
//      if(face == 4)
//      {
//          steps = steps + sign * 1;
//      }
      if(turns == 2)
      {
        steppers[faces[face]]->step(-steps);
        steppers[faces[face]]->step(-steps);
        steppers[faces[face]]->step(-steps - sign * 4);
      }else{
        steppers[faces[face]]->step(steps + sign * 4);
      }
      setStepperIdle(faces[face]);
//      delay(2500);
    }
  }
  Serial.print("done");
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
        while (pch != NULL)
        {
          pch = strtok (NULL, " ,.-");
          if(pch != NULL){
            moves[numberOfMoves++] = atoi(pch);
          }
        }
        newData = false;
    }
}
