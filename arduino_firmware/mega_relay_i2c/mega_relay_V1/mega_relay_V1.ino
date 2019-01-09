//Import the library required
#include <Wire.h>

#define RELAY1  22
#define RELAY2  23
#define RELAY3  24
#define RELAY4  25
#define RELAY5  26
#define RELAY6  27
#define RELAY7  28
#define RELAY8  29
#define RELAY9  30
#define RELAY10 31
#define RELAY11  32
#define RELAY12  33
#define RELAY13  34
#define RELAY14  35
#define RELAY15  36
#define RELAY16  37
#define RELAY17  38
#define RELAY18  39
#define RELAY19  40
#define RELAY20  41
#define RELAY21  42
#define RELAY22  43
#define RELAY23  44
#define RELAY24  45
#define RELAY25  46
#define RELAY26  47
#define RELAY27  48
#define RELAY28  49
#define RELAY29  50
#define RELAY30  51
#define RELAY31  52
#define RELAY32  53

//Slave Address for the Communication
#define SLAVE_ADDRESS 0x05

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
  pinMode(RELAY1, OUTPUT);
  pinMode(RELAY2, OUTPUT);  
  pinMode(RELAY3, OUTPUT);   
  pinMode(RELAY4, OUTPUT);
  pinMode(RELAY5, OUTPUT);   
  pinMode(RELAY6, OUTPUT);  
  pinMode(RELAY7, OUTPUT);   
  pinMode(RELAY8, OUTPUT);  
  pinMode(RELAY9, OUTPUT);   
  pinMode(RELAY10, OUTPUT);  
  pinMode(RELAY11, OUTPUT);   
  pinMode(RELAY12, OUTPUT);  
  pinMode(RELAY13, OUTPUT);   
  pinMode(RELAY14, OUTPUT);  
  pinMode(RELAY15, OUTPUT);   
  pinMode(RELAY16, OUTPUT); 
  pinMode(RELAY17, OUTPUT);
  pinMode(RELAY18, OUTPUT);  
  pinMode(RELAY19, OUTPUT);   
  pinMode(RELAY20, OUTPUT);
  pinMode(RELAY21, OUTPUT);   
  pinMode(RELAY22, OUTPUT);  
  pinMode(RELAY23, OUTPUT);   
  pinMode(RELAY24, OUTPUT);  
  pinMode(RELAY25, OUTPUT);   
  pinMode(RELAY26, OUTPUT);  
  pinMode(RELAY27, OUTPUT);   
  pinMode(RELAY28, OUTPUT);  
  pinMode(RELAY29, OUTPUT);   
  pinMode(RELAY30, OUTPUT);  
  pinMode(RELAY31, OUTPUT);   
  pinMode(RELAY32, OUTPUT); 
   
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
//  Serial.println(real_string_number);
//digitalRead(INTERUPT)==LOW
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
  Serial.println(relay_addr);
  if (relay_addr == "A01") {
    if (relay_state == 1) {
      digitalWrite(RELAY1,0);
    }
    if (relay_state == 0) {
      digitalWrite(RELAY1,1);
    }
  }
  if (relay_addr == "A02") {
    if (relay_state == 1) {
      digitalWrite(RELAY2,0);
    }
    if (relay_state == 0) {
      digitalWrite(RELAY2,1);
    }
  }
  if (relay_addr == "A03") {
    if (relay_state == 1) {
      digitalWrite(RELAY3,0);
    }
    if (relay_state == 0) {
      digitalWrite(RELAY3,1);
    }
  }
  if (relay_addr == "A04") {
    if (relay_state == 1) {
      digitalWrite(RELAY4,0);
    }
    if (relay_state == 0) {
      digitalWrite(RELAY4,1);
    }
  }
  if (relay_addr == "A05") {
    if (relay_state == 1) {
      digitalWrite(RELAY5,0);
    }
    if (relay_state == 0) {
      digitalWrite(RELAY5,1);
    }
  }
  if (relay_addr == "A06") {
    if (relay_state == 1) {
      digitalWrite(RELAY6,0);
    }
    if (relay_state == 0) {
      digitalWrite(RELAY6,1);
    }
  }
  if (relay_addr == "A07") {
    if (relay_state == 1) {
      digitalWrite(RELAY7,0);
    }
    if (relay_state == 0) {
      digitalWrite(RELAY7,1);
    }
  }
  if (relay_addr == "A08") {
    if (relay_state == 1) {
      digitalWrite(RELAY8,0);
    }
    if (relay_state == 0) {
      digitalWrite(RELAY8,1);
    }
  }
  if (relay_addr == "A09") {
    if (relay_state == 1) {
      digitalWrite(RELAY9,0);
    }
    if (relay_state == 0) {
      digitalWrite(RELAY9,1);
    }
  }
  if (relay_addr == "A10") {
    if (relay_state == 1) {
      digitalWrite(RELAY10,0);
    }
    if (relay_state == 0) {
      digitalWrite(RELAY10,1);
    }
  }
  if (relay_addr == "A11") {
    if (relay_state == 1) {
      digitalWrite(RELAY11,0);
    }
    if (relay_state == 0) {
      digitalWrite(RELAY11,1);
    }
  }
  if (relay_addr == "A12") {
    if (relay_state == 1) {
      digitalWrite(RELAY12,0);
    }
    if (relay_state == 0) {
      digitalWrite(RELAY12,1);
    }
  }
  if (relay_addr == "A13") {
    if (relay_state == 1) {
      digitalWrite(RELAY13,0);
    }
    if (relay_state == 0) {
      digitalWrite(RELAY13,1);
    }
  }
  if (relay_addr == "A14") {
    if (relay_state == 1) {
      digitalWrite(RELAY14,0);
    }
    if (relay_state == 0) {
      digitalWrite(RELAY14,1);
    }
  }
  if (relay_addr == "A15") {
    if (relay_state == 1) {
      digitalWrite(RELAY15,0);
    }
    if (relay_state == 0) {
      digitalWrite(RELAY15,1);
    }
  }
  if (relay_addr == "A16") {
      if (relay_state == 1) {
        digitalWrite(RELAY16,0);
      }
      if (relay_state == 0) {
        digitalWrite(RELAY16,1);
      }
    }
  if (relay_addr == "A17") {
    if (relay_state == 1) {
      digitalWrite(RELAY17,0);
    }
    if (relay_state == 0) {
      digitalWrite(RELAY17,1);
    }
  }
  if (relay_addr == "A18") {
    if (relay_state == 1) {
      digitalWrite(RELAY18,0);
    }
    if (relay_state == 0) {
      digitalWrite(RELAY18,1);
    }
  }
  if (relay_addr == "A19") {
    if (relay_state == 1) {
      digitalWrite(RELAY19,0);
    }
    if (relay_state == 0) {
      digitalWrite(RELAY19,1);
    }
  }
  if (relay_addr == "A20") {
    if (relay_state == 1) {
      digitalWrite(RELAY20,0);
    }
    if (relay_state == 0) {
      digitalWrite(RELAY20,1);
    }
  }
  if (relay_addr == "A21") {
    if (relay_state == 1) {
      digitalWrite(RELAY21,0);
    }
    if (relay_state == 0) {
      digitalWrite(RELAY21,1);
    }
  }
  if (relay_addr == "A22") {
    if (relay_state == 1) {
      digitalWrite(RELAY22,0);
    }
    if (relay_state == 0) {
      digitalWrite(RELAY22,1);
    }
  }
  if (relay_addr == "A23") {
    if (relay_state == 1) {
      digitalWrite(RELAY23,0);
    }
    if (relay_state == 0) {
      digitalWrite(RELAY23,1);
    }
  }
  if (relay_addr == "A24") {
    if (relay_state == 1) {
      digitalWrite(RELAY24,0);
    }
    if (relay_state == 0) {
      digitalWrite(RELAY24,1);
    }
  }
  if (relay_addr == "A25") {
    if (relay_state == 1) {
      digitalWrite(RELAY25,0);
    }
    if (relay_state == 0) {
      digitalWrite(RELAY25,1);
    }
  }
  if (relay_addr == "A26") {
    if (relay_state == 1) {
      digitalWrite(RELAY26,0);
    }
    if (relay_state == 0) {
      digitalWrite(RELAY26,1);
    }
  }
  if (relay_addr == "A27") {
    if (relay_state == 1) {
      digitalWrite(RELAY27,0);
    }
    if (relay_state == 0) {
      digitalWrite(RELAY27,1);
    }
  }
  if (relay_addr == "A28") {
    if (relay_state == 1) {
      digitalWrite(RELAY28,0);
    }
    if (relay_state == 0) {
      digitalWrite(RELAY28,1);
    }
  }
  if (relay_addr == "A29") {
    if (relay_state == 1) {
      digitalWrite(RELAY29,0);
    }
    if (relay_state == 0) {
      digitalWrite(RELAY29,1);
    }
  }
  if (relay_addr == "A30") {
    if (relay_state == 1) {
      digitalWrite(RELAY30,0);
    }
    if (relay_state == 0) {
      digitalWrite(RELAY30,1);
    }
  }
  if (relay_addr == "A31") {
    if (relay_state == 1) {
      digitalWrite(RELAY31,0);
    }
    if (relay_state == 0) {
      digitalWrite(RELAY31,1);
    }
  }
  if (relay_addr == "A32") {
      if (relay_state == 1) {
        digitalWrite(RELAY32,0);
      }
      if (relay_state == 0) {
        digitalWrite(RELAY32,1);
      }
    }
}


