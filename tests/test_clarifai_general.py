"""The tests for the clarifai_general component."""
from unittest.mock import Mock, mock_open, patch

import pytest
import requests
import requests_mock

from homeassistant.core import callback
from homeassistant.const import (
    ATTR_ENTITY_ID, ATTR_NAME, CONF_FRIENDLY_NAME, CONF_PASSWORD,
    CONF_USERNAME, CONF_IP_ADDRESS, CONF_PORT,
    HTTP_BAD_REQUEST, HTTP_OK, HTTP_UNAUTHORIZED, STATE_UNKNOWN)
from homeassistant.setup import async_setup_component
import homeassistant.components.image_processing as ip
import homeassistant.components.image_processing.clarifai_general as cg


# Mock data returned by the Clarifai API.

MOCK_HEALTH = {'success': True,
               'hostname': 'b893cc4f7fd6',
               'metadata': {'boxname': 'facebox', 'build': 'development'},
               'errors': []}


MOCK_NAME = 'mock_name'
MOCK_API_KEY = '12345'

RAW_CONCEPTS = [
    {'id': 'ai_Q', 'name': 'dog', 'value': 0.65432, 'app_id': 'main'},
    {'id': 'ai_c', 'name': 'cat', 'value': 0.34568, 'app_id': 'main'}
]

# Concepts data after parsing.
PARSED_CONCEPTS = [{'dog': 65.43},
                   {'cat': 34.57}]

VALID_ENTITY_ID = 'image_processing.clarifai_demo_camera'
VALID_CONFIG = {
    ip.DOMAIN: {
        'platform': 'clarifai_general',
        cg.CONF_API_KEY: MOCK_API_KEY,
        ip.CONF_SOURCE: {
            ip.CONF_ENTITY_ID: 'camera.demo_camera'}
        },
    'camera': {
        'platform': 'demo'
        }
    }


@pytest.fixture
def mock_api_key():
    """Mock cg.validate_api_key."""
    check_key = 'homeassistant.components.image_processing.' \
        'clarifai_general.validate_api_key'
    with patch(check_key, return_value=True) as _mock_api_key:
        yield _mock_api_key


@pytest.fixture
def mock_image():
    """Return a mock camera image."""
    with patch('homeassistant.components.camera.demo.DemoCamera.camera_image',
               return_value=b'Test') as image:
        yield image


def test_encode_image():
    """Test that binary data is encoded correctly."""
    assert cg.encode_image(b'test') == b'dGVzdA=='


def test_parse_data():
    """Test parsing of raw face data, and generation of matched_faces."""
    assert cg.parse_concepts(RAW_CONCEPTS) == PARSED_CONCEPTS


async def test_setup_platform(hass, mock_api_key):
    """Set up platform with one entity."""
    await async_setup_component(hass, ip.DOMAIN, VALID_CONFIG)
    assert hass.states.get(VALID_ENTITY_ID)
