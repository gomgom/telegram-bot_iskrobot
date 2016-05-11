# ISKRobot ver 1.3 with Docker
#  (Dockerfile Version: 1.3)
FROM python:3.5.1-slim
MAINTAINER Gomgom "contact@gom2.net"

# Install Python Modules
RUN pip3 install python-telegram-bot &&\
 mkdir -p /usr/local/ISKRobot/

# Add Programs
ADD ISKRobot.py /usr/local/ISKRobot/
ADD debt.dat /usr/local/ISKRobot/
ADD state.dat /usr/local/ISKRobot/
WORKDIR /usr/local/ISKRobot
CMD python3 ./ISKRobot.py $TOKENKEY