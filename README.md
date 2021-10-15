# Call/Text By Proxy

This guide will show you how to create a bi-directional mask of participants' phone numbers for voice and text messages using the [Python SignalWire SDK](https://developer.signalwire.com/twiml/reference/client-libraries-and-sdks#python). If you ever had a situation where you wanted to keep your phone number private between two parties, this example will help you out.  Services like Lyft and Uber use technology like this every day to help protect the personal phone numbers of both passengers and drivers.  There are many use cases for this, and we hope you find it helpful.

# Setup Your Environment File

1. Copy from example.env and fill in your values
2. Save new file called .env

Your file should look something like this.
```
## This is the full name of your SignalWire Space. e.g., example.signalwire.com
SIGNALWIRE_SPACE=
# Your Project ID - you can find it on the `API` page in your Dashboard.
SIGNALWIRE_PROJECT=
# Your API token - you can generate one on the `API` page in your Dashboard
SIGNALWIRE_TOKEN=
# The first proxy phone number you'll be using for this guide. Must include the `+1` 
SIGNALWIRE_NUMBER_1=+1xxxxxxxxxx
# The second proxy phone number you'll be using for this guide. Must include the `+1` 
SIGNALWIRE_NUMBER_2=+1xxxxxxxxxx
```

# Modify Your Proxy Session File
You will need to edit `proxy_sessions.json` to reflect the correct participant numbers and the SignalWire numbers you choose to wish as proxy numbers. 


```javascript
[
  {
    "Session_Id": "Demo123",
    "Participant_A_Number": "+15551237654",
    "Participant_B_Number": "+15553883000",
    "Proxy_Number": "+15556611212"
  },
  {
    "Session_Id": "Demo234",
    "Participant_A_Number": "+15555181212",
    "Participant_B_Number": "+12347896543",
    "Proxy_Number": "+15556611212"
  }
]

```

# Step by Step Code Walkthrough

When the `/lookup-session` route is called, it will look up an active proxy session and create a back-to-back phone call that is proxied, or a proxied text message.  **LEG A <-> SIGNALWIRE PROXY <-> LEG B** 

```python
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
```

# Build and Run on Docker

1. Use our pre-built image from Docker Hub 
```
docker pull signalwire/snippets-call-text-proxy:python
```
(or build your own image)

1. Build your image
```
docker build -t snippets-call-text-proxy .
```
2. Run your image
```
docker run --publish 5000:5000 --env-file .env snippets-call-text-proxy
```
3. The application will run on port 5000

# Build and Run Natively

To run the application, execute export FLASK_APP=app.py then run flask run.

You may need to use an SSH tunnel for testing this code if running on your local machine. – we recommend [ngrok](https://ngrok.com/). You can learn more about how to use ngrok [here](https://developer.signalwire.com/apis/docs/how-to-test-webhooks-with-ngrok). 

# Sign Up Here

If you would like to test this example out, you can create a SignalWire account and space [here](https://m.signalwire.com/signups/new?s=1).

Please feel free to reach out to us on our Community Slack or create a Support ticket if you need guidance!
