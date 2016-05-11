#/!bin/bash
#
# It's just shell script for docker build
#  (maybe it'll make some backup of debt.dat)
#
VER=1.3;

# If you want to save your data from docker, you can uncomment two commends below it.
#  ** BUT YOU CAN'T USE DATA UNDER VERSION 1.2 (FROM 1.3, YOU CAN USE DATA BACKUP)!! **
#sudo docker cp iskrobot:/usr/local/ISKRobot/debt.dat debt.dat;
#sudo docker cp iskrobot:/usr/local/ISKRobot/state.dat state.dat;
sudo docker build --tag iskrobot:$VER .;