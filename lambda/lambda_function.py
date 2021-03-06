# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging

import pandas as pd
import requests
import io
import calendar
import datetime

import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Hello! Welcome to Hackathon Project Group 12. Would you like to know your zodiac sign or or get a store recommendation?"
        # reprompt_text = "I was born Nov. 6th, 2014. When were you born?"
        reprompt_text = "Would you like to now your zodiac sign or or get a store recommendation?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt_text)
                .response
        )


class CaptureZodiacSignIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("CaptureZodiacSignIntent")(handler_input)
        
        
    def filter(self, X):
        date = X.split()
        month = date[0]
        month_as_index = list(calendar.month_abbr).index(month[:3].title())
        day = int(date[1])
        return (month_as_index,day)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        # speak_output = "Hello World!"

        slots = handler_input.request_envelope.request.intent.slots
        year = slots["year"].value
        month = slots["month"].value
        day = slots["day"].value
        
        print('year', type(year))
        print('month', type(month))
        print('day', type(day))
        
        print('year', (year))
        print('month', (month))
        print('day', (day))
        
        try:
            month_int = int(datetime.datetime.strptime(month,'%b').strftime('%m'))
        except:
            month_int = int(datetime.datetime.strptime(month,'%B').strftime('%m'))
        print('month_int', type(month_int))
        print('month_int', (month_int))

        try:
            datetime.datetime(int(year), int(month_int), int(day))

            #ENTER YOUR URL HERE
            # url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTk3Wa6FiNVfDqcQI_IY-jSyuVjrT-0rve-IXKWckMPp03GLmn666VYubClFJROQw/pub?gid=1245857752&single=true&output=csv"
            url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSMocZJ5tS8seeje0Vp3aODakpNsT9fbActAA4OMUx56_JEPNZSCNlVf3RNjLw2rA/pub?gid=180977679&single=true&output=csv"
            csv_content = requests.get(url).content
            df = pd.read_csv(io.StringIO(csv_content.decode('utf-8')))
            
            zodiac = ''
            month_as_index = list(calendar.month_abbr).index(month[:3].title())
            usr_dob = (month_as_index,int(day))
            for index, row in df.iterrows():
                if self.filter(row['Start']) <= usr_dob <= self.filter(row['End']):
                    zodiac = row['Zodiac']
                    
            speak_output = 'I see you were born on the {day} of {month} {year}, which means that your zodiac sign will be {zodiac}.'.format(month=month, day=day, year=year, zodiac=zodiac)
        
        
        except ValueError:
            speak_output = "This is not a valid date"


        
        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class RecomendStoreIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("RecomendStoreIntent")(handler_input)
        
        

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        # speak_output = "Hello World!"

        print('RecomendStoreIntentHandler.Handle() invoked')

        slots = handler_input.request_envelope.request.intent.slots
        product = slots["product"].value
        city = slots["city"].value
        maxPrice = slots["maxPrice"].value

        print('product', type(product))
        print('city', type(city))
        print('maxPrice', type(maxPrice))
        
        print('product', (product))
        print('city', (city))
        print('maxPrice', (maxPrice))

        
        try:
            maxPrice = int(maxPrice)

            #ENTER YOUR URL HERE
            url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTk3Wa6FiNVfDqcQI_IY-jSyuVjrT-0rve-IXKWckMPp03GLmn666VYubClFJROQw/pub?output=csv"
            csv_content = requests.get(url).content
            df = pd.read_csv(io.StringIO(csv_content.decode('utf-8')))
            
            stores = df[(df["product"] == product.lower()) & (df["city"] == city.lower()) & (df["price"] < maxPrice)].store
            separator = " or "
            print(separator.join(stores))
            
            speak_output = 'I see you want to buy {product} in {city} under Rupees {maxPrice}'.format(product=product, city=city, maxPrice=maxPrice)
            
            if(len(stores) == 0):
                speak_output += '. But I cannot find any store which matches with your requirements'
            else:
                speak_output += ', you can buy the same from the following stores: {stores}.'.format(stores = separator.join(stores))
        
        
        except ValueError:
            speak_output = "something went wrong"
        

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, I'm not sure. You can say Hello or Help. What would you like to do?"
        reprompt = "I didn't catch that. What can I help you with?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(CaptureZodiacSignIntentHandler())
sb.add_request_handler(RecomendStoreIntentHandler())

sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()