# ISKRobot ver 1.1 with Docker
#  (Dockerfile Version: 1.0)
FROM python:3.5.1
MAINTAINER Gomgom "contact@gom2.net"

# Install Python Modules
RUN pip install python-telegram-bot

# Run the app
ADD ISKRobot.py /usr/local/ISKRobot/
ADD debt.dat /usr/local/ISKRobot/
WORKDIR /usr/local/ISKRobot
CMD python3 ./ISKRobot.py $TOKENKEY $ADMINID