# HASS-Clarifai
Home-assistant image processing with [Clarifai](https://www.clarifai.com/). Clarifai provide a number of different (models)[https://www.clarifai.com/models].

There is an open issue with the install of clarifai within the home-assistant venv. To get around this, within venv I had to `pip install clarifai==2.0.32`
then `pip install --upgrade requests==2.14.2`

We will use a dummy camera for the puprpose of this demo:
```
camera:
  - platform: demo
  ```

To first setup authentication with Clarifai, first generate an API key (your_key) as per the (Clarifai docs)[https://www.clarifai.com/developer/docs/] then add to you Home-assistant config:
```
clarifai:
  api_key: "your_key"
```

To use the (face detection model)[https://www.clarifai.com/models/face-detection-image-recognition-model/a403429f2ddf4b49b307e318f00e528b] with a camera, add the following to your config:
```
image_processing:
 - platform: clarifai_face_detect
   source:
    - entity_id: camera.demo
```
