import os
import flask
import requests
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery

from googleapiclient.discovery import build
from werkzeug.utils import secure_filename
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template

from simpleFunctions import *

from thesis import thesisVector

from twoText import wpReport
from twoText import plotChronoMap
from twoText import overlap

from character import samplePassage

from readability import flesch_read
from readability import flesch_kincaid_read
from readability import fog_read

from reports import *
import matplotlib.pyplot as plt, mpld3

import random
import string
import json

import nltk

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'#necessary to run locally

"""nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('universal_tagset')"""

branch = '/Desktop/AmericanModernism'

app = flask.Flask(__name__, static_folder=os.path.abspath(branch+'/templates/static') )
app.secret_key = "vkjgvkgv"
if __name__ == '__main__':
    app.run(debug=True)
    app.debug = True

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
    if request.method == 'POST':
        # check if the post request has the file part
        if bool(request.files) == False:
            flask.session['failedSingle'] = 3
            return redirect(flask.session['priorUrl'])
        print("b")
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            flask.session['failedSingle'] = 1
            return redirect(flask.session['priorUrl'])
        if file and allowed_file(file.filename):
            flask.session['failedSingle'] = 0
            flask.session['fname'] = secure_filename(file.filename)
            flask.session['fnameDisplay'] = flask.session['fname']
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], flask.session['fname']))
            # where you go after uploading
            return redirect(flask.session['priorUrl'])
    flask.session['failedSingle'] = 1
    return redirect(flask.session['priorUrl'])#render_template(type+'.html')

from flask import send_from_directory

@app.route(branch+'/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

#---Single Text
@app.route('/single')
def single():
    flask.session['priorUrl'] = '/single'
    if 'failedSingle' not in flask.session:
        fail = 0
    else:
        fail = flask.session['failedSingle']
    flask.session['failedSingle'] = 0
    if 'fname' not in flask.session:
        flask.session['fname'] = ""
    if "fnameDisplay" not in flask.session:
        fnameDisplay = ''
    else:
        fnameDisplay = flask.session['fnameDisplay']
    flask.session['fnameDisplay'] =''
    return render_template('oneText.html',fail = fail, fname=fnameDisplay)

class txtResult:
  def __init__(self, name, pq, sen, wp, pos, top):
    self.name = name
    self.pq = pq
    self.sen = sen
    self.wp = wp
    self.pos = pos
    self.top = top

@app.route('/report', methods=['GET', 'POST'])
def get_file():
    if flask.session['fname'] == "":
        flask.session['failedSingle'] = 2
        return redirect('/single')
    # need to retrieve the uploaded file here for further processing
    dict = request.form.to_dict()
    if flask.session['fname'][-4:] == '.pdf':
        text = text_extractor('uploads/' +flask.session['fname'])
        text2 = cleanText2(text)
    else:
        #filename =  str(request)[ str(request).index('=')+1 : str(request).index('\' [GET]>') ]
        text = simpleTokenize( 'uploads/' + flask.session['fname'] )
        #getNames('uploads/' + fname)
        text2  = cleanText( 'uploads/' + flask.session['fname'] )
    textRst = txtResult(flask.session['fname'],-1,-1,"1","1","1")
    if "PercentQuotes" in dict:
        textRst.pq = percentQuotes(text)
        print("getting percent quotes")
    if "SLength" in dict:
        textRst.sen = senlenStats(text)
        print("sentence length")
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
    flask.session['fname'] = ""
    print(textRst.pos);
    print(textRst.wp);
    print(textRst.top);
    return render_template('results.html', result = textRst)#mpld3.fig_to_html(topFig))

#---Multi Text

@app.route('/allusions')
def allusions():
    return render_template('dev.html')

@app.route('/multi-comp')
def multi():
    if 'failedMulti' not in flask.session:
        fail = 0
    else:
        fail = flask.session['failedMulti']
    flask.session['priorUrl'] = '/multi-comp'
    if 'files' not in flask.session:
        files = []
        flask.session['files'] = []
    else:
        files = flask.session['files']
    return render_template('multi-comp.html', files = files, fail = fail)

@app.route('/upload_multifile', methods=['GET', 'POST'])
def upload_multifile():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flask.session['failedMulti'] = 3
            return redirect(flask.session['priorUrl'])
        file = request.files['file']

        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            flask.session['failedMulti'] = 1
            return redirect(request.url)
        if file and allowed_file(file.filename):
            flask.session['fname'] = secure_filename(file.filename)
            if 'files' not in flask.session:
                flask.session['files'] = []
            flask.session['files'].append(flask.session['fname'])
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], flask.session['fname']))
            # where you go after uploading
            flask.session['failedMulti'] = 0
            return redirect(flask.session['priorUrl'])
    flask.session['failedMulti'] = 1
    return redirect(flask.session['priorUrl'])#render_template(type+'.html')

