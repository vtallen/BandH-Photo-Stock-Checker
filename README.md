# B&H Photo Stock Checker
---
This script can be used to check if a list of items is in stock or not on bhphotovideo.com. If an item is in stock, the script uses gmail smtp to send a notification email to the address of your choice.

## Setup
---
This script depends on selenium to function. Install it with this command.
```
pip install selenium
```

To setup an app specific password for gmail, go here: https://myaccount.google.com/apppasswords
Select "Mail" as the app, and "Other" for the device. Enter this password without spaces into the program when it asks for it.

Upon program start, it will ask for several pieces of information to create the configuration file.

The location of your chrome binary is required to run the application, this is the location of the executable file for your installation of chrome.

## Usage
---
```
python3 bandh_checker.py
```

URLs can be added after the inital configuration by editing urls.json
