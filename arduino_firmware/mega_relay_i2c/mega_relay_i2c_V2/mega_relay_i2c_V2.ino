#include <Adafruit_ESP8266.h>

//Import the library required
#include <Wire.h>

#define RELAY1  2
#define RELAY2  3
#define RELAY3  4
#define RELAY4  5
#define RELAY5  6
#define RELAY6  7
#define RELAY7  8
#define RELAY8  9
#define RELAY9  10
#define RELAY10 11
#define RELAY11  12
#define RELAY12  13

char relay_code_name[15] = {
  'RELAY1',
  'RELAY2',
  'RELAY3',
  'RELAY4',
  'RELAY5',
  'RELAY6',
  'RELAY7',
  'RELAY8',
  'RELAY9',
  'RELAY10',
  'RELAY11',
  'RELAY12',
};



char addresse_code[15] = {
  'A01',
  'A02',
  'A03',
  'A04',
  'A05',
  'A06',
  'A07',
  'A08',
  'A09',
  'A10',
  'A11',
  'A12',
};


//Slave Address for the Communication
#define SLAVE_ADDRESS 0x04

char number[50];
int state = 0;
String real_string_number;
String relay_code;
String relay_addr;
int string_length;
int relay_state;



//Code Initialization
void setup() {
  // initialize i2c as slave
  Serial.begin(9600);
  
  for (int i=0;i<=sizeof(addresse_code)-1;i++) {
    pinMode(relay_code_name[i], OUTPUT);
   }

  TurnOffLights ();

  Wire.begin(SLAVE_ADDRESS);
  // define callbacks for i2c communication
  Wire.onReceive(receiveData);
  //  Wire.onRequest(sendData);
}

void loop() {
  delay(100);
} // end loop

// callback for received data
void receiveData(int byteCount) {
  int i = 0;
  while (Wire.available()) {
    number[i] = Wire.read();
    i++;
  }
  number[i] = '\0';
  String string_number = String(number);
  real_string_number += string_number;
  string_length = real_string_number.length();
  if (string_length == 5) {
    relay_code = real_string_number;
    chop_data();
    Serial.println(real_string_number);
    update_relay_state();
    real_string_number = "";
  }
}

void chop_data() {
  int commaIndex = relay_code.indexOf(' ');
  relay_addr = relay_code.substring(0, commaIndex);
  relay_state = relay_code.substring(commaIndex + 1).toInt();
}

void update_relay_state() {
  for (int i=0;i<=sizeof(addresse_code)-1;i++) {
    if (relay_addr = addresse_code[i]) {
     if (relay_state == 1) {
      digitalWrite(relay_code_name[i],0);
      }
      if (relay_state == 0) {
        digitalWrite(relay_code_name[i],1);
      }
    }
  }
}

// callback for sending data
void sendData() {
  Wire.write(number);
}

void TurnOffLights () {
   for (int i=0;i<=sizeof(addresse_code)-1;i++) {
    digitalWrite(relay_code_name[i],1);
   }
}
