@echo off
echo Running script for User and Admin Telegram Bot...
echo Starting User Bot
start "" python main.py
echo Starting Admin Bot
start "" python admin.py
echo Bot successfully started!