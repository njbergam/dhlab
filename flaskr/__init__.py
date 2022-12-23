import os
import requests
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
from googleapiclient.discovery import build
from werkzeug.utils import secure_filename
from flask import Flask, session, flash, request, redirect, url_for, render_template
# Talisman is used for security reasons - has much more use we aren't currently tapping into
# from flask_talisman import Talisman
from flask_session.__init__ import Session
import matplotlib.pyplot as plt, mpld3
import random
import string
import json
import nltk

from .tools.simple_analytics import *
from .tools.vars import branch, UPLOAD_FOLDER, GRAPHS_FOLDER, ALLOWED_EXTENSIONS
from .tools.txtresult import txtResult

# branch = "/Users/someone/Desktop/dhlab/flaskr"
# ^ Running on local device ()
# branch = "/var/www/html"
# ^ Running on the remote server
branch = os.path.abspath(__file__)[0:-12]


def create_app(test_config=None):

    ############################
    ###  APP CONFIGURATION   ###
    ############################

    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        # Not-so-secret key
        SECRET_KEY='password',
        # Defines path to database used in db.py
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    # Does nothing for now -- can be used to load a config from the test_config
    # e.g. setting an actual secret_key
    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Allows OAuth to work with http instead of https
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    ############################
    ###  SETUP LIBRARIES/BP  ###
    ############################

    # Prepare the sqlalchemy object to work with the application object
    # Necessary because app is defined locally and sqlalchemy is defined globally
    # Imports from the ./db.py file
    from . import db
    db.init_app(app)

    # Sets up authentication framework using blueprints -- organization tool
    # Loads module from ./auth.py
    from . import auth
    app.register_blueprint(auth.bp)

    # Blueprint that provides functionality for blog posts
    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/blog', endpoint='index')

    ############################
    ###    WEBPAGE ROUTES    ###
    ############################

    # Register the multi-page system
    from .blueprints.multifile import multifile
    app.register_blueprint(multifile)

    from .blueprints.singlefile import singlefile
    app.register_blueprint(singlefile)

    from .blueprints.projects import p
    app.register_blueprint(p)

    from .blueprints.writerly import writerly
    app.register_blueprint(writerly)

    # Mainpage route that contains basic information about the app
    @app.route('/', methods=['GET', 'POST'])
    def home():
        return render_template('hello.html')

    #--- Multi Text

    # Simply explaining what to do with the app and how it works.
    @app.route('/howTo')
    def howTo():
        return render_template('howTo.html')

    # TODO: make something here I guess
    @app.route('/allusions')
    def allusions():
        return render_template('dev.html')

    # TODO: make generative models work on the website
    @app.route('/generative', methods=['GET', 'POST'])
    def gen():
        return render_template('generative.html')

    #---Thesis and Essay Help

    # Landing page for thesis help
    @app.route('/thesis')
    def student():
        return render_template('thesis.html')


    # Landing page for essay help, displayed with color coded essay text
    @app.route('/thesis-result', methods=['GET', 'POST'])
    def result():
        raw_text = request.form.to_dict()
        print(raw_text.keys())
        print(POSColor(raw_text['thesis']))
        pos_text = [POSColor(raw_text[name]) for name in raw_text.keys()]
        readability = [
            read_score(name, text) for name, text in raw_text.items()
        ]
        return render_template('thesis-results.html',
                               pos_text=pos_text,
                               raw_text=raw_text,
                               readability=readability)

    # Returns array of all reading scores for a given text
    def read_score(name, text):
        ret = [name]
        ret.extend(['Flesch Readability', flesch_read(text)])
        ret.extend(['Flesch-Kincaid Readability', flesch_kincaid_read(text)])
        ret.extend(['Fog Readability', fog_read(text)])
        return ret

    @app.route('/layout')
    def layout():
        return render_template('layout.html')

    # # Landing page for the projects page
    # @app.route('/projects')
    # def projects():
    #     return render_template('projects.html')

    # # Route to serve the JSON file containing
    # @app.route('/projectData')
    # def projectData():
    #     return app.send_static_file("projects.json")

    #---School texts

    class textInfo():
        def __init__(self, title, author, txtName, pdfName, image):
            self.title = title
            self.author = author
            self.txtName = txtName
            self.pdfName = pdfName
            self.image = image

    ninthTexts = [
        textInfo("The Absolutely True Diary of a Part-Time Indian",
                 "Sherman Alexie", "PartTimeIndian.txt", "PartTimeIndian.pdf",
                 ""),
        textInfo(
            "Catcher in the Rye", "JD Salinger", "CatcherSalinger.txt",
            "CatcherSalinger.pdf",
            "https://images-na.ssl-images-amazon.com/images/I/51EqnTkohBL._SX307_BO1,204,203,200_.jpg"
        ),
        textInfo(
            "As I Lay Dying", "William Faulkner", "AILDFaulkner.txt",
            "AILDFaulkner.pdf",
            "https://images-na.ssl-images-amazon.com/images/I/91yR2PB%2B2KL.jpg"
        ),
        textInfo("Othello", "William Shakespeare", "othello.text",
                 "othello.pdf", ""),
        textInfo("Oedipus Rex", "Sophocles", "oedipusRex.txt",
                 "oedipusRex.pdf", ""),
        textInfo("Oedipus at Colonus", "Sophocles", "oedipusColonus.txt",
                 "oedipusColonus.pdf", ""),
        textInfo("Antigone", "Sophocles", "antigone.txt", "antigone.pdf", ""),
        textInfo("Master Harold and the Boys", "Athol Fugard",
                 "masterHarold.txt", "masterHarold.pdf", ""),
        textInfo("Death of a Salesman", "Arthur Miller",
                 "deathOfASalesman.txt", "deathOfASalesman.pdf", ""),
        textInfo("Their Eyes Were Watching God", "Zora Neale Hurston",
                 "theirEyesWereWatchingGod.txt",
                 "theirEyesWereWatchingGod.pdf", ""),
    ]
    tenthTexts = [
        textInfo("Balzac and the Little Chinese Seamstress", "Dai Sijie",
                 "balzac.txt", "balzac.pdf", ""),
        textInfo("White Tiger", "Aravind Adiga", "WhiteTiger.txt",
                 "whitetiger.pdf", ""),
        textInfo("Beowulf", "Unknown Author", "beowulf.txt", "beowulf.pdf",
                 ""),
        textInfo("Go Tell It On The Mountain", "James Baldwin",
                 "goTellItOnTheMountain.txt", "goTellItOnTheMountain.txt", ""),
        textInfo("Jane Eyre", "Charlotte Brontë", "janeeyre.txt",
                 "janeeyre.pdf", ""),
        textInfo("Grendel", "John Gardner", "grendel.txt", "grendel.pdf", ""),
        textInfo("Wide Sargasso Sea", "Jean Rhys", "wideSargassoSea.txt",
                 "wideSargassoSea.pdf", ""),
        textInfo("Macbeth", "William Shakespeare", "macbeth.txt",
                 "macbeth.pdf", ""),
        textInfo("Blood Dazzler", "Patricia Smith", "bloodDazzler.txt",
                 "bloodDazzler.pdf", ""),
        textInfo("Heidi Chronicles", "Wendy Wasserstein",
                 "heidiChronicles.txt", "heidiChronicles.pdf", ""),
        textInfo("A Streetcar Named Desire", "Tennessee Williams",
                 "astreecarNamedDesire.txt", "astreecarNamedDesire.pdf", "")
    ]
    eleventhTexts = []
    twelfth = []

    @app.route('/downloads')
    def downloads():
        if 'email' not in session:
            session['priorUrl'] = '/downloads'
            return redirect('/getUser')

        if session['email'][-10:] == "pingry.org":
            return render_template('downloads.html',
                                   ninthTexts=ninthTexts,
                                   tenthTexts=tenthTexts,
                                   eleventhTexts=eleventhTexts)
        else:
            del session['email']
            del session['credentials']
            return render_template('askLogin.html', fail=1)

    @app.route('/downloadbooks/<path:filename>', methods=['GET', 'POST'])
    def download(filename):
        return send_from_directory(directory=app.config['UPLOAD_FOLDER'],
                                   filename=filename)

    @app.route('/getUser')
    def getUser():
        if 'credentials' not in session:
            return render_template('askLogin.html', fail=0)
        credentials = google.oauth2.credentials.Credentials(
            **session['credentials'])
        drive = build('drive', 'v2', credentials=credentials)
        userInfo = drive.about().get().execute()
        #attrs = vars(userInfo)
        #for item in attrs.items():
        #    print(item)
        session['priorUrl'] = '/downloads'
        print(userInfo["user"]["emailAddress"])
        session['email'] = userInfo["user"]["emailAddress"]
        return redirect(session['priorUrl'])

    @app.route('/authorize')
    def authorize():
        #flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('client_secret.json',scopes=['https://www.googleapis.com/auth/drive.metadata.readonly'],code_verifier='128buoABUFU01189fhUA021uAFHJA102810hf3rfsdboq031rfd')
        oauth2_session, client_config = google_auth_oauthlib.helpers.session_from_client_secrets_file(
            'flaskr/client_secret.json',
            scopes=['https://www.googleapis.com/auth/drive.file'])
        flow = google_auth_oauthlib.flow.Flow(
            oauth2_session,
            client_type='web',
            client_config=client_config,
            redirect_uri='http://dhlab.pingry.org:8000/oauth_callback',
            code_verifier='128buoABUFU01189fhUA021uAFHJA102810hf3rfsdboq031rfd'
        )
        # flow.redirect_uri = 'http://localhost:5000/oauth_callback' # GET RID OF THIS LINE WHEN DEPLOYING
        authorization_url, state = flow.authorization_url(
            access_type='offline'
        )  # Enable offline access so that you can refresh an access token without re-prompting the user for permission. Recommended for web server apps.#,include_granted_scopes='true'
        print("state:")
        print(state)
        session['state'] = state
        return redirect(authorization_url)

    @app.route('/oauth_callback')
    def oauth_callback():
        #state = session['state']
        oauth2_session, client_config = google_auth_oauthlib.helpers.session_from_client_secrets_file(
            'flaskr/client_secret.json',
            scopes=['https://www.googleapis.com/auth/drive.file'])
        flow = google_auth_oauthlib.flow.Flow(
            oauth2_session,
            client_type='web',
            client_config=client_config,
            redirect_uri='http://dhlab.pingry.org:8000/oauth_callback',
            code_verifier='128buoABUFU01189fhUA021uAFHJA102810hf3rfsdboq031rfd'
        )
        # flow.redirect_uri = 'http://localhost:5000/oauth_callback' # GET RID OF THIS LINE WHEN DEPLOYING
        authorization_response = request.url
        flow.fetch_token(authorization_response=authorization_response)
        credentials = flow.credentials
        session['credentials'] = credentials_to_dict(credentials)
        return redirect('/getUser')

    @app.route('/clear')
    def clear_credentials():
        if 'credentials' in session:
            del session['credentials']
        if 'email' in session:
            del session['email']
        return redirect('/')

    def credentials_to_dict(credentials):
        return {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }

    return app
