#/!bin/bash
#
# It's just shell script for docker build
#  (maybe it'll make some backup of debt.db)
#
VER=1.4.2;

# If you want to save your data from docker, you can uncomment a comment below it.
#  ** YOU CAN'T USE DATA OF VERSION UNDER 1.3, PLEASE BACK UP YOUR DATA ON OTHER TEXT EDITOR, OR ETC. **
#sudo docker cp iskrobot:/usr/local/ISKRobot/debt.db debt.db;
sudo docker build --tag iskrobot:$VER .;