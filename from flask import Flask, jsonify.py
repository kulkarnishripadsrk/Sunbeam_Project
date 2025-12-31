from flask import Flask, jsonify
import paho.mqtt.client as mqtt

# ---------------- MQTT CONFIG ----------------
BROKER = "10.197.75.34"
PORT = 1883

# Store latest sensor values
sensor_data = {
    "temperature": None,
    "humidity": None,
    "gas": None
}

# ---------------- MQTT CALLBACKS ----------------
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker")
    client.subscribe("iot/temperature")
    client.subscribe("iot/humidity")
    client.subscribe("iot/gas")

def on_message(client, userdata, msg):
    value = msg.payload.decode()

    if msg.topic == "iot/temperature":
        sensor_data["temperature"] = value
    elif msg.topic == "iot/humidity":
        sensor_data["humidity"] = value
    elif msg.topic == "iot/gas":
        sensor_data["gas"] = value

    print(f"{msg.topic} → {value}")

# ---------------- MQTT SETUP ----------------
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(BROKER, PORT)
mqtt_client.loop_start()

# ---------------- FLASK APP ----------------
app = Flask(__name__)

@app.route('/')
def home():
    return "<h2>MQTT Flask Server Running</h2>"

@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(sensor_data)

# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000, debug=True)
