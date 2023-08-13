# BountyBackend
Database server application for our bounty kiosk accounting.
[![Upload Python Package](https://github.com/BountyApplication/BountyBackend/actions/workflows/python-publish.yml/badge.svg)](https://github.com/BountyApplication/BountyBackend/actions/workflows/python-publish.yml)

# Usage/Prerequisites
This backend is written in Python using Flask. First install Python 3.10.x and use
- pip install flask
- pip install flask_cors

More details here: https://flask.palletsprojects.com/en/2.1.x/installation/

Then run these commands in a PowerShell:
- $env:FLASK_APP = "BountyBackend"
- python -m flask run

This should make the backend available at http://127.0.0.1:5000

For production install Nginx and Gunicorn.

# Deployment / System setup
There are many ways to do that. Here is one example that seemed to be an easy yet secure setup:
- Nginx as proxy HTTP-Server
- Gunicorn as WSGI-Server

Unfortunately up to now this is a manual process...
## Server application
Make sure this repository is cloned into some working directory e.g. /home/pi/BountyBackend.
## Nginx configuration
Add the follwing lines to Nginx's configuration e.g. in the server section in file: /etc/nginx/sites-enabled/default
- location /bounty/ {
-   proxy_pass http://localhost:9000
- }
## Systemd Unit
Create a systemd unit e.g. /usr/lib/systemd/system/bountybackend.service with this content:
- [Unit]
- Description=Bounty Database Server Application
- After=network.target
- Before=nginx
- 
- [Service]
- User=pi
- Environment=FLASK_CONFIG=production
- ExecStart=gunicorn -w 1 -b localhost:9000 'BountyBackend:app'
- WorkingDirectory=/home/pi/BountyBackend
- Restart=always
- 
- [Install]
- WantedBy=multi-user.target

Remember to enable the systemd unit by
- systemctl enable bountybackend.service
