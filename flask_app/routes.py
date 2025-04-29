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
    feedback = request.form.to_dict()

    name = feedback.get('name')
    email = feedback.get('email')
    comment = feedback.get('comment')

    if not all([name, email, comment]):
        return "Error: All fields are required.", 400

    # Insert feedback into database
    db.insert_feedback(name, email, comment)  # Using proper method
    
    # Retrieve updated feedback list
    feedback_data = db.get_all_feedback()
    
    # Render template correctly
    return render_template('processfeedback.html', feedback_data=feedback_data)