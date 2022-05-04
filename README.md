# Personal_Digital_Assitant

# Set up
go to Google api console, create a new project, add geocoding API and distance matrix API
https://console.cloud.google.com/

Under credientials create API key
Download the api key and store in src/APIkey.txt

pip install -r requirements.txt


# Run
mpiexec --oversubscribe -n 5 python3 main.py       


# Testing
python3 server.py
this will just start the web server
