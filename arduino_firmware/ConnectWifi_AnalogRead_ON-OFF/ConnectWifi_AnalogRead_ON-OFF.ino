#include <WiFi.h>
#include <WiFiClient.h>

#define ANALOG_PIN_1 25 // A1
#define ANALOG_PIN_2 34 // A2
#define ANALOG_PIN_3 39 // A3

int analog_value = 0;
int ButtonRead = 0;
int PressedButton = 0;
int PreviousPressedButton1 = 0;
int PreviousPressedButton2 = 0;
int PreviousPressedButton3 = 0;
int value = 0;
int state;

bool lastpressedbutton1 = true;
bool lastpressedbutton2 = true;
bool lastpressedbutton3 = true;
bool lastpressedbutton4 = true;
bool lastpressedbutton5 = true;
bool lastpressedbutton6 = true;
bool lastpressedbutton7 = true;
bool lastpressedbutton8 = true;

const char* ssid = "LumiereColas";
const char* password =  "lumierecherive";

String complete_addresse;
const char* host = "192.168.1.106";
const int httpPort = 8090;

String http_adresse = "http://";
String host_code = "192.168.1.106:8090";
String code = "/ButtonDetector";
char* locations[] = {"B1", "B1","B2", "B2","B3", "B3","B4", "B4","B5", "B5","B6", "B6"};
//String location;

unsigned long timeout;

WiFiClient client;

void setup() {

  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial.println("Connecting to WiFi..");
  
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

void loop() {
  ButtonRead = analogRead(ANALOG_PIN_1);
  PreviousPressedButton1 = ReadButtonONOFF(0, ButtonRead, PreviousPressedButton1);  

  ButtonRead = analogRead(ANALOG_PIN_2);
  PreviousPressedButton2 = ReadButtonONOFF(4, ButtonRead, PreviousPressedButton2);

  ButtonRead = analogRead(ANALOG_PIN_3);
  PreviousPressedButton3 = ReadButtonONOFF(8, ButtonRead, PreviousPressedButton3);

  delay(1000);
}



void SendLightState(int PressedButton){
  if (PressedButton % 2 == 0){
    state = 1;
  }
  else {
    state = 0;
  }
  
  if (!client.connect(host, httpPort)) {
    Serial.println("connection failed");
    return;
  }
  
  complete_addresse= code + "?light=" + locations[PressedButton-1] + "&state=" + state;
  Serial.print("Requesting URL: ");
  Serial.println(complete_addresse);

  client.print(String("GET ") + complete_addresse + " HTTP/1.1\r\n" +
                 "Host: " + host + "\r\n" +
                 "Connection: close\r\n\r\n");
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

int ReadButtonONOFF(int AnalogIn, int ButtonRead, int PreviousPressedButton) {
  // grab the PressedButton state of the remote-buttons
  if (ButtonRead > 450 && ButtonRead < 550) {
    PressedButton = 1 + AnalogIn;
    PrintDetectedButton(PressedButton);
    SendLightState(PressedButton);
  }
  if (ButtonRead > 550 && ButtonRead < 750) {
    PressedButton = 2 + AnalogIn;
    PrintDetectedButton(PressedButton);
    SendLightState(PressedButton);
  }
  if (ButtonRead > 750 && ButtonRead < 1000) {
    PressedButton = 3 + AnalogIn;
    PrintDetectedButton(PressedButton);
    SendLightState(PressedButton);
  }
  if (ButtonRead > 1000) {
    PressedButton = 4 + AnalogIn;
    PrintDetectedButton(PressedButton);
    SendLightState(PressedButton);
  }

  if(PressedButton == PreviousPressedButton){
    return PressedButton;
  }
  else{
    PreviousPressedButton = PressedButton;
  }
  
  return PreviousPressedButton;
}

void PrintWifiInfo(){
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

void PrintDetectedButton(int PressedButton){
    Serial.print("Analog ");
    Serial.print(PressedButton);
    Serial.print(" detected");
    Serial.println("");
}
