#include <Arduino.h>
#include <Stepper.h>
#include <Wire.h>


//INSTRUCTIONS
/*/

1. curl 192.168.137.71/api?command=STEPFORW in command prompt - TRIGGERS FORWARD STEP
2. profit.






/*/





const int stepsPerRevolution = 2048; // How many steps a rev
Stepper myStepper(stepsPerRevolution, 12, 10, 11, 9); // initalise stepper
int stepCount = 0;  // number of steps the motor has taken
// default
const int def_time = 7361; // constant, so  we can reset to the hardcoded default.
float t = 7361; // no longer a constant, this is to allow changing speed in runtime
// faster
//const int t = 3680; // const for time between steps
//fastest
//int t = 1000; // const 

int move = 0; // -1: backwards, 0: stop, 1: forwards

// We do be the arduinoing


// ---------------------------------------------- //
void receiveEvent(int howMany) {
  Serial.println("Receiving data!");
  char c;
  String Store = "";
  while (Wire.available()) { // loop through all but the last
    c = Wire.read(); // receive byte as a character
    //Serial.println(c); - don't need, keep as backup.
    Store.concat(String(c));        // print the character
  }
  Serial.println("Store now equals: "+Store);
  if (Store.endsWith(" --Stepper")){ // Hope to Add multiple args?
    Store.replace(" --Stepper",""); // remove it, this means I can actually ignore args now
    Serial.println("Store: "+Store);
    if (Store == "STEPFORW"){
      Serial.println("STEPPINGFORWARD");
      //sendTrigger(Store);
      move = 1;
    }
    else if (Store == "STEPBACK")
    {
      move = -1;
    }
    
    else if (Store == "STEPSTOP"){
      move = 0;
    }
  
  }
  else if (Store.endsWith(" --Speed")){
    Store.replace(" --Speed","");
    t = def_time * (Store.toFloat()/100);
    Serial.println("SENDING SPEED CHANGE");
    Serial.println("Time per step is now: "+String(t));
  }
  
  else if (Store.endsWith(" --RESET_SPEED")){
    t = def_time; // resets t
  }

  else{
    Serial.println("How did we get here??");
  }
  
}
  




// -------------------------------------- /
long previousMillis = 0;
long interval = 5000;

void setup() {
  Wire.begin(8);                // join I2C bus with address #8
  Wire.onReceive(receiveEvent); // register event
  Serial.begin(9600);           // start serial for output
  myStepper.setSpeed(5);
  Serial.println("SetupFinished");
  unsigned long startMillis = millis();
}




void loop() { // stepper code

  if (move != 0){ // aka is button ON on?
    myStepper.step(move);
    //Serial.println(move);
    //Serial.println("STEP TO THE BEAT BROTHER");
    //Serial.println("Stepped");
    delayMicroseconds(t);
    
    if(millis() - previousMillis > 5000){
      Serial.println("We are STEPPING");
      previousMillis=millis();
    }}
  else{
    //Serial.println("Hello");
    if(millis() - previousMillis > 5000){
      previousMillis=millis();
      Serial.print("Waiting. move: ");
      Serial.print(move);
      Serial.println("");

    }
  }
}



void requestEvent() {
  Wire.beginTransmission(1);
  Wire.write("Command received successfully");
  Wire.endTransmission();
  Serial.println("Command Received Sucessfully");
}

