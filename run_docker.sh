#!/bin/sh
#
# It's just shell script for running ISKRobot docker
#
VER=1.5.2;

sudo docker stop iskrobot;
sudo docker rm iskrobot;
sudo docker run -d --name iskrobot --restart=unless-stopped -e TOKENKEY='USE_YOUR_BOT_TOKEN' -v /etc/localtime:/etc/localtime iskrobot:$VE$
sudo docker cp debt.db iskrobot:/usr/local/ISKRobot/debt.db;
sudo docker restart iskrobot;