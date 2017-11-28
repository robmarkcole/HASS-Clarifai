# HASS-Clarifai
Home-assistant image processing with Clarifai.

There is an open issue with the install of clarifai within the home-assistant venv. To get around this, within venv I had to `pip install clarifai==2.0.32`
then `pip install --upgrade requests==2.14.2`

To setup authentification, first add to config:
```
clarifai:
  api_key: "your_key"
```