@app.route('/removefile', methods = ['GET'])
def worker():
    # read json + reply
    removedfile=request.args.get('filename')
    print (removedfile)
    flask.session['files'].remove(removedfile)
    return redirect('/multi-comp')

@app.route('/reportMulti', methods=['GET', 'POST'])
def multiReport():
    if len(flask.session['files']) == 0:#error checking
        flask.session['failedMulti'] = 2
        return redirect('/multi-comp')
    dict = request.form.to_dict()
    text = []
    text2 = []
    textRsts = []
    for i in range(len(flask.session['files'])):
        print("HOLLAA")
        print(flask.session['fname'][i])
        if flask.session['fname'][i][-4:] == '.pdf':
            text.append(text_extractor( 'uploads/' + flask.session['files'][i] ))
            text2.append(cleanText2( 'uploads/' + flask.session['files'][i] ))
        else:
            text.append(simpleTokenize( 'uploads/' + flask.session['fname'][i] ))
            text2.append(cleanText( 'uploads/' + flask.session['fname'][i] ))
        textRsts.append(txtResult(flask.session['files'][i],-1,-1,"1","1","1"))
    if "PercentQuotes" in dict:
        for i in range(len(flask.session['files'])):
            textRsts[i].pq = percentQuotes(text[i])
    if "SLength" in dict:
        for i in range(len(flask.session['files'])):
            textRsts[i].sen = senlenStats(text[i])
    if "POS" in dict:
        print("creating pos chart")
        for i in range(len(flask.session['files'])):
            textRsts[i].pos = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))#title of the generated chart
            savePOSPiChart(text2[i], textRsts[i].pos)
    if "TopWords" in dict:
        print("creating top words chart")
        for i in range(len(flask.session['files'])):
            textRsts[i].top = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            saveTopWords(text2[i], textRsts[i].top)
    overlapCharts = []
    overlapInfo = []
    if "over" in dict:
        print("creating overlap chart")
        k = int(len(flask.session['files'])*(len(flask.session['files'])-1)/2+0.5)
        for i in range(k):
            overlapCharts.append(''.join(random.choices(string.ascii_uppercase + string.digits, k=10)))
        overlap(text2, overlapCharts)
        l = 0
        for i in range(len(flask.session['files'])):
            for j in range(i+1,len(flask.session['files'])):
                temp = []
                temp.append(str(flask.session['files'][i]) + " and " + str(flask.session['files'][j]))
                temp.append(overlapCharts[l])
                l += 1
                overlapInfo.append(temp)
    else:
        overlapCharts.append("1")
    if "WordProg" in dict:
        print("creating word progression chart")
        for i in range(len(flask.session['files'])):
            textRsts[i].wp = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            arr = dict["WordProgWords"].replace(" ", "").split(';')
            groups = []
            for j in range(len(arr)):
                groups.append(arr[j].split(','))
            oneTextPlotChronoMap(text2[i],groups,textRsts[i].wp)
    for i in range(len(textRsts)):
        print(textRsts[i].pq)
        print("a")
    return render_template('multiResults.html',results = textRsts, overlap = overlapInfo)

#---Thesis and Essay Help

@app.route('/thesis')
def student():
    return render_template('thesis.html')

