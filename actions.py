# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
import requests

from rasa_sdk import Action
from rasa_sdk.events import SlotSet

class ActionWeather(Action):
    def name(self):
        return 'action_weather'

    def run(self, dispatcher, tracker, domain):
        loc = tracker.get_slot('location')
        params = {
          'access_key': '87bedac4a43698303d061289bc714313', # Put your API key
          'query': loc
        }
        api_result = requests.get('http://api.weatherstack.com/current', params)
        api_response = api_result.json()
        country = api_response['location']['country']
        city = api_response['location']['name']
        condition = api_response['current']['weather_descriptions'][0]
        temperature_c = api_response['current']['temperature']
        humidity = api_response['current']['humidity']
        wind_mph = api_response['current']['wind_speed']

        response = """It is currently {} in {} at the moment. The temperature is {} ℃ degrees, the humidity is {}% and the wind speed is {} mph.""".format(condition, city, temperature_c, humidity, wind_mph)
        #response = 'Current temperature in %s is %dC' % (api_response['location']['name'], api_response['current']['temperature'])
        #response = "weather is absolutely fantastic in %s" %loc
        #response = 'Current temperature in %s is %d℃' % (api_response['location']['name'], api_response['current']['temperature'])
        dispatcher.utter_message(response)
        return [SlotSet('location',loc)]
