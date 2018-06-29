/*
 *  Simple HTTP get webclient test
 */

#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

int motionPin = 5;
int pirState = LOW;
int val = 0;



const char* ssid     = "VIDEOTRON3699"; 
const char* password = "mg1yf7v53q";

String complete_addresse;

String http_adresse = "http://";
String host_code = "192.168.0.106:8090";
String code = "/MotionDetector";
String location = "light";
//String state = "&state=";

//char http_adresse[128];
//const char* host = "192.168.0.106:8090";
//const char* code = "/helloesp";
//const char* location = "livingroom";
// http://192.168.0.106/MotionDetector?light=livingroom&state=1

int state = 0;


void setup() {
  Serial.begin(115200);
  delay(100);

  pinMode(motionPin, INPUT);
  
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");  
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  Serial.print("Netmask: ");
  Serial.println(WiFi.subnetMask());
  Serial.print("Gateway: ");
  Serial.println(WiFi.gatewayIP());
}



void loop() {
  val = digitalRead(motionPin);
  if (val==HIGH) {
    if (pirState == LOW) {
      if (WiFi.status() == WL_CONNECTED) {
        state = 1;
        HTTPClient http;
        complete_addresse = http_adresse + host_code + code + "?light=" + location + "&state=" + state;
        
        http.begin(complete_addresse);
        int httpCode = http.GET();
        if (httpCode > 0) {
          String payload = http.getString();
          Serial.println(payload);
        }
        else {
          Serial.println("An error occured");
        }
        http.end();
      }
      complete_addresse = "";
      pirState = HIGH;
    }
  }
  else {
    if (pirState == HIGH) {
      if (WiFi.status() == WL_CONNECTED) {
        state = 0;
        HTTPClient http;
        complete_addresse = http_adresse + host_code + code + "?light=" + location + "&state=" + state;
        
        http.begin(complete_addresse);
        int httpCode = http.GET();
        if (httpCode > 0) {
          String payload = http.getString();
          Serial.println(payload);
        }
        else {
          Serial.println("An error occured");
        }
        http.end();
      }
      complete_addresse = "";     
      pirState = LOW; 
    }
  }
    
  delay(100);
}