@app.route('/passage', methods=['GET', 'POST'])
def passage():
    fname = flask.session['fname']
    flask.session['priorUrl'] = '/passage'
    if "fnameDisplay" not in flask.session:
        fnameDisplay = ''
    else:
        fnameDisplay = flask.session['fnameDisplay']
    flask.session['fnameDisplay'] =''
    return render_template('passage.html', fname =  fnameDisplay)

@app.route('/passage-results', methods=['GET', 'POST'])
def passageResults():
    fname = flask.session['fname']
    print (fname)
    dict = request.form.to_dict()
    print (dict)
    passages = samplePassage(simpleTokenize("uploads/" + fname), dict["term"], dict["numSamp"], dict["wordCount"])
    return render_template('passageResults.html', passages = passages)

@app.route('/thesis-result', methods = ['GET', 'POST'])
def result():
    raw_text = request.form.to_dict()
    print(raw_text.keys())
    print(POSColor(raw_text['thesis']))
    pos_text = [POSColor(raw_text[name]) for name in raw_text.keys()]
    readability = [ read_score(name, text) for name, text in raw_text.items() ]
    return render_template('thesis-results.html', pos_text=pos_text,raw_text=raw_text, readability=readability)

# Returns array of all reading scores for a given text
def read_score(name,text):
    ret = [ name]
    ret.extend( ['Flesch Readability', flesch_read(text)] )
    ret.extend( ['Flesch-Kincaid Readability', flesch_kincaid_read(text)] )
    ret.extend( ['Fog Readability', fog_read(text)] )
    return ret

