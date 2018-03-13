# HASS-Clarifai
Home-assistant image processing with [Clarifai](https://www.clarifai.com/). Clarifai provide a number of different [models](https://www.clarifai.com/models).
The component creates an entity which displays the most likely classification of the image, and the attributes contain all identified classes.

To setup authentication with Clarifai, first generate an API key (YOUR_KEY) as per the [Clarifai docs](https://www.clarifai.com/developer/docs/) then add the following to you Home-assistant config:

```
image_processing:
  - platform: clarifai
    name: general_classifier
    api_key: YOUR_KEY
    model_id: YOUR_MODEL_ID
    source:
      - entity_id: camera.demo_camera

```

<p align="center">
<img src="https://github.com/robmarkcole/HASS-Clarifai/blob/master/images/usage.png" width="300">
</p>
