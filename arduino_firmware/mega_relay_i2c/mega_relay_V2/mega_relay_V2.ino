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

const char* relay_code_name[] = {
        "RELAY1",
        "RELAY2",
        "RELAY3",
        "RELAY4",
        "RELAY5",
        "RELAY6",
        "RELAY7",
        "RELAY8",
        "RELAY9",
        "RELAY10",
        "RELAY11",
        "RELAY12",
        "RELAY13",
        "RELAY14",
        "RELAY15",
        "RELAY16",
        "RELAY17",
        "RELAY18",
        "RELAY19",
        "RELAY20",
        "RELAY21",
        "RELAY22",
        "RELAY23",
        "RELAY24",
        "RELAY25",
        "RELAY26",
        "RELAY27",
        "RELAY28",
        "RELAY29",
        "RELAY30",
        "RELAY31",
        "RELAY32",
};


const char* addresse_code[] = {
    "A01",
    "A02",
    "A03",
    "A04",
    "A05",
    "A06",
    "A07",
    "A08",
    "A09",
    "A10",
    "A11",
    "A12",
    "A13",
    "A14",
    "A15",
    "A16",
    "A17",
    "A18",
    "A19",
    "A20",
    "A21",
    "A22",
    "A23",
    "A24",
    "A25",
    "A26",
    "A27",
    "A28",
    "A29",
    "A30",
    "A31",
    "A32",
};

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
  
