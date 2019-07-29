import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from flask import render_template

from simpleFunctions import *

from thesis import thesisVector

from twoText import wpReport
from twoText import plotChronoMap

from reports import *
import matplotlib.pyplot as plt, mpld3

import random
import string

import nltk


branch = '/Users/JulianMacBookPro/Desktop/AmericanModernism/webDeploy'


priorUrl = '/single'
fname = "abc"
app = Flask(__name__, static_folder=os.path.abspath(branch+'/templates/static') )
if __name__ == '__main__':
    app.run(debug=True)
    app.debug = True
    app.secret_key = "vkjgvkgv"

UPLOAD_FOLDER = branch + '/uploads'
GRAPHS_FOLDER = branch + '/templates/static/graphs'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['GRAPHS_FOLDER'] = GRAPHS_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('hello.html')

failedUpload = 0
@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    global fname
    global failedUpload
    global priorUrl
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            failedUpload = 1
            return redirect(priorUrl)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            failedUpload = 1
            return redirect(priorUrl)
        if file and allowed_file(file.filename):
            fname = secure_filename(file.filename)
            print( fname)
            failedUpload = 0
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
            # where you go after uploading
            return redirect(priorUrl)
    failedUpload = 1
    return redirect(priorUrl)#render_template(type+'.html')

from flask import send_from_directory

@app.route(branch+'/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

#---Single Text

@app.route('/single')
def single():
    global failedUpload
    dict = getWordFreqDict(200)
    global priorUrl
    priorUrl = '/single'
    uploadFailed = failedUpload
    failedUpload = 0
    print(uploadFailed);
    return render_template('oneText.html',fail = uploadFailed)


@app.route('/report', methods=['GET', 'POST'])
def get_file():
    global fname
    # need to retrieve the uploaded file here for further processing
    print( fname)
    dict = request.form.to_dict()
    #filename =  str(request)[ str(request).index('=')+1 : str(request).index('\' [GET]>') ]
    text = simpleTokenize( 'uploads/' + fname )
    text2  = cleanText( 'uploads/' + fname )
    if "PercentQuotes" in dict:
        pq = percentQuotes(text)
    else:
        pq = -1
    if "SLength" in dict:
        sen = senlenStats(text)
    else:
        sen = -1
    if "POS" in dict:
        print("creating pos chart")
        pos = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))#title of the generated chart
        savePOSPiChart(text2, pos)
    else:
        pos = "1"
    if "TopWords" in dict:
        print("creating top words chart")
        top = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        #os.unlink(os.path.join( app.config['GRAPHS_FOLDER'], top + ".png"))
        #os.unlink(branch+"/templates/static/graphs/" + top + ".png")
        #item_id = branch+"/templates/static/graphs/" + top + ".png"
        #item = self.session.query(Item).get(item_id)
        #self.session.delete(item)
        #db.session.commit()
        #os.remove(branch+"/templates/static/graphs/" + top + ".png");
        saveTopWords(text2, top)
    else:
        top = "1"
    if "WordProg" in dict:
        print("creating word progression chart")
        wp = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        arr = dict["WordProgWords"].replace(" ", "").split(';')
        groups = []
        for i in range(len(arr)):
            groups.append(arr[i].split(','))
        oneTextPlotChronoMap(text2,groups,wp)
    """
    bw = ['yellow', 'fish', 'glass', 'foot', 'beach', 'suicide']
    genGraph = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    secgen = similarContext( text,  bw)
    print("c")
    saveChronoMap(text, bw, secgen, genGraph)
    genReport = wpReport(text, bw, secgen, 10)

    charReport = sampleCharacter(text, 'Caddy', 3, 100)
    print("d")"""

    return render_template('results.html', pq = pq, sen = sen, wp = wp, pos = pos, top = top)#mpld3.fig_to_html(topFig))
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
    thisWarning = False
    if 'this' in thesis:
        thisWarning = True
    vector = thesisVector(thesis, nouns, verbs)
    return render_template('thesis-results.html', thesis=thesis, vector = vector, thisWarning=thisWarning)
  # if request.method == 'POST':
      #result = request.form
      #return request.form

@app.route('/layout')
def layout():
    return render_template('layout.html')


@app.route('/projects')
def projects():
    return render_template('projects.html')
