# Solar Pi

A [Raspberry Pi](http://geni.us/K28m) based, Flask powered photovoltaic monitor

![Solar Pi Dashboar](http://i.imgur.com/HLLRQ2f.png)

Demo at [http://solarpi.tafkas.net](http://solarpi.tafkas.net)

[![Code Climate](https://codeclimate.com/github/Tafkas/solarpi/badges/gpa.svg)](https://codeclimate.com/github/Tafkas/solarpi)

## Getting Started

### Prerequisites

To run the Solar Pi you need

- A Linux server running Python 2.7 (e.g. [Raspberry Pi](http://geni.us/K28m) running Raspbian)
- SQLite3 installed

### Installation

- Clone the repostory

        $ git clone https://github.com/Tafkas/solarpi.git

- create a virtual enviroment and activate it

        $ virtualenv --python=/usr/bin/python .venv
        $ source .venv/bin/activate
        
- install dependencies

        $ (.venv) pip install -r requirements/dev.txt
        
- create the SQLite database

        $ sqlite3 dev.db
        $ cat db_schema.sql | sqlite3 dev.db

- run the server
       
        $ (.venv) python manage.py server         
