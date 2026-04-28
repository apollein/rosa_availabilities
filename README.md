# Rosa Availabilities checker
Allows an user to check if a MD has closer availibilities than before, through Signal notifications.
It requires:

- https://github.com/bbernhard/signal-cli-rest-api
- a crontab to run it frequently
- a Signal account
- the link to Rosa's API that returns availabilities for a MD. Use F12 on your navigator, but functions to get that automatically will be implemented.

Usage: /usr/bin/python3 main.py [SIGNAL_PHONE_NUMBER] [SIGNAL_REST_API_SERVER] "[ROSA API AVAILABILITIES]"

More features will come, such as a config.json file to configure options (Signal REST API server, Signal account, MD to check, ...).

**This project is not related in any way to Rosa ASBL.**
