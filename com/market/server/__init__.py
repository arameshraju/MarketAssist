import flask
from flask import Flask, request, Response

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Create some test data for our catalog in the form of a list of dictionaries.



@app.route('/', methods=['GET'])
def home():
    return '''<h1>Thank you for using api</h1>
<p> ramesh</p>'''


@app.route('/webhook', methods=['POST'])
def respond():
    print(request);
    print();
    return Response(status=200)

app.run()