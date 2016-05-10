#/!bin/bash
#
# It's just shell script for docker build
#  (maybe it'll make some backup of debt.dat)
#
VER=1.2;

sudo docker cp iskrobot:/usr/local/ISKRobot/debt.dat debt.dat;
sudo docker cp iskrobot:/usr/local/ISKRobot/state.dat state.dat;
sudo docker build --tag iskrobot:$VER .;