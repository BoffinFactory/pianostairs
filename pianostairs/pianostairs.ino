/* 
 Debounce
 
 Each time the input pin goes from LOW to HIGH (e.g. because of a push-button
 press), the output pin is toggled from LOW to HIGH or HIGH to LOW.  There's
 a minimum delay between toggles to debounce the circuit (i.e. to ignore
 noise).  
 
 The circuit:
 * LED attached from pin 13 to ground
 * pushbutton attached from pin 2 to +5V
 * 10K resistor attached from pin 2 to ground
 
 * Note: On most Arduino boards, there is already an LED on the board
 connected to pin 13, so you don't need any extra components for this example.
 
 
 created 21 November 2006
 by David A. Mellis
 modified 30 Aug 2011
 by Limor Fried
 modified 28 Dec 2012
 by Mike Walters
 
 This example code is in the public domain.
 
 http://www.arduino.cc/en/Tutorial/Debounce
 */

// constants won't change. They're used here to 
// set pin numbers:
const int numPins=2;
const int buttonPin[] ={2,3} ;    // the number of the pushbutton pin
  // the number of the LED pin

unsigned int val = -1;


// Variables will change:
 // the current state of the output pin
int *buttonState = new int[numPins];             // the current reading from the input pin
int *lastButtonState = new int[numPins];   // the previous reading from the input pin

// the following variables are long's because the time, measured in miliseconds,
// will quickly become a bigger number than can be stored in an int.
long *lastDebounceTime = new long[numPins];  // the last time the output pin was toggled
long debounceDelay = 1;    // the debounce time; increase if the output flickers
int changed = false;
void setup() {
  for(int u = 0;u<numPins;u++)
  {
    pinMode(buttonPin[u], INPUT);
    buttonState[u] = HIGH;
  }


  // set initial LED state


  Serial.begin(9600); 
  while (!Serial) {
    ; // wait for serial port to connect. Needed for Leonardo only
  } 
}


void loop() {
  // read the state of the switch into a local variable:
  for(unsigned int u=0;u<numPins;u++)
  {
  int reading = digitalRead(buttonPin[u]);

  // check to see if you just pressed the button 
  // (i.e. the input went from LOW to HIGH),  and you've waited 
  // long enough since the last press to ignore any noise:  

  // If the switch changed, due to noise or pressing:
  if (reading != lastButtonState[u]) {
    // reset the debouncing timer
    lastDebounceTime[u] = millis();
  } 
  
  if ((millis() - lastDebounceTime[u]) > debounceDelay) {
    // whatever the reading is at, it's been there for longer
    // than the debounce delay, so take it as the actual current state:

    // if the button state has changed:
    if (reading != buttonState[u]) {
      

      buttonState[u] = reading;
      val ^= 1<< buttonPin[u];
      changed = true;
    }
  }// set the LED:

  // save the reading.  Next time through the loop,
  // it'll be the lastButtonState:
  lastButtonState[u] = reading;
  }
  if(changed)
  {
    Serial.println(val,HEX);
    changed = false;
  }
  
  // turn the LED on (HIGH is the voltage level)
  //delay(0.013157895);               // wait for a second
  //digitalWrite(led, LOW);    // turn the LED off by making the voltage LOW
  //delay(0.013157895);
  //delay(0.013157895);
}

