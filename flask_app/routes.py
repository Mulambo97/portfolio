# Author: Odon Mulambo

from flask import current_app as app
from flask import render_template

# Define Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/home')
def home_route():
    return render_template('home.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/piano')
def piano():
    return render_template('piano.html')

@app.route('/<page>')
def dynamic_page(page):
    return render_template(page)