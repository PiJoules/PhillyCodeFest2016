const int PIN_DATA = 4;
const int PIN_LATCH = 3;
const int PIN_CLOCK = 2;

byte arrivalStatus = 1;

void setup() {
    pinMode(PIN_DATA, OUTPUT);
    pinMode(PIN_CLOCK, OUTPUT);
    pinMode(PIN_LATCH, OUTPUT);
}

void loop() {
    digitalWrite(PIN_LATCH, LOW);
    shiftOut(PIN_DATA, PIN_CLOCK, MSBFIRST, arrivalStatus);
    digitalWrite(PIN_LATCH, HIGH);
    simulate_motion();
}

/**
 * Pretend Update arrivalStatus as if this
 * was a bus that is getting closer to the
 * desired stop
 */
void simulate_motion() {
    arrivalStatus <<= 1;
    if (!arrivalStatus)
        arrivalStatus = 1;
    delay(1000);
}