// callback for sending data
void sendData() {
  Wire.write(number);
}

void TurnOffLights () {
  digitalWrite(RELAY1,1);
  digitalWrite(RELAY2,1);
  digitalWrite(RELAY3,1);
  digitalWrite(RELAY4,1);
  digitalWrite(RELAY5,1);
  digitalWrite(RELAY6,1);
  digitalWrite(RELAY7,1);
  digitalWrite(RELAY8,1);
  digitalWrite(RELAY9,1);
  digitalWrite(RELAY10,1);
  digitalWrite(RELAY11,1);
  digitalWrite(RELAY12,1);
  digitalWrite(RELAY13,1);
  digitalWrite(RELAY14,1);
  digitalWrite(RELAY15,1);
  digitalWrite(RELAY16,1);
  digitalWrite(RELAY17,1);
  digitalWrite(RELAY18,1);
  digitalWrite(RELAY19,1);
  digitalWrite(RELAY20,1);
  digitalWrite(RELAY21,1);
  digitalWrite(RELAY22,1);
  digitalWrite(RELAY23,1);
  digitalWrite(RELAY24,1);
  digitalWrite(RELAY25,1);
  digitalWrite(RELAY26,1);
  digitalWrite(RELAY27,1);
  digitalWrite(RELAY28,1);
  digitalWrite(RELAY29,1);
  digitalWrite(RELAY30,1);
  digitalWrite(RELAY31,1);
  digitalWrite(RELAY32,1);  
}
