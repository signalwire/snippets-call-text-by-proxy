# Snippets Call/Text By Proxy
This snippet will show you how to create a bi-directional mask of participants phone numbers for voice and text messages.
## About Call/Text By Proxy
If you ever had a situation where you wanted to keep your personal phone number private between two parties, this example will help you out.  Services like Lyft, and Uber use technology like this every day to protect passengers and drivers personal phone numbers.  There are many use cases for this and we hope you find it helpful.
## Getting Started
You will need a machine with Python installed, the SignalWire SDK, a provisioned SignalWire phone number, and optionaly Docker if you decide to run it in a container.

For this demo we will be using Python, but more languages may become available.

- [x] Python
- [x] SignalWire SDK
- [x] SignalWire Phone Number
- [x] Docker (Optional)
----
## Running Call/Text By Proxy - How It Works
## Methods and Endpoints

```
Endpoint: /lookup-session
Methods: GET OR POST
When this is called, it will lookup an active proxy session and bascially create a back to back phone call that is proxied, or a proxied text message.  LEG A <-> SIGNALWIRE PROXY <-> LEG B 
```

## Setup Your Enviroment File

1. Copy from example.env and fill in your values
2. Save new file callled .env

Your file should look something like this
```
## This is the full name of your SignalWire Space. e.g.: example.signalwire.com
SIGNALWIRE_SPACE=
# Your Project ID - you can find it on the `API` page in your Dashboard.
SIGNALWIRE_PROJECT=
# Your API token - you can generate one on the `API` page in your Dashboard
SIGNALWIRE_TOKEN=
# The proxy 1 phone number you'll be using for this Snippets. Must include the `+1` , e$
SIGNALWIRE_NUMBER_1=+14346613376
# The proxy 2 phone number you'll be using for this Snippets. Must include the `+1` , e$
SIGNALWIRE_NUMBER_2=+14346613377
```

## Modify Your Proxy Session File
1. Edit proxy_sessions.json
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

## Build and Run on Docker
Lets get started!
1. Use our pre-built image from Docker Hub 
```
For Python:
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

## Build and Run Natively
For Python
```
1. Replace environment variables
2. From command line run, python3 app.py
```

----
# More Documentation
You can find more documentation on LaML, Relay, and all Signalwire APIs at:
- [SignalWire Python SDK](https://github.com/signalwire/signalwire-python)
- [SignalWire API Docs](https://docs.signalwire.com)
- [SignalWire Github](https://gituhb.com/signalwire)
- [Docker - Getting Started](https://docs.docker.com/get-started/)
- [Python - Gettings Started](https://docs.python.org/3/using/index.html)

# Support
If you have any issues or want to engage further about this Signal, please [open an issue on this repo](../../issues) or join our fantastic [Slack community](https://signalwire.community) and chat with others in the SignalWire community!

If you need assistance or support with your SignalWire services please file a support ticket from your Dashboard. 

