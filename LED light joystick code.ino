// Define pin connections
const int vrxPin = A0;   // Joystick X-axis
const int vryPin = A1;   // Joystick Y-axis
const int swPin = 2;     // Joystick button switch

const int ledUp = 10;    // LED for UP
const int ledDown = 11;  // LED for DOWN
const int ledLeft = 12;  // LED for LEFT
const int ledRight = 13; // LED for RIGHT
const int ledButton = 9; // LED for Button press

// Define joystick thresholds
const int threshold = 512;  // Mid-point of the joystick (between 0 and 1023)
const int deadzone = 100;   // Deadzone to prevent accidental triggering

void setup() {
  // Initialize Serial Monitor for debugging
  Serial.begin(9600);

  // Set joystick pins as input
  pinMode(vrxPin, INPUT);
  pinMode(vryPin, INPUT);
  pinMode(swPin, INPUT_PULLUP);

  // Set LED pins as output
  pinMode(ledUp, OUTPUT);
  pinMode(ledDown, OUTPUT);
  pinMode(ledLeft, OUTPUT);
  pinMode(ledRight, OUTPUT);
  pinMode(ledButton, OUTPUT); // Set button LED as output

  // Turn off all LEDs initially
  digitalWrite(ledUp, LOW);
  digitalWrite(ledDown, LOW);
  digitalWrite(ledLeft, LOW);
  digitalWrite(ledRight, LOW);
  digitalWrite(ledButton, LOW); // Turn off button LED initially
}

void loop() {
  // Read joystick values
  int xValue = analogRead(vrxPin);  // Read X-axis
  int yValue = analogRead(vryPin);  // Read Y-axis
  int swState = digitalRead(swPin); // Read the switch state

  // Debugging: print joystick values
  Serial.print("X: ");
  Serial.print(xValue);
  Serial.print(" | Y: ");
  Serial.print(yValue);
  Serial.print(" | SW: ");
  Serial.print(swState);
  Serial.println();

  // Turn off all LEDs initially
  digitalWrite(ledUp, LOW);
  digitalWrite(ledDown, LOW);
  digitalWrite(ledLeft, LOW);
  digitalWrite(ledRight, LOW);
  digitalWrite(ledButton, LOW); // Turn off button LED initially

  // Check the joystick direction and turn on the appropriate LED
  if (yValue > threshold + deadzone) {
    // Joystick pushed UP
    digitalWrite(ledUp, HIGH);
    Serial.println("LED Up ON");
  } else if (yValue < threshold - deadzone) {
    // Joystick pushed DOWN
    digitalWrite(ledDown, HIGH);
    Serial.println("LED Down ON");
  } else if (xValue < threshold - deadzone) {
    // Joystick pushed LEFT
    digitalWrite(ledLeft, HIGH);
    Serial.println("LED Left ON");
  } else if (xValue > threshold + deadzone) {
    // Joystick pushed RIGHT
    digitalWrite(ledRight, HIGH);
    Serial.println("LED Right ON");
  }

  // Check if the joystick button is pressed
  if (swState == LOW) { // Button pressed (active low)
    digitalWrite(ledButton, HIGH); // Turn on button LED
    Serial.println("Button LED ON");
  } else {
    digitalWrite(ledButton, LOW);  // Turn off button LED
  }
}
