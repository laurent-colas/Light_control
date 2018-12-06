#include <WiFi.h>
#include <WiFiClient.h>

#define INPUT_PIN_1 25 // A1
#define INPUT_PIN_2 34 // A2
#define INPUT_PIN_3 39 // A3

const char* ssid = "VIDEOTRON9664";
const char* password =  "ym8qxtb3cg";

String complete_addresse;
const char* host = "192.168.0.106";
const int httpPort = 8090;
String code = "/ButtonDetector";
char* locations[] = {"B1","B2","B3"};

int ButtonRead = 0;

int PreviousStateButton1 = 0;
int PreviousStateButton2 = 0;
int PreviousStateButton3 = 0;

WiFiClient client;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  pinMode(INPUT_PIN_1, INPUT);
  pinMode(INPUT_PIN_2, INPUT);
  pinMode(INPUT_PIN_3, INPUT);
//  ConnectWiFi();

}

void loop() {
  // put your main code here, to run repeatedly:
  ButtonRead = digitalRead(INPUT_PIN_1);
  PreviousStateButton1 = LightStateChange(1, PreviousStateButton1, ButtonRead);

  ButtonRead = digitalRead(INPUT_PIN_2);
  PreviousStateButton2 = LightStateChange(2, PreviousStateButton2, ButtonRead);

  ButtonRead = digitalRead(INPUT_PIN_3);
  PreviousStateButton3 = LightStateChange(3, PreviousStateButton3, ButtonRead);
  
  delay(500);
}

int LightStateChange(int ButtonNum, int PreviousState, int ButtonRead) {
  if (ButtonRead == PreviousState) {
    return ButtonRead;
  }
  else{
      Serial.print("SW ");
      Serial.print(ButtonNum);
      Serial.print(" reads: ");
      Serial.println(ButtonRead);
//      SendSwitchState(ButtonNum, ButtonRead);
  }
  return ButtonRead;
}

void ConnectWiFi() {
  
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

void SendSwitchState(int ButtonNum, int ButtonRead) {
  if (!client.connect(host, httpPort)) {
    Serial.println("connection failed");
    return;
  }
  
  complete_addresse= code + "?light=" + locations[ButtonNum - 1] + "&state=" + ButtonRead;
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
