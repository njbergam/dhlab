from flask import Flask, Blueprint, session, flash, request, redirect, url_for, render_template
import os
import requests
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
from googleapiclient.discovery import build
from werkzeug.utils import secure_filename
# Used for security reasons - has much more use we aren't currently tapping into
from flask_talisman import Talisman
from flask_session.__init__ import Session
import matplotlib.pyplot as plt, mpld3
import random
import string
import json
import nltk

from ..tools1 import *
from ..tools.vars import branch, UPLOAD_FOLDER, GRAPHS_FOLDER, ALLOWED_EXTENSIONS
from ..tools.txtresult import txtResult

singlefile = Blueprint("singlefile", __name__, template_folder="templates")


# Route that is redirected to when the user wants to upload a file
@singlefile.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    # Request should be a post request
    if request.method == 'POST':
        # Check if the post request has the file data
        if bool(request.files) == False:
            session['failedSingle'] = 3
            return redirect(session['priorUrl'])

        # Store the file
        file = request.files['file']

        # If the user does not select a file, the browser submits an
        # empty file without a filename, so catch this.
        if file.filename == '':
            flash('No selected file')
            session['failedSingle'] = 1
            return redirect(session['priorUrl'])

        # If the file exists and is valid
        if file and allowed_file(file.filename):
            # Store file information in the session variable
            session['failedSingle'] = 0
            #secure_filename() makes sure the filename is not malicious
            session['fname'] = secure_filename(file.filename)
            session['fnameDisplay'] = session['fname']

            # Save the file in the upload folder
            file.save(os.path.join(UPLOAD_FOLDER, session['fname']))

            # Redirect back to the original page
            return redirect(session['priorUrl'])

    # Request was not a post request
    session['failedSingle'] = 1
    return redirect(session['priorUrl'])


# Route for the single-text webpage, used to show statistics for a single text
@singlefile.route('/single')
def single():
    # Store the previous route in session variable in case the user is
    # redirected off of this page.
    session['priorUrl'] = '/single'

    # Check for any previous error messages
    if 'failedSingle' not in session:
        fail = 0
    else:
        fail = session['failedSingle']

    # Reset error message variable
    session['failedSingle'] = 0

    # Check for fname and fnamedisplay variables
    if 'fname' not in session:
        session['fname'] = ""
    if "fnameDisplay" not in session:
        fnameDisplay = ''
    else:
        fnameDisplay = session['fnameDisplay']

    # Reset filename display variable
    session['fnameDisplay'] = ''

    # Render the template and pass the arguments as parameters
    return render_template('oneText.html', fail=fail, fname=fnameDisplay)


# Endpoint for reporting the results of a single text analysis
@singlefile.route('/report', methods=['GET', 'POST'])
def get_file():
    # If the user hits submit without giving any files
    if session['fname'] == "":
        session['failedSingle'] = 2
        return redirect('/single')

    # Converts received form data into a dictionary to be accessed
    dict = request.form.to_dict()

    # need to retrieve the uploaded file here for further processing
    # tokenization methods defined in tools1.py
    if session['fname'][-4:] == '.pdf':
        text = text_extractor('flaskr/uploads/' + session['fname'])
        text2 = cleanText2(text)
    else:
        #filename =  str(request)[ str(request).index('=')+1 : str(request).index('\' [GET]>') ]
        text = simpleTokenize('flaskr/uploads/' + session['fname'])
        #getNames('uploads/' + fname)
        text2 = cleanText('flaskr/uploads/' + session['fname'])

    # Create a new text result object with default values
    textRst = txtResult(session['fname'], -1, -1, "1", "1", "1")

    # Check the form data and compute various stats
    # Functions imported from tools1.py

    if "PercentQuotes" in dict:
        textRst.pq = percentQuotes(text)
        print("getting percent quotes")
    if "SLength" in dict:
        textRst.sen_avg, textRst.sen_stdv = senlenStats(text)
        print("sentence length")
    if "POS" in dict:
        print("creating pos chart")
        textRst.pos = ''.join(
            random.choices(string.ascii_uppercase + string.digits,
                           k=10))  #title of the generated chart
        savePOSPiChart(text2, textRst.pos)
    if "TopWords" in dict:
        print("creating top words chart")
        textRst.top = ''.join(
            random.choices(string.ascii_uppercase + string.digits, k=10))
        #os.unlink(os.path.join( app.config['GRAPHS_FOLDER'], top + ".png"))
        #os.unlink(branch+"/templates/static/graphs/" + top + ".png")
        #item_id = branch+"/templates/static/graphs/" + top + ".png"
        #item = self.session.query(Item).get(item_id)
        #self.session.delete(item)
        #db.session.commit()
        #os.remove(branch+"/templates/static/graphs/" + top + ".png");
        saveTopWords(text2, textRst.top)
    if "WordProg" in dict:
        print("creating word progression chart")
        textRst.wp = ''.join(
            random.choices(string.ascii_uppercase + string.digits, k=10))
        arr = dict["WordProgWords"].replace(" ", "").split(';')
        groups = []
        for i in range(len(arr)):
            groups.append(arr[i].split(','))
        oneTextPlotChronoMap(text2, groups, textRst.wp)
    session['fname'] = ""
    print(textRst.pos)
    print(textRst.wp)
    print(textRst.top)
    return render_template('results.html',
                           result=textRst)  #mpld3.fig_to_html(topFig))
