#include <WiFi.h>
#include <WiFiClient.h>

#define uS_TO_S_FACTOR 1000000  //Conversion factor for micro seconds to seconds
#define TIME_TO_SLEEP  20        //Time ESP32 will go to sleep (in seconds)
RTC_DATA_ATTR int bootCount = 0;


typedef int32_t esp_err_t;
int GPIO_WAKE;
int period = 3000;
unsigned long time_now = 0;


const char* ssid = "LumiereColas";
const char* password =  "lumierecherive";
String complete_addresse;
const char* host = "192.168.2.41";
const int httpPort = 5000;

String code = "/SwitchDetector";
String switch_code = "SW1";

unsigned long timeout;

int debug = 1;

WiFiClient client;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  delay(100); 
  Serial.println("Hello There");
  delay(100);
  
  touch_pad_intr_disable();
  
  //Increment boot number and print it every reboot
  //++bootCount;
  ++bootCount;
  Serial.println("Boot number: " + String(bootCount));
  delay(1000);
  //Print the wakeup reason for ESP32
  print_wakeup_reason();

  
  if (bootCount%2 == 1) {
    motion_detected();
    Serial.println("Setup ESP32 to sleep for every " + String(TIME_TO_SLEEP) +
  " Seconds");
    //Set timer to 5 seconds
    esp_sleep_enable_timer_wakeup(TIME_TO_SLEEP * uS_TO_S_FACTOR);
  }
  if (bootCount%2 == 0) {
    motion_undetected();
    Serial.println("Motion Undetected");
    //Configure GPIO34 as ext0 wake up source for HIGH logic level
    esp_sleep_enable_ext0_wakeup(GPIO_NUM_34,1);
  }
  
  
  
  Serial.println("Going to sleep now");
  delay(100);
  
  //Go to sleep now
  esp_deep_sleep_start();
}

void loop() {}

void motion_detected() {
  send_wifi_state();
}

void motion_undetected() {
  send_wifi_state_off();
}
//Function that prints the reason by which ESP32 has been awaken from sleep
void print_wakeup_reason(){
  esp_sleep_wakeup_cause_t wakeup_reason;
  wakeup_reason = esp_sleep_get_wakeup_cause();
  switch(wakeup_reason)
  {
    case 1  : Serial.println("Wakeup caused by external signal using RTC_IO"); break;
    case 2  : Serial.println("Wakeup caused by external signal using RTC_CNTL"); break;
    case 3  : Serial.println("Wakeup caused by timer"); break;
    case 4  : Serial.println("Wakeup caused by touchpad"); break;
    case 5  : Serial.println("Wakeup caused by ULP program"); break;
    default : Serial.println("Wakeup was not caused by deep sleep"); break;
  }
  
  delay(100);
  
}

void send_wifi_state() {

  if (debug == 0) {
    ConnectToWiFi();
  }
  delay(100);
  complete_addresse= code + "?light=" + switch_code + "&state=100";
  Serial.print("Requesting URL: ");
  Serial.println(complete_addresse);

  if (debug == 0) {
    if (!client.connect(host, httpPort)) {
      Serial.println("connection failed");
      return;
    }
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
  
}

void send_wifi_state_off() {

  if (debug == 0) {
    ConnectToWiFi();
  }
  delay(100);
  complete_addresse= code + "?light=" + switch_code + "&state=0";
  Serial.print("Requesting URL: ");
  Serial.println(complete_addresse);

  if (debug == 0) {
    if (!client.connect(host, httpPort)) {
      Serial.println("connection failed");
      return;
    }
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
