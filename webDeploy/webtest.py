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

#error checking
failedSingle = 0
failedMulti = 0

priorUrl = '/single'
fname = ""
app = Flask(__name__, static_folder=os.path.abspath(branch+'/templates/static') )
if __name__ == '__main__':
    app.run(debug=True)
    app.debug = True
    app.secret_key = "vkjgvkgv"

UPLOAD_FOLDER = branch + '/uploads'
GRAPHS_FOLDER = branch + '/templates/static/graphs'
ALLOWED_EXTENSIONS = set(['txt', 'pdf'])


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
    global failedSingle
    global priorUrl
    if request.method == 'POST':
        # check if the post request has the file part
        if bool(request.files) == False:
            failedSingle = 3
            return redirect(priorUrl)
        print("b")
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            failedSingle = 1
            return redirect(priorUrl)
        if file and allowed_file(file.filename):
            failedSingle = 0
            fname = secure_filename(file.filename)
            if fname[len(fname)-4:] == ".pdf":
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
                txt = text_extractor(UPLOAD_FOLDER+"/"+fname)
                fname = fname[:len(fname)-4] + ".txt"
                with open(UPLOAD_FOLDER + "/"+ fname,"w") as fo:
                   fo.write(txt)
                   fo.close()
            else:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
            # where you go after uploading
            return redirect(priorUrl)
    failedSingle = 1
    return redirect(priorUrl)#render_template(type+'.html')

from flask import send_from_directory

@app.route(branch+'/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

#---Single Text
@app.route('/single')
def single():
    global failedSingle
    global priorUrl
    priorUrl = '/single'
    fail = failedSingle
    failedSingle = 0
    return render_template('oneText.html',fail = fail, fname=fname)

class txtResult:
  def __init__(self, name, pq, sen, wp, pos, top):
    self.name = name
    self.pq = pq
    self.sen = sen
    self.wp = wp
    self.pos = pos
    self.top = top

@app.route('/report', methods=['GET', 'POST'])
def report():
    global fname
    global failedSingle
    if fname == "":
        failedSingle = 2
        return redirect('/single')
    # need to retrieve the uploaded file here for further processing
    dict = request.form.to_dict()
    #filename =  str(request)[ str(request).index('=')+1 : str(request).index('\' [GET]>') ]
    text = simpleTokenize( 'uploads/' + fname )
    #getNames('uploads/' + fname)
    text2  = cleanText( 'uploads/' + fname )
    textRst = txtResult(fname,-1,-1,"1","1","1")
    if "PercentQuotes" in dict:
        textRst.pq = percentQuotes(text)
    if "SLength" in dict:
        textRst.sen = senlenStats(text)
    if "POS" in dict:
        print("creating pos chart")
        textRst.pos = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))#title of the generated chart
        savePOSPiChart(text2, textRst.pos)
    if "TopWords" in dict:
        print("creating top words chart")
        textRst.top = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
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
        textRst.wp = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        arr = dict["WordProgWords"].replace(" ", "").split(';')
        groups = []
        for i in range(len(arr)):
            groups.append(arr[i].split(','))
        oneTextPlotChronoMap(text2,groups,textRst.wp)
    fname = ""
    return render_template('results.html', result = textRst)#mpld3.fig_to_html(topFig))
#---Multi Text

global files
files = []

@app.route('/multi-comp')
def multi():
    global failedMulti
    print(failedMulti)
    fail = failedMulti
    failedMulti = 0
    global priorUrl
    priorUrl = '/multi-comp'
    print(files)
    return render_template('multi-comp.html', files = files, fail = fail)

@app.route('/upload_multifile', methods=['GET', 'POST'])
def upload_multifile():
    global fname
    global failedMulti
    global priorUrl
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            failedMulti = 3
            return redirect(priorUrl)
        file = request.files['file']

        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            failedMulti = 1
            return redirect(request.url)
        if file and allowed_file(file.filename):
            fname = secure_filename(file.filename)
            files.append(fname)
            print(files)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
            # where you go after uploading
            failedMulti = 0
            return redirect(priorUrl)
    failedMulti = 1
    return redirect(priorUrl)#render_template(type+'.html')

@app.route('/removefile', methods = ['GET'])
def worker():
    global files
    # read json + reply
    removedfile=request.args.get('filename')
    print (removedfile)
    files.remove(removedfile)
    return redirect('/multi-comp')

@app.route('/reportMulti', methods=['GET', 'POST'])
def multiReport():
    global files
    global failedMulti
    if len(files) == 0:#error checking
        failedMulti = 2
        return redirect('/multi-comp')
    dict = request.form.to_dict()
    text = []
    text2 = []
    textRsts = []
    for i in range(len(files)):
        text.append(simpleTokenize( 'uploads/' + files[i] ))
        text2.append(cleanText( 'uploads/' + files[i] ))
        textRsts.append(txtResult(files[i],-1,-1,"1","1","1"))
    if "PercentQuotes" in dict:
        for i in range(len(files)):
            textRsts[i].pq = percentQuotes(text[i])
    if "SLength" in dict:
        for i in range(len(files)):
            textRsts[i].sen = senlenStats(text[i])
    if "POS" in dict:
        print("creating pos chart")
        for i in range(len(files)):
            textRsts[i].pos = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))#title of the generated chart
            savePOSPiChart(text2[i], textRsts[i].pos)
    if "TopWords" in dict:
        print("creating top words chart")
        for i in range(len(files)):
            textRsts[i].top = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            saveTopWords(text2[i], textRsts[i].top)
    if "WordProg" in dict:
        print("creating word progression chart")
        for i in range(len(files)):
            textRsts[i].wp = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            arr = dict["WordProgWords"].replace(" ", "").split(';')
            groups = []
            for j in range(len(arr)):
                groups.append(arr[j].split(','))
            oneTextPlotChronoMap(text2[i],groups,textRsts[i].wp)
    for i in range(len(textRsts)):
        print(textRsts[i].pq)
    return render_template('multiResults.html',results = textRsts)
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
