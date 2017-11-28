"""
Support for Clarifai authentification.

Note that witin venv I had to pip install clarifai==2.0.32
then pip install --upgrade requests==2.14.2

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/clarifai/
"""
import logging
from requests.exceptions import RequestException
import voluptuous as vol

from homeassistant.const import CONF_API_KEY
import homeassistant.helpers.config_validation as cv

REQUIREMENTS = ['clarifai==2.0.32']

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'clarifai'

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_API_KEY): cv.string,
    }),
}, extra=vol.ALLOW_EXTRA)


def setup(hass, config):
    """Set up the Clarifai component."""
    from clarifai.rest import ClarifaiApp
    api_key = config[DOMAIN].get(CONF_API_KEY)

    try:
        app = ClarifaiApp(api_key=api_key)
        _LOGGER.error("Clarifai auth went OK!")
    except RequestException:
        # This doesnt currently work
        _LOGGER.error("Error while accessing the Clarifai. "
                      "Please check that your "
                      "API key is correct.")
        return False
    return True
