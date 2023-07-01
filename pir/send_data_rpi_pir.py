import paho.mqtt.client as mqtt
import json
import time
import RPi.GPIO as GPIO
import socket

# Replace with your own values
MQTT_BROKER_PORT = 1883
THING_ID = "org.Iotp2c:pir_sensor"
MQTT_TOPIC = f"{THING_ID}/things/twin/commands/modify"

# PIR sensor pin
PIR_PIN = 14


def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc))


def on_disconnect(client, userdata, rc):
    print("Disconnected from MQTT broker with result code " + str(rc))


def on_publish(client, userdata, mid):
    print("Message published to " + MQTT_TOPIC)


def send_data_to_ditto(pir_data):
    # Create a MQTT client instance
    client = mqtt.Client()

    # Set the callbacks
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_publish = on_publish

    # Get the IP address of the MQTT broker
    broker_ip = socket.gethostbyname("mosquitto")

    # Connect to the MQTT broker
    client.username_pw_set(username='ditto', password='ditto')
    client.connect(broker_ip, MQTT_BROKER_PORT, 60)

    # Prepare the Ditto command payload
    ditto_data = {
        "topic": "org.Iotp2c/pir_sensor/things/twin/commands/modify",
        "path": "/",
        "value": {
            "thingId": "org.Iotp2c:pir_sensor",
            "policyId": "org.Iotp2c:policy",
            "definition": "https://github.com/casafurix/PIR-Sensor-Ditto/blob/main/wot/pir.tm.jsonld",
            "attributes": {
                "motion_detected": pir_data['motion_detected']
            }
        }
    }

    # Convert the dictionary to a JSON string
    ditto_data_str = json.dumps(ditto_data)

    # Publish the message to the MQTT topic
    client.publish(MQTT_TOPIC, payload=ditto_data_str)

    # Disconnect from the MQTT broker
    client.disconnect()

    print("Data sent to Ditto: " + json.dumps(ditto_data))


def setup_pir():
    # Set up the PIR sensor
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIR_PIN, GPIO.IN)


def read_pir():
    # Read the PIR sensor state
    motion_detected = GPIO.input(PIR_PIN)
    return motion_detected


def cleanup():
    # Clean up GPIO settings
    GPIO.cleanup()


# Set up PIR sensor
setup_pir()

# Example usage
while True:
    pir_data = {
        "motion_detected": read_pir()
    }
    send_data_to_ditto(pir_data)
    time.sleep(1)

# Clean up GPIO settings
cleanup()
