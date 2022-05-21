//Combined Lights, Fan and Relay Control

#include <FastLED.h>

#define NUM_STRIPS 2
#define NUM_LEDS_PER_STRIP1 24
#define NUM_LEDS_PER_STRIP2 12

unsigned long startTime;
unsigned long LedTime;
CRGB leds[NUM_LEDS_PER_STRIP1];
CLEDController * controllers[NUM_STRIPS];
uint8_t gBrightness = 64;

int incomingByte = 0;
const int RELAY_PIN = 3;
const int FAN_PIN = 4;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, HIGH);

  pinMode(FAN_PIN, OUTPUT);
  digitalWrite(FAN_PIN, LOW);

  startTime = millis();
  controllers[0] = &FastLED.addLeds<WS2812,5>(leds, NUM_LEDS_PER_STRIP1);
  //controllers[1] = &FastLED.addLeds<WS2812,5>(leds, NUM_LEDS_PER_STRIP2);

}

void loop() {
  // put your main code here, to run repeatedly:
  /*
  //If 'F' is sent to arduino (initial Fill)
  if(incomingByte == 70 && initial_filled == false){
    initial_fill();
    initial_filled = true;
  }

  //If 'D' is sent to arduino (Daily fill)
  if(incomingByte == 68 && initial_filled == false){
    every_day();
  }
  
  //If 'L' is sent to arduino (lights on)
  if(incomingByte == 76){
    fill_solid(leds, NUM_LEDS_PER_STRIP1, CRGB::White);
    controllers[0]->showLeds(gBrightness);
  }

  //If 'l' is sent to arduino (lights off)
  if(incomingByte == 108){
    fill_solid(leds, NUM_LEDS_PER_STRIP1, CRGB::Black);
    controllers[0]->showLeds(gBrightness);
  }
  */
  if (Serial.available() > 0) {
    incomingByte = Serial.read();

    //If 'V' is sent to arduino (valves open)
    if(incomingByte == 86){
      digitalWrite(3, LOW);
    }
  
    //If 'v' is sent to arduino (valves closed)
    if(incomingByte == 118){
      digitalWrite(3, HIGH);
    }

    //If 'L' is sent to arduino (lights on)
    if(incomingByte == 76){
      fill_solid(leds, NUM_LEDS_PER_STRIP1, CRGB::White);
      controllers[0]->showLeds(gBrightness);
    }
  
    //If 'l' is sent to arduino (lights off)
    if(incomingByte == 108){
      fill_solid(leds, NUM_LEDS_PER_STRIP1, CRGB::Black);
      controllers[0]->showLeds(gBrightness);
    }

    //If 'F' is sent to arduino (fan on)
    if(incomingByte == 70){
      digitalWrite(4, HIGH);
    }

    //If 'f' is sent to arduino (fan off)
    if(incomingByte == 102){
      digitalWrite(4, LOW);
    }
  }

}
