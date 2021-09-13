#!/bin/sh

# downloading the files needed to put the data into a db

echo Downloading latest covid data from governemnt of Alberta
python3 dataAPI.py
echo Data download success! 


# Putting data into database file

echo Putting data into .db file
python3 createCovidDB.py
echo Data successfully put into database
