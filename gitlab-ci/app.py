from flask import Flask
app = Flask(__name__)

@app.route('/')
def helloworld():
    return 'Hello World!'
