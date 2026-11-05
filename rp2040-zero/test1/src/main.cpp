#include <Arduino.h>

// Define RP2040-Zero GPIO pins connected to control lines
const int S0_PIN = 0;
const int S1_PIN = 1;
const int S2_PIN = 2;
const int S3_PIN = 3;

// Define the Analog pin connected to the SIG pin
const int SIG_PIN = 26; // GP26 is Analog Input A0

// Voltage detection thresholds
// RP2040 ADC is 12-bit (0 - 4095). 3.3V outputs ~4095.
const int THRESHOLD = 3500; 

void setup() {
  // Initialize Serial communication
  Serial.begin(115200);
  while (!Serial) {
    delay(10); // Wait for Serial Monitor to open
  }

  // Configure control pins as outputs
  pinMode(S0_PIN, OUTPUT);
  pinMode(S1_PIN, OUTPUT);
  pinMode(S2_PIN, OUTPUT);
  pinMode(S3_PIN, OUTPUT);

  // RP2040 default ADC resolution is 10-bit in Arduino, let's explicitly set it to 12-bit
  analogReadResolution(12);
}

void loop() {
  int activeChannel = -1;

  // Scan all 16 channels
  for (int channel = 0; channel < 16; channel++) {
    // Set binary address on control pins using bitwise operations
    digitalWrite(S0_PIN, (channel & 0x01));
    digitalWrite(S1_PIN, (channel & 0x02) >> 1);
    digitalWrite(S2_PIN, (channel & 0x04) >> 2);
    digitalWrite(S3_PIN, (channel & 0x08) >> 3);

    // Give the analog switch a tiny moment to stabilize
    delayMicroseconds(10);

    // Read the voltage level on the common SIG pin
    int analogValue = analogRead(SIG_PIN);

    // Check if the channel is receiving a high voltage (near 3.3V)
    if (analogValue > THRESHOLD) {
      Serial.println("Channel " + String(channel) + " is HIGH with value: " + String(analogValue));
      activeChannel = channel;
      // Optional: break loop early if you only expect one channel to be high at a time
    }
  }

  // Print results to the Serial Monitor
  if (activeChannel != -1) {
    Serial.println(activeChannel);
  }

  // Delay before the next complete scan cycle
  delay(250);
}
