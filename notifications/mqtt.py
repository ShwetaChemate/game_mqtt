import paho.mqtt.client as mqtt
from django.conf import settings
import logging
import time

from notifications.models import GameEvent
from django.contrib.auth import get_user_model
User = get_user_model()

logger = logging.getLogger(__name__)

class MQTTClient:
    def __init__(self):
        self.topic = "game/notifications"
        self.client = mqtt.Client()
        # Clear any retained messages
        self.client.will_set(self.topic, None, qos=0, retain=True)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_publish = self._on_publish
        self.client.on_disconnect = self.on_disconnect
        self.connected = False
        self.connection_attempts = 0
        self.max_attempts = 3

    def _on_publish(self, client, userdata, mid, properties=None):
        """Fixed to match Paho MQTT's expected signature"""
        logger.info(f"Message with MID {mid} published successfully")

    def publish(self, username, event):
        if not self.connected:
            logger.warning("Not connected to broker")
            return False

        message = f"prosumio {username} {event}"
        try:
            result = self.client.publish(self.topic, message, qos=0)
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                logger.info(f"Published: {message}")
                return True
            logger.error(f"Publish failed with RC: {result.rc}")
            return False
        except Exception as e:
            logger.error(f"Publish error: {str(e)}")
            self.connected = False
            return False

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connected = True
            # Unsubscribe first to prevent duplicates
            client.unsubscribe(self.topic)
            # Then subscribe once
            client.subscribe(self.topic)
            self.connection_attempts = 0
            logger.info("Successfully connected to MQTT broker")
            client.subscribe(self.topic)
        else:
            logger.error(f"Connection failed with code {rc}")
            self.connected = False

    def on_disconnect(self, client, userdata, rc):
        self.connected = False
        if rc != 0:
            logger.warning(f"Unexpected disconnection (RC: {rc})")
            self.reconnect()

    def reconnect(self):
        if self.connection_attempts < self.max_attempts:
            self.connection_attempts += 1
            logger.info(f"Attempting reconnect ({self.connection_attempts}/{self.max_attempts})")
            try:
                self.client.reconnect()
            except Exception as e:
                logger.error(f"Reconnect failed: {str(e)}")
                time.sleep(2)  # Wait before next attempt

    def connect(self):
        try:
            logger.info(f"Connecting to {settings.MQTT_BROKER}:{settings.MQTT_PORT}...")
            self.client.connect(
                settings.MQTT_BROKER,
                port=settings.MQTT_PORT,
                keepalive=60
            )
            # Use clean session to prevent message buffering
            self.client.reconnect_delay_set(min_delay=1, max_delay=120)
            self.client.loop_start()
            time.sleep(1)
            return self.connected
        except Exception as e:
            logger.error(f"Connection error: {str(e)}")
            return False

    def on_message(self, client, userdata, msg):
        try:
            message = msg.payload.decode()
            logger.info(f"Received message: {message}")

            if not message.startswith("prosumio "):
                return

            _, username, event_info = message.split(' ', 2)

            try:
                user = User.objects.get(username=username)
                event_type = self.determine_event_type(event_info)

                GameEvent.objects.create(
                    user=user,
                    event_type=event_type,
                    message=event_info
                )
                logger.info(f"Saved event for {username}")

            except User.DoesNotExist:
                logger.error(f"User {username} not found")
            except Exception as e:
                logger.error(f"Database error: {str(e)}")

        except Exception as e:
            logger.error(f"Message processing error: {str(e)}")

    def determine_event_type(self, event_info):
        event_info = event_info.lower()
        if "start" in event_info:
            return 'start'
        elif "end" in event_info:
            return 'end'
        elif "pause" in event_info:
            return 'pause'
        elif "resume" in event_info:
            return 'resume'
        return 'score'


mqtt_client = MQTTClient()