#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
#include <avr/power.h> // Required for 16 MHz Adafruit Trinket
#endif
#include <SoftwareSerial.h>
#include <Stream.h>

// Which pin on the Arduino is connected to the NeoPixels?
#define PIN 6 // On Trinket or Gemma, suggest changing this to 1

// How many NeoPixels are attached to the Arduino?
#define NUMPIXELS 16 // Popular NeoPixel ring size

// When setting up the NeoPixel library, we tell it how many pixels,
// and which pin to use to send signals. Note that for older NeoPixel
// strips you might need to change the third parameter -- see the
// strandtest example for more information on possible values.
Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

#define DELAYVAL 20 // Time (in milliseconds) to pause between pixels
#define BLINKDELAY 500

#define DEBUG

#define DEBUG_ERROR true
#define DEBUG_ERROR_SERIAL \
  if (DEBUG_ERROR)         \
  Serial

#define DEBUG_WARNING true
#define DEBUG_WARNING_SERIAL \
  if (DEBUG_WARNING)         \
  Serial

#define DEBUG_INFORMATION true
#define DEBUG_INFORMATION_SERIAL \
  if (DEBUG_INFORMATION)         \
  Serial

typedef enum
{
  RED,
  GREEN,
  YELLOW,
  BLUE,
  WHITE,
  OFFLINE,
  INIT,
  CALL,
  FREE,
  UNDEFINED
} busyStatus;

busyStatus resolvebusyStatusString(String input)
{
  if (input == "RED")
  {
    return RED;
  }
  if (input == "GREEN")
  {
    return GREEN;
  }
  if (input == "YELLOW")
  {
    return YELLOW;
  }
  if (input == "WHITE")
  {
    return WHITE;
  }
  if (input == "BLUE")
  {
    return BLUE;
  }
  if (input == "OFF")
  {
    return OFFLINE;
  }
  else
  {
    return UNDEFINED;
  }
};

busyStatus previousState = INIT;

void setup()
{
  // These lines are specifically to support the Adafruit Trinket 5V 16 MHz.
  // Any other board, you can remove this part (but no harm leaving it):
#if defined(__AVR_ATtiny85__) && (F_CPU == 16000000)
  clock_prescale_set(clock_div_1);
#endif
  // END of Trinket-specific code.

  pixels.begin(); // INITIALIZE NeoPixel strip object (REQUIRED)
                  // open the serial port:
  Serial.begin(9600);
  // initialize control over the keyboard:
  // Keyboard.begin();
  // pixels.clear();  // Set all pixel colors to 'off'
  SetAllPixelToColor(255, 255, 255);
  pixels.show(); // Send the updated pixel colors to the hardware.
  DEBUG_INFORMATION_SERIAL.println(" Version: 1.3.0.3  - Setup done, Arduino initialized. Waiting for Serial input......");
}

void loop()
{
  //pixels.clear(); // Set all pixel colors to 'off'
  if (Serial.available() > 0)
  {
    // read incoming serial data:
    String inStr = Serial.readString();
    // inChar = inChar
    inStr.trim();
    inStr.toUpperCase();
    switch (resolvebusyStatusString(inStr))
    {
    case RED:
    {
      DEBUG_WARNING_SERIAL.println("Case: RED");
      DEBUG_WARNING_SERIAL.print("previousState: ");
      DEBUG_WARNING_SERIAL.println(previousState);
      if (previousState != RED)
      {
        blink(255, 0, 0);
        SetAllPixelToColor(255, 0, 0);
        previousState = RED;
      }
      break;
    }
    case GREEN:
    {
      DEBUG_WARNING_SERIAL.println("Case: GREEN");
      if (previousState != GREEN)
      {
        blink(0, 255, 0);
        SetAllPixelToColor(0, 255, 0);
        previousState = GREEN;
      }
      break;
    }
    case YELLOW:
    {
      DEBUG_WARNING_SERIAL.println("Case: YELLOW");
      if (previousState != YELLOW)
      {
        blink(255, 200, 0);
        SetAllPixelToColor(255, 200, 0); // otherwise the LEDs look more greenish
        previousState = YELLOW;
      }
      break;
    }
    case WHITE:
    {
      DEBUG_WARNING_SERIAL.println("Case: WHITE");
      if (previousState != WHITE)
      {
        blink(255, 255, 255);
        SetAllPixelToColor(255, 255, 255);
        previousState = WHITE;
      }
      break;
    }
    case OFFLINE:
    {
      DEBUG_WARNING_SERIAL.println("Case: OFFLINE");
      if (previousState != OFFLINE)
      {
        blink(0,0,0);
        pixels.clear();
        previousState = OFFLINE;
      }
      break;
    }
    case UNDEFINED:
    {
      DEBUG_ERROR_SERIAL.print("Case: UNDEFINED. Please check why. String was: ");
      DEBUG_ERROR_SERIAL.println(inStr);
      if (previousState != UNDEFINED)
      {
        blink(0, 0, 255);
        SetAllPixelToColor(0, 0, 255);
        previousState = UNDEFINED;
      }
      break;
    }
    }

    pixels.show(); // Send the updated pixel colors to the hardware.
  }
}

