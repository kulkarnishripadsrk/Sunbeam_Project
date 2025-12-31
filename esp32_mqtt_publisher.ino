#include <WiFi.h>
#include <ArduinoMqttClient.h>
#include "DHT.h"

// ---------- WIFI ----------
const char* ssid = "sada";
const char* password = "12345678";

// ---------- MQTT ----------
const char* broker = "broker.hivemq.com";
int port = 1883;

// ---------- SENSOR ----------
#define DHTPIN 4
#define DHTTYPE DHT11
#define MQ2_PIN 34

WiFiClient wifiClient;
MqttClient mqttClient(wifiClient);
DHT dht(DHTPIN, DHTTYPE);
  
void setup() {
  Serial.begin(115200);

  // WiFi Connect
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi Connected");

  // MQTT Connect
  Serial.println("Connecting to MQTT...");
  if (!mqttClient.connect(broker, port)) {
    Serial.println("MQTT connection failed!");
    while (1);
  }
  Serial.println("MQTT Connected");

  dht.begin();
}

void loop() {

  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();
  int gasValue = analogRead(MQ2_PIN);

  // ---- Publish Temperature ----
  mqttClient.beginMessage("enviro/temperature");
  mqttClient.print(temperature);
  mqttClient.endMessage();

  // ---- Publish Humidity ----
  mqttClient.beginMessage("enviro/humidity");
  mqttClient.print(humidity);
  mqttClient.endMessage();

  // ---- Publish Gas ----
  mqttClient.beginMessage("enviro/gas");
  mqttClient.print(gasValue);
  mqttClient.endMessage();

  Serial.println("Published:");
  Serial.print("Temp: "); Serial.println(temperature);
  Serial.print("Humidity: "); Serial.println(humidity);
  Serial.print("Gas: "); Serial.println(gasValue);

  delay(6000);
}