@app.route('/layout')
def layout():
    return render_template('layout.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

#---School texts

class textInfo ():
    def __init__(self, title, author, txtName, pdfName, image):
        self.title = title
        self.author = author
        self.txtName = txtName
        self.pdfName = pdfName
        self.image = image

ninthTexts=[
    textInfo("The Absolutely True Diary of a Part-Time Indian", "Sherman Alexie", "PartTimeIndian.txt", "PartTimeIndian.pdf", ""),
    textInfo("Catcher in the Rye", "JD Salinger", "CatcherSalinger.txt", "CatcherSalinger.pdf", "https://images-na.ssl-images-amazon.com/images/I/51EqnTkohBL._SX307_BO1,204,203,200_.jpg"),
    textInfo("As I Lay Dying", "William Faulkner", "AILDFaulkner.txt", "AILDFaulkner.pdf", "https://images-na.ssl-images-amazon.com/images/I/91yR2PB%2B2KL.jpg"),
    textInfo("Othello", "William Shakespeare", "othello.text","othello.pdf", ""),
    textInfo("Oedipus Rex", "Sophocles", "oedipusRex.txt", "oedipusRex.pdf", ""),
    textInfo("Oedipus at Colonus", "Sophocles", "oedipusColonus.txt", "oedipusColonus.pdf", ""),
    textInfo("Antigone", "Sophocles", "antigone.txt", "antigone.pdf", ""),
    textInfo("Master Harold and the Boys", "Athol Fugard", "masterHarold.txt", "masterHarold.pdf", ""),
    textInfo("Death of a Salesman", "Arthur Miller", "deathOfASalesman.txt", "deathOfASalesman.pdf", ""),
    textInfo("Their Eyes Were Watching God", "Zora Neale Hurston", "theirEyesWereWatchingGod.txt", "theirEyesWereWatchingGod.pdf", ""),
]
tenthTexts=[
    textInfo("Balzac and the Little Chinese Seamstress", "Dai Sijie", "balzac.txt", "balzac.pdf", ""),
    textInfo("White Tiger", "Aravind Adiga", "WhiteTiger.txt", "whitetiger.pdf", ""),
    textInfo("Beowulf", "Unknown Author", "beowulf.txt", "beowulf.pdf", ""),
    textInfo("Go Tell It On The Mountain", "James Baldwin", "goTellItOnTheMountain.txt", "goTellItOnTheMountain.txt", ""),
    textInfo("Jane Eyre", "Charlotte Brontë", "janeeyre.txt", "janeeyre.pdf", ""),
    textInfo("Grendel", "John Gardner", "grendel.txt", "grendel.pdf", ""),
    textInfo("Wide Sargasso Sea", "Jean Rhys", "wideSargassoSea.txt", "wideSargassoSea.pdf", ""),
    textInfo("Macbeth", "William Shakespeare", "macbeth.txt", "macbeth.pdf", ""),
    textInfo("Blood Dazzler", "Patricia Smith", "bloodDazzler.txt", "bloodDazzler.pdf", ""),
    textInfo("Heidi Chronicles", "Wendy Wasserstein", "heidiChronicles.txt", "heidiChronicles.pdf", ""),
    textInfo("A Streetcar Named Desire", "Tennessee Williams", "astreecarNamedDesire.txt", "astreecarNamedDesire.pdf", "")
]
eleventhTexts=[]
twelfth=[]

@app.route('/downloads')
def downloads():
    if 'email' not in flask.session:
        flask.session['priorUrl'] = '/downloads'
        return flask.redirect('/getUser')
    if flask.session['email'][-10:] == "pingry.org":
        return render_template('downloads.html', ninthTexts = ninthTexts, tenthTexts=tenthTexts,eleventhTexts=eleventhTexts )
    else:
        del flask.session['email']
        del flask.session['credentials']
        return render_template('askLogin.html', fail = 1)

@app.route('/downloadbooks/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    return send_from_directory(directory=app.config['UPLOAD_FOLDER'], filename = filename)



@app.route('/getUser')
def getUser():
    if 'credentials' not in flask.session:
        return render_template('askLogin.html', fail = 0)
    credentials = google.oauth2.credentials.Credentials(**flask.session['credentials'])
    drive = build('drive', 'v2', credentials=credentials)
    userInfo = drive.about().get().execute()
    #attrs = vars(userInfo)
    #for item in attrs.items():
    #    print(item)
    flask.session['priorUrl'] = '/downloads'
    print(userInfo["user"]["emailAddress"])
    flask.session['email'] = userInfo["user"]["emailAddress"]
    return flask.redirect(flask.session['priorUrl'])

@app.route('/authorize')
def authorize():
    #flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('client_secret.json',scopes=['https://www.googleapis.com/auth/drive.metadata.readonly'],code_verifier='128buoABUFU01189fhUA021uAFHJA102810hf3rfsdboq031rfd')
    #flow.redirect_uri = 'http://localhost:5000/oauth_callback'
    oauth2_session, client_config = google_auth_oauthlib.helpers.session_from_client_secrets_file('client_secret.json',scopes=['https://www.googleapis.com/auth/drive.file'])
    flow = google_auth_oauthlib.flow.Flow(oauth2_session, client_type='web', client_config=client_config, redirect_uri='http://localhost:5000/oauth_callback', code_verifier='128buoABUFU01189fhUA021uAFHJA102810hf3rfsdboq031rfd')
    authorization_url, state = flow.authorization_url(access_type='offline')# Enable offline access so that you can refresh an access token without re-prompting the user for permission. Recommended for web server apps.#,include_granted_scopes='true'
    print("state:")
    print(state)
    flask.session['state'] = state
    return flask.redirect(authorization_url)

@app.route('/oauth_callback')
def oauth_callback():
    #state = flask.session['state']
    oauth2_session, client_config = google_auth_oauthlib.helpers.session_from_client_secrets_file('client_secret.json',scopes=['https://www.googleapis.com/auth/drive.file'])
    flow = google_auth_oauthlib.flow.Flow(oauth2_session, client_type='web', client_config=client_config, redirect_uri='http://localhost:5000/oauth_callback', code_verifier='128buoABUFU01189fhUA021uAFHJA102810hf3rfsdboq031rfd')
    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials
    flask.session['credentials'] = credentials_to_dict(credentials)
    return flask.redirect('/getUser')

@app.route('/clear')
def clear_credentials():
    if 'credentials' in flask.session:
        del flask.session['credentials']
    if 'email' in flask.session:
        del flask.session['email']
    return flask.redirect('/')

def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
            }
