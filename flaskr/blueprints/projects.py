from flask import Flask, Blueprint, session, flash, request, redirect, url_for, render_template
import os
import requests
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
from googleapiclient.discovery import build
from werkzeug.utils import secure_filename
# Used for security reasons - has much more use we aren't currently tapping into
# from flask_talisman import Talisman
from flask_session.__init__ import Session
import matplotlib.pyplot as plt, mpld3
import random
import string
import json
import nltk

from ..tools.simple_analytics import *
from ..tools.vars import branch, UPLOAD_FOLDER, GRAPHS_FOLDER, ALLOWED_EXTENSIONS
from ..tools.txtresult import txtResult

p = Blueprint("p",
              __name__,
              template_folder="templates",
              static_folder="../static")


# Landing page for the projects page
@p.route('/projects')
def projects():
    return render_template('projects.html')


# Route to serve the JSON file containing
@p.route('/projectData')
def projectData():
    return p.send_static_file("projects.json")


# Route to serve individual project page
@p.route("/projects/single/<identifier>")
def projectsSingle(identifier):
    return render_template('projectsSingle.html', id=identifier)
