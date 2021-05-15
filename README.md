# dhlab
This will hold the code for the Pingry's Digital Humanities suite and initial projects

To run on your local server:
  cd path/to/dhlab
  source environment/bin/activate
  export FLASK_APP=flaskr
  export FLASK_ENV=development
  flask run

To run on a remote server:
  gunicorn -w 4 -b 0.0.0.0:8000 "flaskr:create_app()" --daemon
  
 
