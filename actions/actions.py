# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
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
class ActionCoronaState(Action):

    def name(self) -> Text:
        print("hi")
        return "action_corona_state"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("------inside -----run--")    
        response = requests.get("https://api.covid19india.org/data.json").json()
        print("response check point",response)

        
        entities = tracker.latest_message['entities']
        print("entities ",entities)
        state = None

        for e in entities:
            if e['entity'] == "state":
                state = e['value']
                print("state is "+state)
        message = "please enter correct state name"

        if state == "india":
            state = "Total"
            print(state)
            
        for data in response["statewise"]:
            # print(data)
            # message = "Active :"+data["active"]+"Confirmed :"+data["confirmed"]+"Recovered :"+data["recovered"]+"On "+data["lastupdatedtime"]
            if data['state'] == state:
                print(data)
                message = "Active :"+data["active"]+"Confirmed :"+data["confirmed"]+"Recovered :"+data["recovered"]+"On "+data["lastupdatedtime"]
        dispatcher.utter_message(message)
        return []