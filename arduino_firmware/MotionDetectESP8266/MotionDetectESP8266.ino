#define INPUT_PIN_1 13 // ESP8266 feather pull down required
//#define INPUT_PIN_1 2 // Arduino UNO
//#define INPUT_PIN_1 A1 // ESP32

#include <ESP8266WiFi.h>

const char* ssid = "LumiereColas";
const char* password =  "lumierecherive";

String complete_addresse;
const char* host = "192.168.1.106";
const int httpPort = 8090;

String url = "/MotionDetector";
const char* lightId = "?light=";
const char* stateId = "&state=";

const char* MotionDetectorId = "D1";
String location = "D1";

int ButtonRead = 0;
int state;

unsigned long motionDelay = 10000;
unsigned long motionTimer; 
bool inMotion = false;

void setup() {
  Serial.begin(115200);
  delay(10);
  ConnectToInternet();
  ConfigurePins();
  delay(15000);
}

void loop() {
  ButtonRead = digitalRead(INPUT_PIN_1);
//  Serial.println(ButtonRead);
  inMotion = MotionDetection(1, ButtonRead, inMotion);
  delay(100);
}


int MotionDetection(int ButtonNum, int ButtonRead, boolean inMotion) {
  if (ButtonRead == HIGH && !inMotion) {
    Serial.println("Motion Detected");
    SendMotionDetection(inMotion);
    motionTimer = millis();
    inMotion = true;
    digitalWrite(0, LOW);
  }
  else if (millis() - motionTimer >= motionDelay && inMotion) {
    SendMotionDetection(inMotion);
    Serial.println("Motion UnDetected");
    inMotion = false;
    digitalWrite(0, HIGH);
  }
  return inMotion;
}

void SendMotionDetection(bool inMotion) {
  // Use WiFiClient class to create TCP connections
  WiFiClient client;
  
  if (!client.connect(host, httpPort)) {
    Serial.println("connection failed");
    return;
  }

  url += lightId;
  url += MotionDetectorId;
  url += stateId;
  url += MotionChangeInt(inMotion);
  
  Serial.print("Requesting URL: ");
  Serial.println(url);
  
  // This will send the request to the server
  client.print(String("GET ") + url + " HTTP/1.1\r\n" +
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
  while (client.available()) {
    String line = client.readStringUntil('\r');
    Serial.print(line);
  }

  Serial.println();
  Serial.println("closing connection");

  url = "/MotionDetector";
}

int MotionChangeInt(bool inMotion) {
  if (inMotion) {
    int state = 1;
  }
  else {
    int state = 0;
  }
  return state;
}

void ConnectToInternet() {
  // We start by connecting to a WiFi network

  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  /* Explicitly set the ESP8266 to be a WiFi-client, otherwise, it by default,
     would try to act as both a client and an access-point and could cause
     network-issues with your other WiFi-devices on your WiFi-network. */
  WiFi.mode(WIFI_STA);
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

void ConfigurePins() {
  pinMode(INPUT_PIN_1, INPUT);
  pinMode(0, OUTPUT);
  digitalWrite(0, LOW);
}
