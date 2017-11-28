# HASS-Clarifai
Home-assistant image processing with [Clarifai](https://www.clarifai.com/).

There is an open issue with the install of clarifai within the home-assistant venv. To get around this, within venv I had to `pip install clarifai==2.0.32`
then `pip install --upgrade requests==2.14.2`

To setup authentification, first generate an API key (your_key) as per the (Clarifai docs)[https://www.clarifai.com/developer/docs/] then add to you Home-assistant config:
```
clarifai:
  api_key: "your_key"
```
