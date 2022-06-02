# BountyBackend
Database server application for our bounty kiosk acounting.

# Usage/Prerequisites
This backend is written in Python using Flask. First install Python 3.10.x and use
> pip install flask

More details here: https://flask.palletsprojects.com/en/2.1.x/installation/

Then run these commands in a PowerShell:
> $env:FLASK_APP = "BountyBackend"

> python -m flask run

This should make the backend available at http://127.0.0.1:5000
