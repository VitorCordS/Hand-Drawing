#include <Servo.h>
#define numOfValsRec 5
#define digitsPerValRec 1

Servo servoThumb;
Servo servoIndex;
Servo servoMiddle;
Servo servoRing;
Servo servoPinky;

int valsRec[numOfValsRec];
int stringLength = numOfValsRec * digitsPerValRec + 1; // Including the `$`
int counter = 0;
bool countStart = false;
String receivedString;

void setup() {
  Serial.begin(9600);
  servoThumb.attach(6);
  servoIndex.attach(5);
  servoMiddle.attach(4);
  servoRing.attach(3);
  servoPinky.attach(2);
}

void receiveData() {
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '$') {
      countStart = true;
      receivedString = ""; // Clear previous data
      counter = 0; // Reset counter
    }
    
    if (countStart) {
      if (counter < stringLength) {
        receivedString += c; // Append the incoming character
        counter++;
      }

      if (counter >= stringLength) {
        // Once the full string is received, process it
        for (int i = 0; i < numOfValsRec; i++) {
          int num = (i * digitsPerValRec) + 1; // +1 to skip the '$'
          valsRec[i] = receivedString.substring(num, num + digitsPerValRec).toInt();
        }

        receivedString = ""; // Clear the string after processing
        counter = 0;
        countStart = false; // Reset to stop processing until the next '$'
      }
    }
  }
}

void loop() {
  receiveData();

  // Move the servos based on the received values
  if (valsRec[0] == 0) { servoThumb.write(180); } else { servoThumb.write(0); }
  if (valsRec[1] == 0) { servoIndex.write(180); } else { servoIndex.write(0); }
  if (valsRec[2] == 0) { servoMiddle.write(180); } else { servoMiddle.write(0); }
  if (valsRec[3] == 0) { servoRing.write(180);} else { servoRing.write(0);}
  if (valsRec[4] == 0) { servoPinky.write(180); } else { servoPinky.write(0); }
}
