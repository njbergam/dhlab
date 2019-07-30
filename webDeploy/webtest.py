import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from flask import render_template

from simpleFunctions import cleanText
from simpleFunctions import simpleTokenize
from simpleFunctions import detokenize
from simpleFunctions import percentQuotes
from simpleFunctions import senlenStats
from simpleFunctions import savePOSPiChart
from simpleFunctions import deList
from simpleFunctions import saveTopWords
from simpleFunctions import getWordFreqDict

from thesis import thesisVector

from twoText import wpReport
from twoText import plotChronoMap

from reports import wpReport
from reports import similarContext
from reports import saveChronoMap
from reports import sampleCharacter
import matplotlib.pyplot as plt, mpld3

import random
import string
import json

import nltk
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('universal_tagset')

branch = '/Users/Justin/Desktop/AmericanModernism/webDeploy'


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

@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    global fname
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
            fname = secure_filename(file.filename)
            print( fname)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
            # where you go after uploading
            global priorUrl
            return redirect(priorUrl)
    return redirect(request.url)#render_template(type+'.html')

from flask import send_from_directory

@app.route(branch+'/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

#---Single Text

@app.route('/single')
def single():
    dict = getWordFreqDict(200)
    global priorUrl
    priorUrl = '/single'
    return render_template('oneText.html')


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
    """
    bw = ['yellow', 'fish', 'glass', 'foot', 'beach', 'suicide']
    genGraph = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    secgen = similarContext( text,  bw)
    print("c")
    saveChronoMap(text, bw, secgen, genGraph)
    genReport = wpReport(text, bw, secgen, 10)
    charReport = sampleCharacter(text, 'Caddy', 3, 100)
    print("d")"""

    return render_template('results.html', pq = pq, sen = sen, pos = pos, top = top)#mpld3.fig_to_html(topFig))
#---Double Text

@app.route('/double')
def double():
	return render_template('twoText.html')

@app.route('/double-results', methods=['GET', 'POST'])
def doubleResults():
    return render_template('double-results.html')

#---Multi Text

global files
files = []

@app.route('/multi-comp')
def multi():
    global priorUrl
    priorUrl = '/multi-comp'
    print(files)
    return render_template('multi-comp.html', files = files)

@app.route('/upload_multifile', methods=['GET', 'POST'])
def upload_multifile():
    global fname
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
            fname = secure_filename(file.filename)
            files.append(fname)
            print(files)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
            # where you go after uploading
            global priorUrl
            return redirect(priorUrl)
    return redirect(request.url)#render_template(type+'.html')

@app.route('/removefile', methods = ['GET'])
def worker():
    global files
    # read json + reply
    removedfile=request.args.get('filename')
    print (removedfile)
    files.remove(removedfile)
    return redirect('/multi-comp')


@app.route('/multireport', methods=['GET', 'POST'])
def get_multifile():
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
    """
    bw = ['yellow', 'fish', 'glass', 'foot', 'beach', 'suicide']
    genGraph = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    secgen = similarContext( text,  bw)
    print("c")
    saveChronoMap(text, bw, secgen, genGraph)
    genReport = wpReport(text, bw, secgen, 10)
    charReport = sampleCharacter(text, 'Caddy', 3, 100)
    print("d")"""

    return render_template('results.html', pq = pq, sen = sen, pos = pos, top = top)#mpld3.fig_to_html(topFig))


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
