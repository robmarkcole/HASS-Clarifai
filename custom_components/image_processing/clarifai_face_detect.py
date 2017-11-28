"""
Support for Clarifai face detect model.

Based on https://github.com/robmarkcole/home-assistant/blob/dev/homeassistant/components/image_processing/dlib_face_detect.py

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/image_processing/clarifai_face_detect/
"""
import logging

from homeassistant.components.clarifai import CLARIFAI_APP
from homeassistant.components.image_processing import (
    CONF_SOURCE, CONF_ENTITY_ID, CONF_NAME)

DEPENDENCIES = ['clarifai']

_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the Clarifai general platform."""
    entities = []
    for camera in config[CONF_SOURCE]:
        entities.append(ClarifaiGeneralEntity(
            camera[CONF_ENTITY_ID], camera.get(CONF_NAME)
        ))

    add_devices(entities)


class ClarifaiFaceDetectEntity(ImageProcessingFaceEntity):
    """Clarifai general entity."""

    def __init__(self, camera_entity, name=None):
        """Initialise entity."""
        super().__init__()

        self._camera = camera_entity

        if name:
            self._name = name
        else:
            self._name = "Dlib Face {0}".format(
                split_entity_id(camera_entity)[1])

    @property
    def camera_entity(self):
        """Return camera entity id from process pictures."""
        return self._camera

    @property
    def name(self):
        """Return the name of the entity."""
        return self._name

    def process_image(self, image):
        """Process image."""
        # pylint: disable=import-error
        import face_recognition

        fak_file = io.BytesIO(image)
        fak_file.name = 'snapshot.jpg'
        fak_file.seek(0)

        image = face_recognition.load_image_file(fak_file)
        face_locations = face_recognition.face_locations(image)

        face_locations = [{ATTR_LOCATION: location}
                          for location in face_locations]

        self.process_faces(face_locations, len(face_locations))
