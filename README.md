SkypeCheckin
==============

1. Get 32-bit Python (Since Skype is a 32-bit application.) 
2. Get pip and run `pip install -r "requirements.txt"`
3. Run Skype
4. Put the chat you want to "check in" to into your bookmarked list
5. The members list in skype.py is a whitelist for the chats that contain members from the skype list you want to use the bot on.  For it to work, you must specify the full name as displayed on their Skype profile.  An empty list means the bot is enabled on all chats.
6. Run `python skype.py`
7. Have fun!

Commands
--------------
%time - Gets the current time(To be formatted)

%live - Gets the livestreamers.

%8ball [question] - Need an answer? Consult 8Ball.

%streamers - Gives a list of streamers currently being polled.

%addstreamer [streamer's channel] - Adds a streamer to the list of watched streamers.

%removestreamer [streamer's channel] - Removes a streamer to the list of watched streamers.

%message [optional message]- Shows/Modifies the message of the day.

%weather [city] [country] - Gets the weather for a city in a country.
