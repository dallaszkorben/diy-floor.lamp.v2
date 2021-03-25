
int ledPin = 5;
float MAX_ANALOG_VALUE = 698;//644; //694; //1023;
float MAX_DIG_VALUE = 255;

#define SAMPLES 1000

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  //0-1023
  //int potmeterValue = analogRead(A0);
  int potmeterValue = 0;

  long value = 0;

  for (int i=0; i< SAMPLES ; i++){    
    //value = analogRead(A0);
    //Serial.print(value);
    //Serial.print(", ");
    value += analogRead(A0);
  }
  //Serial.println(potmeterValue);
  potmeterValue = value/SAMPLES;

  //0-1
  float normalizedValue = potmeterValue / MAX_ANALOG_VALUE;
  
  //1-2
  normalizedValue += 1.0;
  
  //10-100 -> 0-90
  float expValue = pow(10, normalizedValue) - 10;

  int fadeValue = (int) (expValue * MAX_DIG_VALUE / 90);
  
  //int fadeValue = log10(potmeterValue/4);
  
  analogWrite(ledPin, fadeValue);
  delay(50);

  //analogWrite(ledPin, 251);
  //delay(1000);
  //analogWrite(ledPin, 255);
  //delay(1000);
  //analogWrite(ledPin, 254);
  //delay(1000);
  //analogWrite(ledPin, 253);
  //delay(1000);
  //analogWrite(ledPin, 251);
  //delay(1000);

  Serial.print(potmeterValue);
  Serial.print(", ");
  Serial.print(normalizedValue);
  Serial.print(", ");
  Serial.print(expValue);  
  Serial.print(", ");
  Serial.println(fadeValue);
}
