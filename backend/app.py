from flask import Flask, send_file, request
from flask_cors import CORS
# from diffusion import image_generation
from celery_app import generate_image_task
import sys
import random

app = Flask(__name__)
CORS(app)

@app.route("/api/image_generation_task", methods=['GET'])
def generate_image_celery():
    prompt = request.args.get('prompt', "柴犬、カラフルアート")
    filename = str(random.getrandbits(32))
    print("calling the task")
    # Call the Celery task
    task = generate_image_task.apply_async(args=[prompt, filename])

    # Wait for the task to finish and get the result
    image_file = task.get()
    print("task finished")

    return send_file(image_file, mimetype='image/jpg')

@app.route("/api/", methods=['GET'])
def test():
    return "Hello"

@app.route("/api/dummytest", methods=['GET'])
def dummy_test():
    filename = 'shibainu.jpg'
    return send_file(filename, mimetype='image/jpg')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8888, debug=True)