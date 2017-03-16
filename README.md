# cmq
CMQ (Carnegie Mellon Queues) is an interactive website that maintains a database of queues for the public facilities/spaces
of Carnegie Mellon University. It was programmed using Python, Flask, HTML/CSS, SQL and Microsoft Azure.

The website cannot be run at the moment as the server for the database was being hosted on
Microsoft Azure has now been removed. 

The following commands would allow the website to be run if all of the proper additions are installed
and if the server were running. After entering commands, run server on browser of your choice.

% virtualenv venv
% venv\Sripts\activate.bat
(source venv/bin/activate for MAC users)
% python main.py start
% deactivate #deactivates virtual environment

Things to be installed in order to run server:
Python3, pip
After installing pip, enter the following commands
% pip install pyodbc==3.1.1
% pip install plotly
% pip install Flask
% pip install flask flask-sqlalchemy
