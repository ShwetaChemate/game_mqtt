from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)

class NotificationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notifications'

    def ready(self):
        if not hasattr(self, 'mqtt_started'):
            from .mqtt import mqtt_client
            # Ensure we don't create multiple instances
            if not hasattr(mqtt_client, '_initialized'):
                mqtt_client.connect()
                setattr(mqtt_client, '_initialized', True)
            self.mqtt_started = True

