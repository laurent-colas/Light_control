// Remote Control with the Huzzah + Adafruit IO
// 
// Button Board
// 
// Adafruit invests time and resources providing this open source code.
// Please support Adafruit and open source hardware by purchasing
// products from Adafruit!
//
// Written by Richard Albritton, based on original code by Tony DiCola for Adafruit Industries
// Licensed under the MIT license.
//
// All text above must be included in any redistribution.
 
/************************** Configuration ***********************************/
 
// edit the config.h tab and enter your Adafruit IO credentials
// and any additional configuration needed for WiFi, cellular,
// or ethernet clients.
#include "config.h"
 
/************************ Example Starts Here *******************************/
#include <ESP8266WiFi.h>
 
// Analog Pin on ESP8266
#define Buttons A0
 
// remote-buttons state
int ButtonRead = 0;
int current = 0;
int last = -1;
 
// set up the 'remote-buttons' feed

void setup () {
 
  // start the serial connection
  Serial.begin(115200);
 
  // wait for serial monitor to open
  while(! Serial);
 
  // connect to io.adafruit.com
  Serial.print("Connecting to Adafruit IO");

  
}
 
void loop() {
  
  // io.run(); is required for all sketches.
  // it should always be present at the top of your loop
  // function. it keeps the client connected to
  // io.adafruit.com, and processes any incoming data.
  
 
  ButtonRead = analogRead(Buttons);
  delay(1);
  // grab the current state of the remote-buttons
  if (ButtonRead > 500 && ButtonRead < 600) {
    current = 1;
  }
  if (ButtonRead > 600 && ButtonRead < 750) {
    current = 2;
  }
  if (ButtonRead > 750 && ButtonRead < 900) {
    current = 3;
  }
  if (ButtonRead > 900) {
    current = 0;
  }
 
  // ret if value hasnt changed
  if(current == last)
    return;
 
  int32_t value = current;
  
  // let's publish stuff
  Serial.print("Sending RemoteButtons Value: ");
  Serial.print(value);
  Serial.print("...");
 
  delay(3000);
  
}
