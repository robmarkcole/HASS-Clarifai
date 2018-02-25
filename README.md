# HASS-Clarifai
Home-assistant image processing with [Clarifai](https://www.clarifai.com/).
Clarifai provide a number of different [models](https://www.clarifai.com/models).

To setup authentication with Clarifai, first generate an API key (YOUR_KEY) as per the [Clarifai docs](https://www.clarifai.com/developer/docs/) then add the following to you Home-assistant config:

```
image_processing:
  - platform: clarifai
    name: general_classifier
    api_key: YOUR_KEY
    model_id: YOUR_MODEL_ID
    file_path: /Users/robincole/Documents/Github/HASS-Clarifai/images/bird.jpg

# Lets display the file on the front end.
camera:
  - platform: local_file
    file_path: /Users/robincole/Documents/Github/HASS-Clarifai/images/bird.jpg
```

<p align="center">
<img src="https://github.com/robmarkcole/HASS-Clarifai/blob/master/images/usage.png" width="500">
</p>
