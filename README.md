# dhlab
This will hold the code for the Pingry Digital Humanities suite and initial projects

To run on your local server:

> cd path/to/dhlab

> python -m venv environment

> pip install -r requirements.txt (this step may take a few minutes)
  
> source environment/bin/activate (Windows: environment\Scripts\activate)
  
> export FLASK_APP=flaskr (Windows: set FLASK_APP=flaskr)
  
> export FLASK_ENV=development (Windows: set FLASK_ENV=development)
  
> flask run

> navigate to 127.0.0.1:5000 on your browser

To run on a remote server:

> gunicorn -w 4 -b 0.0.0.0:8000 "flaskr:create_app()" --daemon

> access at ip_address:8000
