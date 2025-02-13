# Author: Odon Mulambo

#--------------------------------------------------
# Import Requirements
#--------------------------------------------------
import os
from flask import Flask
from flask_failsafe import failsafe

#--------------------------------------------------
# Create a Failsafe Web Application
#--------------------------------------------------
@failsafe
def create_app():
    app = Flask(__name__)
    # Enable template auto-reloading
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.jinja_env.auto_reload = True
    app.jinja_env.cache = None

    from .utils.database.database import database
    db = database()
    db.createTables(purge=True)  # Ensure consistent indentation here

    with app.app_context():
        from . import routes  # Import routes inside app context
    return app

