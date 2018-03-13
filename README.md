# HASS-Clarifai
Home-assistant custom component for  [image processing](https://home-assistant.io/components/image_processing/) with [Clarifai](https://www.clarifai.com/). Clarifai provide a number of different [models](https://www.clarifai.com/models). The component creates an entity with a state that is the most likely concept (objects or ideas) within a camera image. The entities attributes contains a dictionary of all identified concepts and their probability (in %). An event is fired for each configured concept if that concept is identified.

* Place the custom_components folder in your configuration directory (or add its contents to an existing custom_components folder).
* The maximum image file size supported is 195 KB.
* For interval control, adjust the `scan_interval`. The default is 20 seconds since the number of API requests available on the [free plan](https://www.clarifai.com/pricing) is limited to 5000 per month (approx 1 every 10 minutes). Therefore the free plan is really only useful for testing the service.

To setup authentication with Clarifai, first generate an API key (YOUR_KEY) as per the [Clarifai docs](https://www.clarifai.com/developer/docs/) then add the following to you Home-assistant config:

```
image_processing:
  - platform: clarifai
    name: general_classifier
    api_key: YOUR_KEY
    model_id: YOUR_MODEL_ID
    source:
      - entity_id: camera.demo_camera
    concepts:
      - dog
      - pet

```

<p align="center">
<img src="https://github.com/robmarkcole/HASS-Clarifai/blob/master/images/usage.png" width="700">
</p>

#### To do
1. Currently image_processing of a camera feed performs a processing action every `scan_interval`. Would rather just processing image on each new frame captured by the camera.
2. Fork this component and use a classifier running on a local computer, probably in Docker. [MachineBox](https://machinebox.io/) is a good candidate.
3. Implement binary sensor for each concept.
