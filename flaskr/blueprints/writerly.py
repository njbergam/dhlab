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

writerly = Blueprint("writerly", __name__, template_folder="templates")

# Landing page for passage sampling
@writerly.route('/passage', methods=['GET', 'POST'])
def passage():
    if not session["files"]:
        session["files"] = []

    session['priorUrl'] = '/passage'

    return render_template('passage.html', files=session["files"])

# Page for displaying the results of passage sampling
@writerly.route('/passage-results', methods=['GET', 'POST'])
def passageResults():
    dict = request.form.to_dict()

    results = samplePassage(session["files"], dict["term"],dict["numSamp"], dict["wordCount"])
    return render_template('passageResults.html',
                            results=results)