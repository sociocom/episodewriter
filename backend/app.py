from flask import Flask, send_file
from flask_cors import CORS
import sys

app = Flask(__name__)
CORS(app)

@app.route("/api/", methods=['GET'])
def test():
    return "Hello"

@app.route("/api/dummytest", methods=['GET'])
def dummytest():
    filename = 'shibainu.jpg'
    return send_file(filename, mimetype='image/jpg')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8888, debug=True)