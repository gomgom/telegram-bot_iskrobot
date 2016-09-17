# ISKRobot ver 1.6.0 with Docker
#  (Dockerfile Version: 1.6.0)
FROM python:3.6-slim
MAINTAINER Gomgom "contact@gom2.net"

# Install Python Modules
RUN pip3 install python-telegram-bot &&\
 mkdir -p /usr/local/ISKRobot/

# Add Programs
ADD ISKRobot.py /usr/local/ISKRobot/
#ADD debt.db /usr/local/ISKRobot/
WORKDIR /usr/local/ISKRobot
CMD python3 ./ISKRobot.py $TOKENKEY