# backend/wsgi.py

"""
wsgi.py
- creates an application instance for the wsgi production server
"""

from sweettweet.application import create_app
app = create_app()