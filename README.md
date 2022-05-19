# Personal_Digital_Assitant

# DB Setup
install Postgresql: https://www.postgresql.org/download/  

In order to create the database execute the following command in psql command line:  
createdb -h localhost -p 5432 -U postgres pda  
and set the password: pdapassword  

Then, in the psql command line execute:    
\i /PATH/TO/init.sql  

This will create the required schemas on your database. You can confirm this by running /dt. If this command shows a table named "userData" you are all set!

# Set up
install open-mpi https://www.open-mpi.org/

go to Google api console, create a new project, add geocoding API and distance matrix API
https://console.cloud.google.com/

Under credientials create API key
Download the api key and store it in APIkey.txt

Create a python virtual environment
``python3 -m venv``
and activate it
``. ./vent/bin/activate``
then install the required python packages:

``pip install -r requirements.txt``


# Run
``mpiexec --oversubscribe -n 5 python3 src/main.py``
This will start the program using 5 processes. If your CPU has more than 5 cores, you can ignore the oversubscribe option.

# Testing
there are seperated testing scripts that can run without using MPI
``python3 server.py``
this will just start the web server
