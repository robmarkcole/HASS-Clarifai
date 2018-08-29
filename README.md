# HASS-Clarifai
Home-assistant custom component for [image processing](https://home-assistant.io/components/image_processing/) with [Clarifai](https://www.clarifai.com/) using the [general model](https://www.clarifai.com/models/general-image-recognition-model-aaa03c23b3724a16a56b629203edc62c) and the [Clarifai-python-api](https://clarifai-python.readthedocs.io/en/latest/clarifai.rest/). The component creates an entity with a state that is the most likely concept (objects or ideas) within a camera image. The entities attributes contains a dictionary of all identified concepts and their probability (in %). A `image_processing.model_prediction` event is fired for each concept predicted by the model.

* Place the custom_components folder in your configuration directory (or add its contents to an existing custom_components folder).
* The maximum image file size supported is 195 KB.
* For interval control, adjust the `scan_interval`. The default is 20 seconds since the number of API requests available on the [free plan](https://www.clarifai.com/pricing) is limited to 5000 per month (approx 1 every 10 minutes). Therefore the free plan is really only useful for testing the service.

To setup authentication with Clarifai, first generate an API key (YOUR_KEY) as per the [Clarifai docs](https://www.clarifai.com/developer/docs/) then add the following to you Home-assistant config:

```
image_processing:
  - platform: clarifai
    name: general_classifier
    api_key: YOUR_KEY
    source:
      - entity_id: camera.demo_camera
    concepts:
      - dog
      - pet

```

<p align="center">
<img src="https://github.com/robmarkcole/HASS-Clarifai/blob/master/images/usage.png" width="700">
</p>
