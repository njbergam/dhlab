# dhlab
This will hold the code for the Pingry's Digital Humanities suite and initial projects

In order to use locally:
1) Download the repository
      via terminal, git clone https://github.com/YOURUSERNAME/dhlab/
2) Use a Python3 virtual environment
      Activate: source ENVNAME/bin/activate
3) Downlaod the necessary dependencies
      pip install flask
      pip install requests
      pip install google_auth
      pip install google
      pip install wikipedia
      pip install --upgrade google-cloud-storage
      pip install google_auth_oauthlib      
      pip install googleapiclient
      pip install --upgrade google-api-python-client
      pip install nltk
      pip install matplotlib
      pip install mpld3
      pip install PyPDF2
      pip install scipy
4) Run Flask
      export FLASK_APP=webtest.py
      export FLASK_ENV=development
      flask run
