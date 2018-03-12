"""
Component that will perform image classification via Clarifai.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/image_processing/clarifai
"""
import requests
import logging
import base64
import pathlib
import voluptuous as vol

from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_NAME

_LOGGER = logging.getLogger(__name__)

CONF_API_KEY = 'api_key'
CONF_MODEL_ID = 'model_id'
CONF_FILE_PATH = 'file_path'


PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_NAME): cv.string,
    vol.Required(CONF_API_KEY): cv.string,
    vol.Required(CONF_MODEL_ID): cv.string,
    vol.Required(CONF_FILE_PATH): cv.isfile,
})


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the folder sensor."""
    classifier = ClarifaiClassifier(
        config.get(CONF_NAME),
        config.get(CONF_API_KEY),
        config.get(CONF_MODEL_ID),
        config.get(CONF_FILE_PATH)
        )
    add_devices([classifier], True)


class ClarifaiClassifier(Entity):
    """Perform a classification via Clarifai."""

    ICON = 'mdi:file'

    def __init__(self, name, API_key, model_id, image_path):
        """Init with the API key and model id"""
        self._name = name
        self._headers = {
            'content-type': 'application/json',
            'Authorization': 'Key ' + API_key
        }
        self._url = "https://api.clarifai.com/v2/models/{}/outputs".format(
            model_id)
        self._image_path = image_path
        self._response = None
        self._data = None
        self._classifications = {}  # The dict of classifications
        self._state = None    # The most likely classification
        self.process_image()

    def process_image(self):
        """Perform classification of a single image."""
        img_file_data = pathlib.Path(self._image_path).read_bytes()
        base64_img = base64.b64encode(img_file_data).decode('ascii')
        json_data = {
            "inputs": [{"data": {"image": {"base64": base64_img}}}]
        }
        self._response = requests.post(
            self._url, headers=self._headers, json=json_data).json()

        if self._response['status']['description'] == 'Ok':
            self._data = self._response['outputs'][0]['data']['concepts']
            self._classifications = {
                item['name']: item['value'] for item in self._data}
            self._state = next(iter(self._classifications))
        else:
            self._state = "Request failed"
            self._data = None
            self._classifications = {}

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
