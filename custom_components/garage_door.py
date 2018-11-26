import homeassistant.loader as loader

# The domain of your component. Should be equal to the name of your component.
DOMAIN = 'garage_door'

# List of component names (string) your component depends upon.
DEPENDENCIES = ['mqtt']
 
CONF_STATUS_TOPIC = 'status_topic'
CONF_TRIGGER_TOPIC = 'trigger_topic'
DEFAULT_STATUS_TOPIC = 'connectedGarageDoor/status'
DEFAULT_TRIGGER_TOPIC = 'connectedGarageDoor/trigger'


def setup(hass, config):
    #Set up the Hello MQTT component.
    mqtt = hass.components.mqtt
    status_topic = config[DOMAIN].get(CONF_STATUS_TOPIC, DEFAULT_STATUS_TOPIC)
    trigger_topic = config[DOMAIN].get(CONF_TRIGGER_TOPIC, DEFAULT_TRIGGER_TOPIC)
    entity_id = 'garage_door.last_message'

    # Listener to be called when we receive a message.
    def message_received(topic, payload, qos):
        #Handle new MQTT messages.
        hass.states.set(entity_id, payload)

    # Subscribe our listener to a topic.
    mqtt.subscribe(status_topic, message_received)

    # Set the initial state.
    hass.states.set(entity_id, 'Ukjent status')  

    # Service to publish a message on MQTT.
    def set_trigger_service(call):
        # Service to send a message.
        mqtt.publish(hass, trigger_topic, call.data.get('new_state'))

    # Register our service with Home Assistant.
    hass.services.register(DOMAIN, 'trigger_door', set_trigger_service)

    # Return boolean to indicate that initialization was successfully.
    return True