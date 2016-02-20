const int PIN_DATA = 4;
const int PIN_LATCH = 3;
const int PIN_CLOCK = 2;

void setup() {
    //Initialize Shift register
    pinMode(PIN_DATA, OUTPUT);
    pinMode(PIN_CLOCK, OUTPUT);
    pinMode(PIN_LATCH, OUTPUT);

    //Initialize Serial Port
    Serial.begin(9600);
}

void loop() {
    //Wait for a single byte
    while (Serial.available() < 1);
    byte arrivalStatus = Serial.read();
    Serial.write(arrivalStatus);

    //Update LEDs
    digitalWrite(PIN_LATCH, LOW);
    shiftOut(PIN_DATA, PIN_CLOCK, MSBFIRST, arrivalStatus);
    digitalWrite(PIN_LATCH, HIGH);
}
