from flask import Flask, send_file, request
from flask_cors import CORS
from diffusion import image_generation
import sys
import random



app = Flask(__name__)
CORS(app)

@app.route("/api/", methods=['GET'])
def test():
    return "Hello"

@app.route("/api/dummytest", methods=['GET'])
def dummy_test():
    filename = 'shibainu.jpg'
    return send_file(filename, mimetype='image/jpg')

@app.route("/api/image_generation", methods=['GET'])
def generate_image():
    prompt = request.args.get('prompt', "柴犬、カラフルアート")

    filename = str(random.getrandbits(32))

    # Generate image
    image = image_generation(prompt)
    image_file = 'data/' + filename + '.jpg'

    # Save image
    image.save(image_file)

    # Save prompt
    with open('data/' + filename + '.txt', 'w') as f:
        f.write(prompt)
    
    return send_file(image_file, mimetype='image/jpg')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8888, debug=True)