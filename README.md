# global-entry-notify
This app will parse an input json to identify your appointment date and location, and then query the CBP's Trusted Traveler appointment availability API to check for any earlier appointment time slots. This code based on what I found on https://github.com/Drewster727/goes-notify, tweaked/modified to work with Python 3.9 and local execution only.

# Getting Started
- Clone the repo
- Have a PC/Mac with Python 3.9 or greater installed.
	- Install python modules for twilio & requests 
	`python pip install twilio`
	`python pip install requests`
- Update `config.json` for 
	- Current Appointment Time slot in MON DD, YYYY format. Example November 10, 2022
		- If you don't have an appointment set, set the current appointment to today's date.
	- Update the location-id for the location you are looking for. Currently only a single location is supported. You can lookup location id at [this link](https://ttp.cbp.dhs.gov/schedulerapi/locations/?temporary=false&inviteOnly=false&operational=true&serviceName=Global%20Entry). Search for your location of choice; use the 'id' field as location-id
	- Set the `sms_flag` and/or `email_flag` to true if you need notifications. See below for SMS/Email setup

- For SMS notifications
	- Create a twilio trial account (https://www.twilio.com/)
	- Update `config.json` 

- If Email notification are needed (only gmail supported at this time), create an app specific password on your gmail account (https://myaccount.google.com/apppasswords)

# Usage
- Open command prompt (PC) or Terminal (Mac), navigate to the location of the code.
- Execute the script `python main.py`
