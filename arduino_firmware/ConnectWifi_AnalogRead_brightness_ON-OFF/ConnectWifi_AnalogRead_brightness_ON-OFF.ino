#include <WiFi.h>
#include <WiFiClient.h>

#define ANALOG_PIN_1 25 // A1
#define ANALOG_PIN_2 34 // A2
#define ANALOG_PIN_3 39 // A3
#define ANALOG_PIN_4 36 // A4
#define ANALOG_POT 4 // A5

// pin 4 et pin 25 ne fonctionne pas lorsque wifi fonctionne
// essayer pin 13 (A12) et pin 33 (A9) pin 32 (A7)

int ButtonRead = 0;
int PotRead = 0;
int PressedButton = 0;
int PreviousPressedButton1 = 0;
int PreviousPressedButton2 = 0;
int PreviousPressedButton3 = 0;
int PreviousPressedButton4 = 0;
int state;
int brightness;
int PotLevel;
String stringState;


const char* ssid = "LumiereColas";
const char* password =  "lumierecherive";
String complete_addresse;
const char* host = "192.168.1.106";
const int httpPort = 5000;

String code = "/BrightnessButtonDetector";
char* locations[] = {"B1", "B1", "B2", "B2", "B3", "B3", "B4", "B4",
                     "B5", "B5", "B6", "B6", "B7", "B7", "B8", "B8"};

unsigned long timeout;

WiFiClient client;

void setup() {

  // put your setup code here, to run once:
  Serial.begin(115200);
  
  
  ConnectToWiFi();

  
}

void loop() {

//  Serial.println(analogRead(ANALOG_POT));
//  Serial.println(analogRead(ANALOG_POT));
  int PotLevelss = (analogRead(ANALOG_POT)*100) / 4095;
  Serial.println(analogRead(ANALOG_POT));
//  
  
//  ButtonRead = analogRead(ANALOG_PIN_1);
//  PreviousPressedButton1 = ReadButtonONOFF(0, ButtonRead, PreviousPressedButton1);  

  ButtonRead = analogRead(ANALOG_PIN_2);
  PreviousPressedButton2 = ReadButtonONOFF(4, ButtonRead, PreviousPressedButton2);

  ButtonRead = analogRead(ANALOG_PIN_3);
  PreviousPressedButton3 = ReadButtonONOFF(8, ButtonRead, PreviousPressedButton3);
  
  ButtonRead = analogRead(ANALOG_PIN_4);
  PreviousPressedButton4 = ReadButtonONOFF(12, ButtonRead, PreviousPressedButton4);

  delay(500);
}

int ReadButtonONOFF(int AnalogIn, int ButtonRead, int PreviousPressedButton) {
  // grab the PressedButton state of the remote-buttons
  if (ButtonRead > 450 && ButtonRead < 550) {
    PressedButton = 1 + AnalogIn;
    PrintDetectedButton(PressedButton);
    PotLevel = potentiometerTranslate(analogRead(ANALOG_POT));
    SendLightState(PressedButton, PotLevel);
  }
  if (ButtonRead > 550 && ButtonRead < 750) {
    PressedButton = 2 + AnalogIn;
    PrintDetectedButton(PressedButton);
    PotLevel = potentiometerTranslate(analogRead(ANALOG_POT));
    SendLightState(PressedButton, PotLevel);
  }
  if (ButtonRead > 750 && ButtonRead < 1000) {
    PressedButton = 3 + AnalogIn;
    PrintDetectedButton(PressedButton);
    PotLevel = potentiometerTranslate(analogRead(ANALOG_POT));
    SendLightState(PressedButton, PotLevel);
  }
  if (ButtonRead > 1000) {
    PressedButton = 4 + AnalogIn;
    PrintDetectedButton(PressedButton);
    PotLevel = potentiometerTranslate(analogRead(ANALOG_POT));
    SendLightState(PressedButton, PotLevel);
  }

  if(PressedButton == PreviousPressedButton){
    return PressedButton;
  }
  else{
    PreviousPressedButton = PressedButton;
  }
  
  return PreviousPressedButton;
}

void SendLightState(int PressedButton, int PotLevel){

  state = ButtonChangeON_OFF(PressedButton);
  if (state == 0) {
    PotLevel = 0;
  }
  if (!client.connect(host, httpPort)) {
    Serial.println("connection failed");
    return;
  }
  
  complete_addresse= code + "?light=" + locations[PressedButton-1] +"&brightness=" + PotLevel;
  Serial.print("Requesting URL: ");
  Serial.println(complete_addresse);

  client.print(String("GET ") + complete_addresse + " HTTP/1.1\r\n" +
                 "Host: " + host + "\r\n" +
                 "Connection: close\r\n\r\n");
//  client.print(String("GET ") + complete_addresse + " HTTP/1.1\r\n");               
  unsigned long timeout = millis();
  while (client.available() == 0) {
      if (millis() - timeout > 5000) {
          Serial.println(">>> Client Timeout !");
          client.stop();
          return;
      }
  }
  
  // Read all the lines of the reply from server and print them to Serial
  while(client.available()) {
      String line = client.readStringUntil('\r');
      Serial.print(line);
  }

  Serial.println();
  Serial.println("closing connection");

  complete_addresse = "";
}


void PrintDetectedButton(int PressedButton){
    Serial.print("Button ");
    Serial.print(locations[PressedButton - 1]);
    Serial.print(" pressed ");
    if (ButtonChangeON_OFF(PressedButton) == 1) {
      stringState = "ON";
    }
    else {
      stringState = "OFF";
    }
    Serial.print(stringState);
    PotRead = analogRead(ANALOG_POT);
//    PotLevel = ;
    Serial.print(" at intensity ");
    Serial.print(potentiometerTranslate(PotRead));
    Serial.println("");
}

int ButtonChangeON_OFF(int PressedButton) {
  if (PressedButton % 2 == 1) {
    state = 1;
  }
  else {
    state = 0;
  }
  return state;
}

int potentiometerTranslate(int PotRead) {

  return (PotRead * 100) / 4095;
}

void ConnectToWiFi() {
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("Connected to the WiFi network");
  Serial.println("");
  Serial.println("WiFi connected");  
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  Serial.print("Netmask: ");
  Serial.println(WiFi.subnetMask());
  Serial.print("Gateway: ");
  Serial.println(WiFi.gatewayIP());
}
