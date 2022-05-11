# Personal_Digital_Assitant

# DB Setup
install Postgresql: https://www.postgresql.org/download/  
in the psql command line execute  
\i /PATH/TO/init.sql  
This will create the required schemas on your database. You can confirm this buy running /dt. If this command shows a table named "userData" you are all set!

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
