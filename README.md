Doople
=============

Framework for rapid development of applications with bi-directional json-rpc over websockets.

Requires: Tornado Web Server (pip install tornado)

Compatible with Python 2.7 and 3


Usage:

Three files are needed:

1. HTML file, put in the sites_html folder
2. Javascript file, put in the import_js folder
3. Python file, put in the import_py folder

If you look at the demo 'chat' app you will see that all three files need to have the same name (chat.html, chat.js, chat.py), this is the app name. You will also see how the files need to be formatted. Any number of apps can be added, but all apps running in the same instance will receive each other's messages.


Run:
>sudo python doople.py

Then open a web browser to 'localhost/chat' or 'localhost/(app_name)'


Planned:
- Database access
- NowJS compatibility
