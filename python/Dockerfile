FROM python:3

ADD app.py /
ADD proxy_sessions.json /

RUN pip install flask
RUN pip install signalwire

EXPOSE 5000

CMD [ "python", "./app.py" ]
