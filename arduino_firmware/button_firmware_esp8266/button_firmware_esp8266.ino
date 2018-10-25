/*
 *  Simple HTTP get webclient test
 */

#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

byte ButtonPin1On = 14;
byte ButtonPin1Off = 12;
byte ButtonPin2On = 13;
byte ButtonPin2Off = 15;
byte ButtonPin3On = 0;
byte ButtonPin3Off = 16;
byte ButtonPin4On = 14;
byte ButtonPin4Off = 15;

boolean ButtonState1 = 0;
boolean ButtonState2 = 0;
boolean ButtonState3 = 0;
boolean ButtonState4 = 0;

boolean flag1 = 0;
boolean flag2 = 0;
boolean flag3 = 0;
boolean flag4 = 0;

String location1 = "B1";
String location2 = "B2";
String location3 = "B3";
String location4 = "B4";

const char* ssid     = "VIDEOTRON3699"; 
const char* password = "mg1yf7v53q";

String complete_addresse;
String http_adresse = "http://192.168.0.106:8090/ButtonDetector?light=";

int state = 0;


void setup() {
  Serial.begin(115200);
  delay(100);

  pinMode(ButtonPin0, INPUT_PULLUP);
  pinMode(ButtonPin2, INPUT_PULLUP);
  pinMode(ButtonPin4, INPUT_PULLUP);
  pinMode(ButtonPin5, INPUT_PULLUP);
  pinMode(ButtonPin12, INPUT_PULLUP);
  pinMode(ButtonPin13, INPUT_PULLUP);
  pinMode(ButtonPin14, INPUT_PULLUP);
  pinMode(ButtonPin15, INPUT_PULLUP);
  pinMode(ButtonPin16, INPUT_PULLUP);

  wifi_connection_initilisation();

}



void loop() {
  
  ButtonState0 = digitalRead(ButtonPin0);
  ButtonState2 = digitalRead(ButtonPin2);
  ButtonState4 = digitalRead(ButtonPin4);
  ButtonState5 = digitalRead(ButtonPin5);
  ButtonState12 = digitalRead(ButtonPin12);
  ButtonState13 = digitalRead(ButtonPin13);
  ButtonState14 = digitalRead(ButtonPin14);
  ButtonState15 = digitalRead(ButtonPin15);
  ButtonState16 = digitalRead(ButtonPin16);

  flag0 = check_state(ButtonState0, flag0, location1);
  flag2 = check_state(ButtonState2, flag2, location2);
  flag4 = check_state(ButtonState4, flag4, location3);
  flag5 = check_state(ButtonState5, flag5, location4);
  flag12 = check_state(ButtonState12, flag12, location5);
  flag13 = check_state(ButtonState13, flag13, location6);
  flag14 = check_state(ButtonState14, flag14, location7);
  flag15 = check_state(ButtonState15, flag15, location8);
  flag16 = check_state(ButtonState16, flag16, location9);
  
//  if (ButtonState5 == LOW) {
//    if (flag5 == 0) {
//      flag5 = 1;
//      
//      if (WiFi.status() == WL_CONNECTED) {
//        state = 1;
//        HTTPClient http;
//        complete_addresse = http_adresse + location1 + "&state=" + state;
//        
//        http.begin(complete_addresse);
//        int httpCode = http.GET();
//        if (httpCode > 0) {
//          String payload = http.getString();
//          Serial.println(payload);
//        }
//        else {
//          Serial.println("An error occured");
//        }
//        http.end();
//        complete_addresse = "";
//      }
//    }
//    else if (flag5 == 1) {
//      flag5 = 0;
//      if (WiFi.status() == WL_CONNECTED) {
//        state = 0;
//        HTTPClient http;
//        complete_addresse = http_adresse + location1 + "&state=" + state;
//        
//        http.begin(complete_addresse);
//        int httpCode = http.GET();
//        if (httpCode > 0) {
//          String payload = http.getString();
//          Serial.println(payload);
//        }
//        else {
//          Serial.println("An error occured");
//        }
//        http.end();
//        complete_addresse = "";
//      }
//    }
//  }
//  delay(200);
}


void wifi_connection_initilisation() {
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


int check_state(boolean ButtonState, boolean flag, String location) {
  if (ButtonState == LOW) {
    if (flag == 0) {
      flag = 1;
      if (WiFi.status() == WL_CONNECTED) {
        state = 1;
        HTTPClient http;
        complete_addresse = http_adresse + location1 + "&state=" + state;
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
        complete_addresse = "";
      }
    }
    else if (flag == 1) {
      flag = 0;
      if (WiFi.status() == WL_CONNECTED) {
        state = 0;
        HTTPClient http;
        complete_addresse = http_adresse + location1 + "&state=" + state;
        
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
        complete_addresse = "";
      }
    }
  }
  delay(200);

  return flag;
}

