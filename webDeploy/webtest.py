import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from flask import render_template

from test import cleanText
from test import simpleTokenize
from test import detokenize
from test import percentQuotes
from test import senlenStats
from test import savePOSPiChart
from test import deList
from test import saveTopWords

from thesis import thesisVector

from twoText import wpReport
from twoText import plotChronoMap

import random
import string



app = Flask(__name__, static_folder=os.path.abspath('/Users/nbergam/Desktop/AmericanModernism/webDeploy/templates/static') )

if __name__ == '__main__':
    app.run(debug=True)
    app.debug = True
    app.secret_key = "vkjgvkgv"

UPLOAD_FOLDER = '/Users/nbergam/Desktop/AmericanModernism/webDeploy/uploads'
GRAPHS_FOLDER = '/Users/nbergam/Desktop/AmericanModernism/webDeploy/graphs'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('hello.html')

@app.route('/<type>', methods=['GET', 'POST'])
def upload_file(type):
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # where you go after uploading
            return redirect(url_for('get_file',
                                    filename=filename))
    return render_template(type+'.html')

from flask import send_from_directory

@app.route('/Users/nbergam/Desktop/AmericanModernism/webDeploy/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

#---Single Text

@app.route('/single')
def single():
	return render_template('oneText.html')

@app.route('/report', methods=['GET', 'POST'])
def get_file():
    # need to retrieve the uploaded file here for further processing
    text = simpleTokenize("/Users/nbergam/Desktop/AmericanModernism/webDeploy/uploads/SoundAndFury.txt")
    text2  = cleanText('/Users/nbergam/Desktop/AmericanModernism/webDeploy/uploads/SoundAndFury.txt')
    pos = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    savePOSPiChart(text2, pos)
    top = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    saveTopWords(text2, top)
    return render_template('results.html', pq = percentQuotes(text), sen = senlenStats(text), pos = pos, top = top)

#---Double Text

@app.route('/double')
def double():
	return render_template('twoText.html')

@app.route('/double-results', methods=['GET', 'POST'])
def doubleResults():
    return render_template('double-results.html')

#---Multi Text

@app.route('/multi')
def multi():
    return render_template('multiText.html')

#---Thesis

@app.route('/thesis')
def student():
   return render_template('thesis.html')

@app.route('/thesis-result', methods = ['GET', 'POST'])
def result():
    e = request.form.to_dict()

    verbs = deList( e['cv'] )
    nouns = deList( e['cn'] )
    thesis = e['thesis']

    vector = thesisVector(thesis, nouns, verbs)

    return render_template('thesis-results.html', vector = vector)
  # if request.method == 'POST':
      #result = request.form
      #return request.form

@app.route('/layout')
def layout():
    return render_template('layout.html')


@app.route('/projects')
def projects():
    return render_template('projects.html')
