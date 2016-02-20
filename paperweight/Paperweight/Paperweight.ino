#include <LiquidCrystal.h>

//Shift Register Pins
const int PIN_DATA = 4;
const int PIN_LATCH = 3;
const int PIN_CLOCK = 2;

//Set up the LCD
LiquidCrystal lcd(12, 11, 7, 8, 9, 10);

void setup() {
    //Initialize Shift register
    pinMode(PIN_DATA, OUTPUT);
    pinMode(PIN_CLOCK, OUTPUT);
    pinMode(PIN_LATCH, OUTPUT);

    //Clear Shift Register
    digitalWrite(PIN_LATCH, LOW);
    shiftOut(PIN_DATA, PIN_CLOCK, MSBFIRST, 0);
    digitalWrite(PIN_LATCH, HIGH);

    //Initialize Serial Port
    Serial.begin(9600);

    //Initialize LCD display
    lcd.begin(16, 2);
    lcd.setCursor(0, 0);
    lcd.print("Loading...");
}

void loop() {
    //Wait for the arrival status
    while (Serial.available() < 1);
    byte arrivalStatus = Serial.read();

    //Update LEDs
    digitalWrite(PIN_LATCH, LOW);
    shiftOut(PIN_DATA, PIN_CLOCK, MSBFIRST, arrivalStatus);
    digitalWrite(PIN_LATCH, HIGH);

    //Wait for the ETA of next bus
    while (Serial.available() < 1);
    byte eta = Serial.read();

    //Update LCD
    lcd.setCursor(0, 0);
    lcd.print("Next bus arrives");
    lcd.setCursor(0, 1);
    lcd.print("in ");
    lcd.print(eta);
    lcd.print(" min.");
}
