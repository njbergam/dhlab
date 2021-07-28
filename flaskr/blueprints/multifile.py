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

multifile = Blueprint("multifile", __name__, template_folder="templates")


# Landing page for multi text comparison
@multifile.route('/analytics')
def multi():
    if 'failedMulti' not in session:
        fail = 0
    else:
        fail = session['failedMulti']

    session['priorUrl'] = '/analytics'

    if 'files' not in session:
        print("empty files")
        files = []
        session['files'] = []
    else:
        print(session["files"])
        files = session['files']

    return render_template('multi-comp.html', files=files, fail=fail)


@multifile.route("/upload_multifile", methods=["POST"])
def upload_multifile():
    if request.method == "POST":
        if "file[]" not in request.files:
            session["failedMulti"] = 3
            return redirect(session["priorUrl"])

        uploadedFiles = request.files.getlist("file[]")
        print(uploadedFiles)

        files = []

        for file in uploadedFiles:
            if file and file.filename != "" and allowed_file(file.filename):
                files.append(secure_filename(file.filename))

                print("Now saving file" + file.filename)

                file.save(
                    os.path.join(UPLOAD_FOLDER,
                                 secure_filename(file.filename)))

        session["files"] = files
        return redirect(session["priorUrl"])

    session['failedMulti'] = 1
    return redirect(session['priorUrl'])


@multifile.route('/removefile/<filename>', methods=['GET'])
def removefile(filename):
    # Get the parameter
    print("Received delete request: " + filename)

    print(session["files"])

    session["files"].remove(filename)
    session.modified = True

    print(session["files"])

    return redirect('/analytics')


@multifile.route('/reportMulti', methods=['GET', 'POST'])
def multiReport():
    print("in multiReport() in multifile.py")

    # Make sure that there are files that the user uploaded
    if len(session['files']) == 0:
        session['failedMulti'] = 2
        return redirect('/analytics')

    # Get the user request options
    dict = request.form.to_dict()
    text = []
    text2 = []
    textRsts = []

    # Loop through each of the files and extract it into an array containing the text
    for i in range(len(session['files'])):
        print("Currently processing file: " + session['files'][i])

        if session['files'][i][-4:] == '.pdf':
            text.append(text_extractor('flaskr/uploads/' +
                                       session['files'][i]))
            text2.append(cleanText2('flaskr/uploads/' + session['files'][i]))
        else:
            text.append(simpleTokenize('flaskr/uploads/' +
                                       session['files'][i]))
            text2.append(cleanText('flaskr/uploads/' + session['files'][i]))
        textRsts.append(txtResult(session['files'][i], -1, -1, "1", "1", "1"))

    # Average sentence length throughout the app
    if "SLength" in dict:
        print("creating sentence length chart")

        for i in range(len(session['files'])):
            textRsts[i].sen_avg, textRsts[i].sen_stdv = senlenStats(text[i])
    if "tfidf" in dict:
        print("creating tf-idf")

        corpus = [] #generating the corpus from our stock

        path = 'flaskr/blueprints/corpus'
        for filename in os.listdir(path):
            corpus.append(simpleTokenize('flaskr/blueprints/corpus/' + filename))
            print(filename)
        wordsToBeTfIDFed = dict["TfIdfWords"].split(",")
        print(wordsToBeTfIDFed)
        wordsNoSpaces = []
        for currWord in wordsToBeTfIDFed:
            print(currWord[0:1])
            while currWord[0:1] == " ":
                currWord = currWord[1:]
            wordsNoSpaces.append(currWord)
        print(wordsToBeTfIDFed)
        print(wordsNoSpaces)
        tfIdfResults = {}
        for i in range(len(session['files'])):
            currFile = session['files'][i]
            print("FINDING TF-IDF FOR: " + currFile)
            currScores = []
            for word in wordsNoSpaces:
                result = tfidf(word, simpleTokenize('flaskr/uploads/' + currFile), corpus)
                currScores.append(result)
                print("tf-idf score for " + word + ": " + str(result))
            textRsts[i].tfidf = currScores
            textRsts[i].tfidf_words = wordsToBeTfIDFed

        # textRsts[i].tfIdf = tfIdfResults #same index for valeus as words to be IDFed
    # Part of speech data
    if "POS" in dict:
        print("creating pos chart in multi")
        for i in range(len(session['files'])):
            textRsts[i].pos = ''.join(
                random.choices(string.ascii_uppercase + string.digits,
                               k=10))  #title of the generated chart
            savePOSPiChart(text2[i], textRsts[i].pos)
    if "TopWords" in dict:
        print("creating top words chart")
        for i in range(len(session['files'])):
            textRsts[i].top = ''.join(
                random.choices(string.ascii_uppercase + string.digits, k=10))
            saveTopWords(text2[i], textRsts[i].top)
    overlapCharts = []
    overlapInfo = []
    if "over" in dict:
        print("creating overlap chart")
        k = int(len(session['files']) * (len(session['files']) - 1) / 2 + 0.5)
        for i in range(k):
            overlapCharts.append(''.join(
                random.choices(string.ascii_uppercase + string.digits, k=10)))
        overlap(text2, overlapCharts)
        l = 0
        for i in range(len(session['files'])):
            for j in range(i + 1, len(session['files'])):
                temp = []
                temp.append(
                    str(session['files'][i]) + " and " +
                    str(session['files'][j]))
                temp.append(overlapCharts[l])
                l += 1
                overlapInfo.append(temp)
    else:
        overlapCharts.append("1")
    # if "WordProg" in dict:
    #     print("creating word progression chart")
    #     for i in range(len(session['files'])):
    #         textRsts[i].wp = ''.join(
    #             random.choices(string.ascii_uppercase + string.digits, k=10))
    #         arr = dict["WordProgWords"].replace(" ", "").split(';')
    #         groups = []
    #         for j in range(len(arr)):
    #             groups.append(arr[j].split(','))
    #         oneTextPlotChronoMap(text2[i], groups, textRsts[i].wp)
    # for i in range(len(textRsts)):
    #     print(textRsts[i].pq)
    #     print("a")

    selectionsList = list(dict.keys())

    return render_template('multiResults.html',
                           results=textRsts,
                           overlap=overlapInfo,
                           selections=selectionsList)
