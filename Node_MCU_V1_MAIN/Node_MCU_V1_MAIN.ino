#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <Wire.h>
/*
#ifndef STASSID
#define STASSID "PRINCESSLUNA 2703"; // we are our own network - means we can't use INTERNET
#define STAPSK  "LunaLand"; 
#endif
*/
// Station Access point
#ifndef APSSID
#define APSSID "Barn Door Tracker V1" // we are using a custom WIFI
#define APPSK  "Luna_Best_Pony"
#endif

/*
const char *ssid = STASSID;
const char *password = STAPSK;
*/
// Station constants
const char *ssid = APSSID;
const char *password = APPSK;

ESP8266WebServer server(80);




void Transmit(String sending) { // 8 bytes required
  sending+=" --Stepper";
  Wire.beginTransmission(8);
  Wire.write(sending.c_str()); // convert String into Char, weirdly it's equiv to a string
  Wire.endTransmission();

}

void Transmit_speed(String command,int speed) {
  Wire.beginTransmission(8);
  String data = String(speed)+" --Speed";
  Wire.write((String(data)).c_str());
  Serial.println("Speed command "+String(speed)+" --Speed");
  Wire.endTransmission();
  //Wire.write('hello'.c_str());
}

void handleRoot() {
  server.send(200, "text/html", "<h1>You are connected to the NodeMCU / Star Tracker - use the app or commandline in order to send commands</h1>");
}

void handleAPI() { // this should be the web server receiving commands
  String message = "Command received: "; // DEBUG
  String command = server.arg("command"); // What action
  String speed = server.arg("speed"); // stepper speed

  if (speed != NULL){ // if Command = SPEED get speed var and send with a dict style: Key - Val
    //Serial.println("Hello, your command was successful, :)");
    digitalWrite(LED_BUILTIN, 1);
    String transmitString = speed+"--Speed"; // hopefully we can actually do something with this lol.
    Serial.println("Speed Arg worked!");
    Serial.println(speed);
    Transmit_speed(transmitString,speed.toInt()); // sends to TRANSMIT function which sends to Arduino
    message += "Setting speed to:";
    message += speed;
  }
  else if (command == "STEPFORW"){
    //Serial.println("Hello, your command was successful, :)");
    digitalWrite(LED_BUILTIN, 0);
    Transmit(command); // sends to TRANSMIT function which sends to Arduino
    message += "Turning FORWARDS";
  }
  else if (command == "STEPBACK"){
    //Serial.println("Hello, your command was successful, :)");
    digitalWrite(LED_BUILTIN, 0); // might change to double flash and loop
    message += "Turning BACKWARDS, ";
    
    Transmit(command);
  }

  else if (command == "STEPSTOP"){
    //Serial.println("Hello, your command was successful, :)");
    digitalWrite(LED_BUILTIN, 1);
    message += "Turning OFF, ";
    
    Transmit(command);
  }
  
  //server.send(message);
  
  server.send(200,"text/plain",message);
  Serial.println(message);
  
}

void setup(void) {
  Wire.begin(D1, D2); // BEGIN Connection to Arduino
  pinMode(LED_BUILTIN, OUTPUT); // Enable Node's Light
  digitalWrite(LED_BUILTIN, 1); // Toggle Off, it's invesrsed(?)
  Serial.begin(115200);

  /*
  WiFi.mode(WIFI_STA); // connect to Wi
  WiFi.begin(ssid, password);
  Serial.println("");

   Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  WiFi.enableSTA(true)*/

  //WiFi.softAP(ssid, password);
  Serial.print("Setting soft-AP ... ");

  // THIS IS THE ONE
  boolean result = WiFi.softAP("Luna_StarTracker", "LunaControl");
  if(result == true)
  {
    Serial.println("Ready");
  }
  else
  {
    Serial.println("Failed!");
  }

  server.begin();

  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());



  server.on("/api", handleAPI);
  server.on("/", handleRoot); // Tell them to use app or command line
  //server.on("/", root);
  server.begin();
  Serial.println("HTTP server started");
}

void loop(void) {

  server.handleClient(); // handle client?
}
