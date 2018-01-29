This is the backend of a simple web-app, developed on Python Flask, as a part of Hasura Internship.
The file hello_world.py handles various HTTP requests (listed below).
It has been developed on a virtual environment on Python3.


1. We begin with by creating a virtual environment.
This can be done from command line as: ```virtualenv venv``` (venv - name of environment)
(Since I am using Anaconda on Linux, I install virtualenv as ```conda install virtualenv```. There are other ways for other platforms/distributions)

2. We then activate our environment: ```./venv/bin/activate```
NOTE: After finishing off our work, we can deactivate the environment: deactivate

3. We tell the terminal the application to be loaded, by setting the FLASK_APP environment variable: 
```export FLASK_APP=hello_world.py```

4. Now we can run our application on localhost. This can be done in 2 ways:
4.1) Using the flask command: ```flask run```
4.2) Using python command with -m switch with flask: ```python -m flask run ```
The application, by default runs on localhost:5000/

5. Our application handles following requests at the moment:
5.1) http://localhost:5000/ - Displays displays a simple string - "Hello World - Shahbaz"
5.2) http://localhost:5000/authors - fetches a list of authors and list of posts from jsonplaceholder.typicode.com, and 
	 displays author names and the number of posts written by them
	 (the data is fetched using requests module)
5.3) http://localhost:8080/setcookie - Sets cookies with variables 'name' and 'age'
5.4) http://localhost:8080/getcookies - Displays the stored cookie key-values
5.5) http://localhost:8080/robots.txt - Request to robots.txt file is denied with an appropriate denial response message
5.6) http://localhost:8080/image - Returns an image file stored in static* directory
5.7) http://localhost:8080/html - Renders an html page (home.html) stored in templates* directory
5.8) http://localhost:8080/input - Renders a form (form.html), which takes text input and sends it on server using POST method
5.9) http://localhost:8080/send-name - This request is made in response to submitting the form data(in form.html). It captures the form inputs and displays them in browser

* In addition to out application file, There are 2 additional directories:
a) static - to store all the static files we want to send as a response to various requests
b) templates - stores html templates to be rendered in response to certain requests

NOTE: Our application might often run into exceptions, so it is necessary to know the source of error.
For this we can run the application in DEBUG mode by setting the FLASK_DEBUG environment variable : ```export FLASK_DEBUG=1```
