#include <DHT.h>

#define DHTPIN 4
#define DHTTYPE DHT11
#define MQ2_PIN 34

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {

  float temp = dht.readTemperature();
  float hum = dht.readHumidity();
  int gasValue = analogRead(MQ2_PIN);

  Serial.print("Temp: ");
  Serial.print(temp);
  Serial.print(" C  |  Humidity: ");
  Serial.print(hum);
  Serial.print(" %  |  Gas: ");
  Serial.println(gasValue);

  delay(2000);
}
