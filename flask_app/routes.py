# Author: Odon Mulambo

from flask import current_app as app
from flask import render_template, redirect, request
from .utils.database.database  import database
from werkzeug.datastructures import ImmutableMultiDict
from pprint import pprint
import json
import random
db = database()

@app.route('/')
def root():
	return redirect('/home')

@app.route('/home')
def home():
	x     = random.choice(['I started university when I was a wee lad of 15 years.','I have a pet sparrow.','I write poetry.'])
	return render_template('home.html')

@app.route('/resume')
def resume():
	resume_data = db.getResumeData()
	pprint(resume_data)
	return render_template('resume.html', resume_data = resume_data)

@app.route('/project')
def project():
	return render_template('projects.html')
@app.route('/piano')
def piano():
	return render_template('piano.html')

@app.route('/processfeedback', methods=['POST'])
def processfeedback():
    feedback = request.form.to_dict()  # Convert ImmutableMultiDict to a dictionary

    name = feedback.get('name')
    email = feedback.get('email')
    comment = feedback.get('comment')

    # Check if any of the variables are None and handle the case
    if name is None or email is None or comment is None:
        # Set default values or return an error message
        return "Error: One or more fields are empty."

    # Insert the form data into the feedback table within the database
    db.query("INSERT INTO feedback (name, email, comment) VALUES (%s, %s, %s)", (name, email, comment))

    # Extract all feedback from the feedback table
    feedback_data = db.query("SELECT * FROM feedback")

    # Render a template processfeedback.html that transforms the feedback data
    return render_template('processfeedback.html', feedback_data=feedback_data)
