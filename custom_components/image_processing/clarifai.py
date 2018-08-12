"""
Component that will perform image classification via Clarifai.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/image_processing/clarifai
"""
from datetime import timedelta
import requests
import logging
import base64
import voluptuous as vol

from homeassistant.core import split_entity_id
import homeassistant.helpers.config_validation as cv
from homeassistant.components.image_processing import (
    PLATFORM_SCHEMA, ImageProcessingEntity, CONF_SOURCE, CONF_ENTITY_ID,
    CONF_NAME)

_LOGGER = logging.getLogger(__name__)

CONF_API_KEY = 'api_key'
CONF_CONCEPTS = 'concepts'
DEFAULT_CONCEPTS = 'NO_CONCEPT'

REQUIREMENTS = ['clarifai==2.2.3']

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_API_KEY): cv.string,
    vol.Optional(CONF_CONCEPTS, default=[DEFAULT_CONCEPTS]):
        vol.All(cv.ensure_list, [cv.string]),
})


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the Clarifai classifier."""
    entities = []
    for camera in config[CONF_SOURCE]:
        entities.append(ClarifaiClassifier(
            camera.get(CONF_NAME),
            config[CONF_API_KEY],
            config[CONF_CONCEPTS],
            camera[CONF_ENTITY_ID],
        ))
    add_devices(entities)


class ClarifaiClassifier(ImageProcessingEntity):
    """Perform a classification via Clarifai."""

    ICON = 'mdi:file'

    def __init__(self, name, API_key, concepts, camera_entity):
        """Init with the API key."""
        from clarifai.rest import ClarifaiApp
        self.app = ClarifaiApp(api_key=API_key)
        self.model_name = 'general-v1.3'
        self.model = self.app.models.get(self.model_name)
        if name:  # Since name is optional.
            self._name = name
        else:
            self._name = "Clarifai {0}".format(
                split_entity_id(camera_entity)[1])
        self._concepts = concepts
        self._camera_entity = camera_entity
        self._classifications = {}  # The dict of classifications
        self._state = None    # The most likely classification

    def process_image(self, image):
        """Perform classification of a single image."""
        base64_img = base64.b64encode(image)
        response = self.model.predict_by_base64(base64_img)

        if response['status']['description'] == 'Ok':
            data = response['outputs'][0]['data']['concepts']
            self._classifications = {
                item['name']: round(100.0*item['value'], 1) for item in data}
            self._state = next(iter(self._classifications))
            self.fire_concept_events()
        else:
            self._state = "Request_failed"
            self._classifications = {}

    def fire_concept_events(self):
        """Fire an event for each concept identified."""
        identified_concepts = self._classifications.keys() & self._concepts
        for concept in identified_concepts:
            self.hass.bus.fire(
                'Clarifai', {
                    CONF_ENTITY_ID: self._camera_entity,
                    'concept': concept,
                    })

    @property
    def device_class(self):
        """Return the class of this device, from component DEVICE_CLASSES."""
        return 'class'

    @property
    def camera_entity(self):
        """Return camera entity id from process pictures."""
        return self._camera_entity

    @property
    def state(self):
        """Return the state of the entity."""
        return self._state

    @property
    def state_attributes(self):
        """Return device specific state attributes."""
        attr = self._classifications
        return attr

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return self.ICON

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name
