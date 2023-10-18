

#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
#include <avr/power.h>  // Required for 16 MHz Adafruit Trinket
#endif
#include <SoftwareSerial.h>
#include <Stream.h>


// Which pin on the Arduino is connected to the NeoPixels?
#define PIN 6  // On Trinket or Gemma, suggest changing this to 1

// How many NeoPixels are attached to the Arduino?
#define NUMPIXELS 16  // Popular NeoPixel ring size

// When setting up the NeoPixel library, we tell it how many pixels,
// and which pin to use to send signals. Note that for older NeoPixel
// strips you might need to change the third parameter -- see the
// strandtest example for more information on possible values.
Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

#define DELAYVAL 20  // Time (in milliseconds) to pause between pixels

enum busyStatus {
  RED,
  GREEN,
  CALL,
  FREE,
  UNDEFINED
};

busyStatus resolvebusyStatusString(String input) {
  if (input == "RED") { return RED; }
  if (input == "GREEN") { return GREEN; }
  else {
    return UNDEFINED;
  }
};

void setup() {
  // These lines are specifically to support the Adafruit Trinket 5V 16 MHz.
  // Any other board, you can remove this part (but no harm leaving it):
#if defined(__AVR_ATtiny85__) && (F_CPU == 16000000)
  clock_prescale_set(clock_div_1);
#endif
  // END of Trinket-specific code.

  pixels.begin();  // INITIALIZE NeoPixel strip object (REQUIRED)
    // open the serial port:
  Serial.begin(9600);
  // initialize control over the keyboard:
  //Keyboard.begin();
  //pixels.clear();  // Set all pixel colors to 'off'
  SetAllPixelToColor(255, 255, 255);
  pixels.show();   // Send the updated pixel colors to the hardware.
}

void loop() {
  pixels.clear();  // Set all pixel colors to 'off'
  if (Serial.available() > 0) {
    // read incoming serial data:
    String inStr = Serial.readString();
    //inChar = inChar
    inStr.trim();
    inStr.toUpperCase();
    switch (resolvebusyStatusString(inStr)) {
      case RED:
        {
          //FadePixelFromGreenToRed();
          SetAllPixelToColor(255, 0, 0);
          break;
        }
      case GREEN:
        {
          //FadePixelFromRedToGreen();
          SetAllPixelToColor(0, 255, 0);
          break;
        }
      case UNDEFINED:
        {
          //FadePixelFromRedToGreen();
          //FadePixelFromGreenToRed();
          //FadePixelFromXToRed();
            SetAllPixelToColor(0, 0, 255);
          //pixels.clear();  // Set all pixel colors to 'off'
          break;
        }
    }

    pixels.show();  // Send the updated pixel colors to the hardware.
  }
}

void SetAllPixelToColor(int R, int G, int B) {
  // The first NeoPixel in a strand is #0, second is 1, all the way up
  // to the count of pixels minus one.
  for (int i = 0; i < NUMPIXELS; i++) {  // For each pixel...
    // pixels.Color() takes RGB values, from 0,0,0 up to 255,255,255
    pixels.setPixelColor(i, pixels.Color(R, G, B));
  }
  pixels.show();  // Send the updated pixel colors to the hardware.
}

void FadePixelFromRedToGreen() {
  for (int r = 255; r >= 0; r--) {
    Serial.println(r);
    Serial.println("FadePixelFromRedToGreen");
    SetAllPixelToColor(r, (r-255) * -1 , 0);
    delay(DELAYVAL);
  }
}

void FadePixelFromGreenToRed() {
  for (int g = 255; g >= 0; g--) {
    Serial.println(g);
    Serial.println("FadePixelFromGreenToRed");
    SetAllPixelToColor( (g-255) * -1, g , 0);
    delay(DELAYVAL);
  }
}

void FadePixelFromXToRed() {
  uint32_t test = pixels.getPixelColor(1);
  Serial.println(test);
    Serial.println("RGB Values of first strip");
    Serial.print("R");
    Serial.println(RED_component(test));
    Serial.print("G");
    Serial.println(GREEN_component(test));
    Serial.print("B: ");
    Serial.println(BLUE_component(test));

}


uint8_t RED_component (uint16_t color){
//Returns RED component of 16-Bit color
return (color >> 16) & 0xFF;
}
uint8_t GREEN_component (uint16_t color){
//Returns GREEN component of 16-Bit color
return (color >> 8) & 0xFF;
}
uint8_t BLUE_component (uint16_t color){
//Returns BLUE component of 16-Bit color
return (color) & 0xFF;
}