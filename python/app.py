import os
import requests
import time
import pprint
import json
import threading

from signalwire.rest import Client as signalwire_client
from signalwire.voice_response import VoiceResponse, Say, Gather
from flask import Flask,request

app = Flask(__name__)

# Create Proxy Session
@app.route('/create_session', methods=['GET', 'POST'])
def create_session(number1, number2):
    return "200"

# Lookup a proxy session by proxy number
@app.route('/lookup-session', methods=['GET', 'POST'])
def lookup_session():

    # Initialize SignalWire Client
    client = signalwire_client(os.environ['SIGNALWIRE_PROJECT'], os.environ['SIGNALWIRE_TOKEN'], signalwire_space_url = os.environ['SIGNALWIRE_SPACE'])

    # Read proxy number from request
    proxy_number = request.values.get("To")

    # Read participant number from request
    leg_1 = request.values.get("From")

    # read proxy sessions from json file
    with open('proxy_sessions.json') as f:
         sessions = json.load(f)

    # Lookup session, find session that has proxy number and participant that matches
    for session in sessions:

        # Lookup the second session participant, if A is calling
        if session["Proxy_Number"] == proxy_number and session["Participant_A_Number"] == leg_1:
            leg_2 = session["Participant_B_Number"]
            found = True
            break

        # Lookup the second session participant, if B is calling
        elif session["Proxy_Number"] == proxy_number and session["Participant_B_Number"] == leg_1:
            leg_2 = session["Participant_A_Number"]
            found = True
            break

        # We did not find anything yet
        found = False

    if found == True:
        # Check if a CallSid exists, if it does, it is a voice call
        if "CallSid" in request.values.keys():
            # Bridge legs voice
            response = VoiceResponse()
            response.dial(leg_2, callerId = proxy_number)
            return str(response)
        # Check if a MessageSid exists, if it does it is a text message
        elif "MessageSid" in request.values.keys():
            # Send a message, with challenge code to phone number provided.
            message = client.messages.create(
                from_ = proxy_number,
                body = request.values.get("Body"),
                to = leg_2
            )
            return "200"
    else:
        # No session found
        response = VoiceResponse()
        response.say("We are sorry but your call can not be completed at this time. Good Bye!")
        return str(response)

# Default route
@app.route('/')
def hello():
    return "Hello World!"

if __name__ == '__main__':
    app.run(host="0.0.0.0")
