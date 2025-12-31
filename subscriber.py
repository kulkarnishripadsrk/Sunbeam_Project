import paho.mqtt.client as mqtt
import mysql.connector
import requests
import time   # 🔹 ADDED

BROKER = "broker.hivemq.com"
PORT = 1883

THINGSPEAK_API_KEY = "OLYJYRGA4TXFHJPQ"
THINGSPEAK_URL = "http://api.thingspeak.com/update"

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="enviro_db"
)
cursor = db.cursor()

data = {"temperature": 0, "humidity": 0, "gas": 0}

# 🔹 ADDED (time control)
STORE_INTERVAL = 10     
last_store_time = 0

def on_connect(client, userdata, flags, rc):
    print("MQTT Connected")
    client.subscribe("enviro/temperature")
    client.subscribe("enviro/humidity")
    client.subscribe("enviro/gas")

def on_message(client, userdata, msg):
    global data, last_store_time

    value = float(msg.payload.decode())

    if msg.topic == "enviro/temperature":
        data["temperature"] = value
    elif msg.topic == "enviro/humidity":
        data["humidity"] = value
    elif msg.topic == "enviro/gas":
        data["gas"] = int(value)

    print(msg.topic, value)

    # 🔹 TIME CHECK (slow storage)
    current_time = time.time()
    if current_time - last_store_time >= STORE_INTERVAL:

        query = """
        INSERT INTO sensor_data (temperature, humidity, gas)
        VALUES (%s, %s, %s)
        """
        cursor.execute(query, (
            data["temperature"],
            data["humidity"],
            data["gas"]
        ))
        db.commit()

        payload = {
            "api_key": THINGSPEAK_API_KEY,
            "field1": data["temperature"],
            "field2": data["humidity"],
            "field3": data["gas"]
        }
        requests.post(THINGSPEAK_URL, data=payload)

        last_store_time = current_time
        print(" Data stored")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT, 60)

print("Backend running...")
client.loop_forever()
