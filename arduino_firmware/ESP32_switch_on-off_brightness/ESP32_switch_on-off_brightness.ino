#include <esp_sleep.h>
#include <WiFi.h>
#include <WiFiClient.h>

//Pushbuttons connected to GPIO32 & GPIO33 & GPIO34 & GPIO35 & GPIO36 & GPIO39
#define BUTTON_PIN_BITMASK 0x9600000000 //0x700000000 //

typedef int32_t esp_err_t;
int GPIO_WAKE;
int period = 3000;
unsigned long time_now = 0;
RTC_DATA_ATTR int bootCount = 0;

const char* ssid = "LumiereColas";
const char* password =  "lumierecherive";
String complete_addresse;
const char* host = "192.168.2.41";
const int httpPort = 5000;

String code = "/SwitchDetector";
char* locations[] = {"SW1", "SW2", "SW3", "SW4","SW5", "SW6", "SW7", "SW8", "SW9",  "SW10"};
                     
int pin_maping[] = {34, 21, 39, 27, 36, 4, 33, 15, 35, 14};

unsigned long timeout;

int debug = 1;

WiFiClient client;

void print_GPIO_wake_up(){
  uint64_t GPIO_reason = esp_sleep_get_ext1_wakeup_status();
  Serial.println("GPIO that triggered the wake up: GPIO ");
  //Serial.println((log(GPIO_reason))/log(2), 0);
  GPIO_WAKE = (log(GPIO_reason))/log(2);
  Serial.println(GPIO_WAKE);
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


void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  delay(100); 
  Serial.println("Hello There");
  delay(100);
  
  touch_pad_intr_disable();
  
  //Increment boot number and print it every reboot
  ++bootCount;
  Serial.println("Boot number: " + String(bootCount));
  delay(1000);
  //Print the wakeup reason for ESP32
  print_wakeup_reason();

  //Print the GPIO used to wake up
  print_GPIO_wake_up();

  setup_IO();
  more_inputs();
  GPIO_WAKE = 0;
  //Configure GPIOxx as ext1 wake up source for HIGH logic level
  esp_sleep_enable_ext1_wakeup(BUTTON_PIN_BITMASK,ESP_EXT1_WAKEUP_ANY_HIGH);

  
  Serial.println("Going to sleep now");
  delay(100);

  //Go to sleep now
  esp_deep_sleep_start();
}

void loop() {}



void check_GPIO_states() {
    delay(1000);
}

void setup_IO(){
  pinMode(33, INPUT);
  pinMode(34,INPUT);
  pinMode(35, INPUT);
  pinMode(36, INPUT);
  pinMode(39, INPUT);
  pinMode(21,INPUT);
  pinMode(27, INPUT);
  pinMode(4, INPUT);
  pinMode(15, INPUT);
  pinMode(14, INPUT);
}

void more_inputs() {
  int pressed_button;
  int previous_pressed = 0;
  time_now = millis();
  Serial.println("Make your Move");
  delay(100);
  //pressed_button = read_buttons();
  while (millis() < time_now + period) {
    pressed_button = read_buttons();
    if (pressed_button > 0 || pressed_button != previous_pressed) {
      
      send_wifi_state(pressed_button);
      
      previous_pressed = pressed_button;
    }
    
    pressed_button = 0;
  }
}

int read_buttons(){
  int val = 0;
  if(digitalRead(33) == HIGH) {
    val = 33;
  }
  else if(digitalRead(34) == HIGH) {
    val = 34;
  }
  else if (digitalRead(34) == HIGH){
    val = 35;
  }
  else if (digitalRead(36) == HIGH){
    val = 36;
  }
  else if (digitalRead(39) == HIGH){
    val = 39;
  }
  else if (digitalRead(21) == HIGH){
    val = 21;
  }
  else if (digitalRead(27) == HIGH){
    val = 27;
  }
  else if (digitalRead(4) == HIGH){
    val = 4;
  }
  else if (digitalRead(15) == HIGH){
    val = 15;
  }
  else if (digitalRead(14) == HIGH){
    val = 14;
  }
  else {
    val = 0;
  }
  return val;
}

void send_wifi_state(int pressed_button) {
  int brightness = 0;
  int pressed_button_index = 0;
  brightness = potentiometerTranslate(analogRead(32));
  
  if (debug == 0) {
    ConnectToWiFi();
  }

  pressed_button_index = convert_pin_to_index(pressed_button);
  delay(100);
  Serial.print("pressed button index: " + pressed_button_index);
  complete_addresse= code + "?light=" + locations[pressed_button_index] +"&state=" + brightness;
  Serial.print("Requesting URL: ");
  Serial.println(complete_addresse);

  
  Serial.print("Send wifi of pin: ");
  Serial.print(pressed_button);
  Serial.print(" at intensity: ");
  Serial.println(brightness);

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

int potentiometerTranslate(int PotRead) {

  return (PotRead * 100) / 4095;
}

int convert_pin_to_index(int pressed_button) {
  int i;
  int pressed_button_index;
  for (i=0;i<10;i++) {
    if (pin_maping[i] == pressed_button) {
      pressed_button_index = i;
    }
  }
  return pressed_button_index;
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