void SetAllPixelToColor(int R, int G, int B)
{
  // The first NeoPixel in a strand is #0, second is 1, all the way up
  // to the count of pixels minus one.
  for (int i = 0; i < NUMPIXELS; i++)
  { // For each pixel...
    // pixels.Color() takes RGB values, from 0,0,0 up to 255,255,255
    pixels.setPixelColor(i, pixels.Color(R, G, B));
  }
  pixels.show(); // Send the updated pixel colors to the hardware.
}

void FadePixelFromRedToGreen()
{
  for (int r = 255; r >= 0; r--)
  {
    Serial.println(r);
    Serial.println("FadePixelFromRedToGreen");
    SetAllPixelToColor(r, (r - 255) * -1, 0);
    delay(DELAYVAL);
  }
}
void blink(int R, int G, int B)
{
  uint32_t test = pixels.getPixelColor(1);
  DEBUG_INFORMATION_SERIAL.println("void blink() start");
  DEBUG_INFORMATION_SERIAL.println("RGB Values of first strip");
  DEBUG_INFORMATION_SERIAL.print("R: ");
  DEBUG_INFORMATION_SERIAL.print(RED_component(test));
  DEBUG_INFORMATION_SERIAL.print(" G: ");
  DEBUG_INFORMATION_SERIAL.print(GREEN_component(test));
  DEBUG_INFORMATION_SERIAL.print(" B: ");
  DEBUG_INFORMATION_SERIAL.println(BLUE_component(test));
  pixels.clear();
  pixels.show();
  delay(BLINKDELAY);
  SetAllPixelToColor(R, G, B);
  pixels.show();
  delay(BLINKDELAY);
  pixels.clear();
  pixels.show();
  delay(BLINKDELAY);
  SetAllPixelToColor(R, G, B);
  pixels.show();
  delay(BLINKDELAY);
  pixels.clear();
  pixels.show();
  delay(BLINKDELAY);
  SetAllPixelToColor(R, G, B);
  pixels.show();
  DEBUG_INFORMATION_SERIAL.println("void blink() end");
}

void FadePixelFromGreenToRed()
{
  for (int g = 255; g >= 0; g--)
  {
    Serial.println(g);
    Serial.println("FadePixelFromGreenToRed");
    SetAllPixelToColor((g - 255) * -1, g, 0);
    delay(DELAYVAL);
  }
}

void FadePixelFromXToRed()
{
  uint32_t test = pixels.getPixelColor(1);
  Serial.println(test);
  Serial.println("RGB Values of first strip");
  Serial.print("R: ");
  Serial.print(RED_component(test));
  Serial.print(" G: ");
  Serial.print(GREEN_component(test));
  Serial.print(" B: ");
  Serial.println(BLUE_component(test));
}

uint8_t RED_component(uint16_t color)
{
  // Returns RED component of 16-Bit color
  return (color >> 16) & 0xFF;
}
uint8_t GREEN_component(uint16_t color)
{
  // Returns GREEN component of 16-Bit color
  return (color >> 8) & 0xFF;
}
uint8_t BLUE_component(uint16_t color)
{
  // Returns BLUE component of 16-Bit color
  return (color)&0xFF;
}