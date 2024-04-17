Book me uses natural language to perform simple functions through the google calendar API.

ex.
user_message = "Put in my calendar that I have a meeting with Jessica from 2 to 4."
output = I have scheduled a meeting with Jessica on April 17, 2024, from 2:00 PM to 4:00 PM. You can view the event details [here](https://www.google.com/calendar/event?eid=dTdxODJuYWowdGlncTExaGxtdGt2MDQ0czQgZXRoYW4ud20uaG9AbQ).

As of now, it can only perform 2 functions, creating a new event, and returning upcoming existing events from your calendar.

SET UP

1. obtain an openai API key and add it to your environment variables
   OPENAI_API_KEY , your_api_key
2. Allow it to access your google calendar account by running the main program once.
