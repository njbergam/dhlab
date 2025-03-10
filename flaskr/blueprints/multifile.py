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
import matplotlib.pyplot as plt
import random
import string
import json
import nltk
import os
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
        files = []
        session['files'] = []
    else:
        files = session['files']

    deleteGraphFolder()

    return render_template('multi-comp.html', files=files, fail=fail)

# Helper method to delete all files in the graph folder.

def deleteGraphFolder():
    currDir = os.path.dirname(os.path.abspath(__file__))
    relativePath = os.path.join(currDir, "..", "static", "graphs")
    
    # Ensure the directory exists
    if not os.path.exists(relativePath):
        os.makedirs(relativePath)

    # Delete files inside the folder
    for file in os.listdir(relativePath):
        filePath = os.path.join(relativePath, file)
        if os.path.isfile(filePath):  # Ensure it's a file before deleting
            print(f"[Clearing Graphs] Deleting {file}.")
            os.remove(filePath)

@multifile.route("/upload_multifile", methods=["POST"])
def upload_multifile():
    if request.method == "POST":
        if "file[]" not in request.files:
            session["failedMulti"] = 3
            return redirect(session["priorUrl"])

        uploadedFiles = request.files.getlist("file[]")

        files = []

        for file in uploadedFiles:
            if file and file.filename != "" and allowed_file(file.filename):
                files.append(secure_filename(file.filename))

                print("[Upload] Now saving file: " + file.filename)

                file.save(
                    os.path.join(UPLOAD_FOLDER,
                                 secure_filename(file.filename)))

        # if "files" in session:
        #     for file in files:
        #         if file not in session["files"]:
        #             session["files"].append(file)
        # else:
        #     session["files"] = files
        print("Before adding new files: ", session["files"])

        # add new files while keeping the old ones there
        if "files" not in session:
            session["files"] = []
        arr = session["files"]
        for file in files:
            if file not in arr:
                arr.append(file)
        session["files"] = arr
        print("After adding new files: ", session["files"])
        return redirect(session["priorUrl"])

    session['failedMulti'] = 1
    return redirect(session['priorUrl'])


@multifile.route('/removefile/<filename>', methods=['GET'])
def removefile(filename):
    # Get the parameter
    print("[Delete] Received delete request: " + filename)
    session["files"].remove(filename)
    session.modified = True
    return redirect('/analytics')


@multifile.route('/reportMulti', methods=['GET', 'POST'])
def multiReport():
    print("[ReportMulti] Computing results...")

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
        print("[ReportMulti] Currently processing file: " + session['files'][i])

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
        print("[Results] Computing sentence length stats.")

        for i in range(len(session['files'])):
            textRsts[i].sen_avg, textRsts[i].sen_stdv = senlenStats(text[i])
    if "tfidf" in dict:
        print("[Results] Computing TF-IDF scores.")

        wordsToBeTfIDFed = dict["TfIdfWords"].split(",")
        wordsNoSpaces = []

        for currWord in wordsToBeTfIDFed:
            wordsNoSpaces.append(currWord.replace(" ", ""))

        print("words:", wordsNoSpaces)

        matrix = tfidf_matrix(wordsNoSpaces, text2, session['files'])

        """tfIdfResults = {}
        for word in wordsNoSpaces:
            currScores = []
            for i in range(len(session['files'])):
                result = tfidf(word, simpleTokenize('flaskr/uploads/' + session['files'][i]), corpus)
                currScores.append(result)
                print("tf-idf score for " + word + ": " + str(result))
            tfIdfResults[word] = currScores
        print(session['files']) """

        #textRsts[i].tfidf = matrix #currScores
        #textRsts[i].books = session['files']
        print("results", textRsts)
        textRsts[0].tfidf = ''.join(
            random.choices(string.ascii_uppercase + string.digits, k=10))
        print(textRsts[0].tfidf)
        createTfidfGraph(matrix, textRsts[0].tfidf)

        # textRsts[i].tfIdf = tfIdfResults #same index for valeus as words to be IDFed

    if "Sentiment" in dict:
        # structure: create randomized graph names for each file, then create a graph for each file and pass 
        # the text and graph name to the renderer
        print("[Results] Computing sentiment analysis.")
        for index, elem in enumerate(session["files"]):
            textRsts[index].polarity_sentiment_graph = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            textRsts[index].polarity_sentiment_score = sentiment_analysis_score(elem, textRsts[index].polarity_sentiment_graph)

    # Part of speech data
    if "POS" in dict:
        print("[Results] Computing POS distribution.")
        for i in range(len(session['files'])):
            textRsts[i].pos = ''.join(
                random.choices(string.ascii_uppercase + string.digits,
                               k=10))  #title of the generated chart
            savePOSPiChart(text2[i], textRsts[i].pos)

        print("POS TITLE: " + textRsts[i].pos)
    if "TopWords" in dict:
        print("[Results] Creating top words chart.")
        for i in range(len(session['files'])):
            textRsts[i].top = ''.join(
                random.choices(string.ascii_uppercase + string.digits, k=10))
            saveTopWords(text2[i], textRsts[i].top)

    overlapCharts = [] # contains the names of the overlap data charts
    overlapInfo = []
    if "over" in dict:
        # structure: create randomized graph names, create graphs and save them at locations in static, then 
        # create a list of the graph names and the graph objects, which is passed to the renderer
        print("[Results] Creating overlap chart.")
        k = int(len(session['files']) * (len(session['files']) - 1) / 2 + 0.5)
        for i in range(k):
            overlapCharts.append(''.join(
                random.choices(string.ascii_uppercase + string.digits, k=10)))
        
        l = 0
        for i in range(len(session['files'])):
            for j in range(i + 1, len(session['files'])):
                # for every pair of files, create a new overlapInfo object and add it to the list
                overlap(session['files'][i], session['files'][j], overlapCharts[l]) # calculate overlap and save charts
                temp = []
                temp.append(
                    str(session['files'][i]) + " and " +
                    str(session['files'][j]))
                temp.append(overlapCharts[l])
                l += 1
                overlapInfo.append(temp)
    else:
        overlapCharts.append("1")
    if "WordProg" in dict:
        # structure: create randomized graph names, create graphs and save them at locations in static, then
        # pass the graph names and graph objects to the renderer
        print("[Results] Creating word progression chart.")
        for i in range(len(session['files'])):
            cleanedInput = []

            textRsts[i].wp = ''.join(
                random.choices(string.ascii_uppercase + string.digits, k=10))
            arr = dict["WordProgWords"].replace(" ", "").split(';')
            groups = []
            for j in range(len(arr)):
                groups.append(arr[j].split(','))
            for subarray in groups:
                cleanedInput.append(cleanText2(subarray))

            oneTextPlotChronoMap(text2[i], cleanedInput, textRsts[i].wp)
    if "topicmodeling" in dict:
        print("[Results] Computing topic modeling.")
        textRsts[0].topicmodeling = ''.join(
            random.choices(string.ascii_uppercase + string.digits, k=10))
        modelTopics(session['files'], textRsts[0].topicmodeling)

    # if "tvect" in dict:
        

    selectionsList = list(dict.keys())

    # at this point, all graphs and statistics have been created, so we can give the text names and graph locations
    # to the renderer which will display them on the page

    print("[Debug] Sentiment Graphs Passed to Template:")
    for result in textRsts:
        print(f"Graph: {result.polarity_sentiment_graph}")


    return render_template('multiResults.html',
                           results=textRsts,
                           overlap=overlapInfo,
                           selections=selectionsList)
