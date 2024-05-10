from flask import Flask, send_file, request, Response
from flask_cors import CORS
# from diffusion import image_generation
from celery_app import generate_image_task, celery
from celery.result import AsyncResult
import sys
import random
import json
import redis

app = Flask(__name__)
CORS(app)

r = redis.Redis(host='redis', port=6379, db=0)


# @app.route("/api/image_generation_task", methods=['GET'])
# def generate_image_celery():
#     prompt = request.args.get('prompt', "柴犬、カラフルアート")
#     filename = str(random.getrandbits(32))
#     print("calling the task")
#     # Call the Celery task
#     task = generate_image_task.apply_async(args=[prompt, filename])

#     # Wait for the task to finish and get the result
#     image_file = task.get()
#     print("task finished")

#     return send_file(image_file, mimetype='image/jpg')

@app.route("/api/image_generation_task", methods=['GET'])
def generate_image_celery():
    prompt = request.args.get('prompt', "柴犬、カラフルアート")
    filename = str(random.getrandbits(32))
    print("calling the task")
    # Call the Celery task
    task = generate_image_task.apply_async(args=[prompt, filename])

    # Return the task_id
    response = Response(json.dumps({'task_id': str(task.id)}), status=200, mimetype='application/json')
    return response

@app.route('/api/task_status/<task_id>')
def task_status(task_id):
    task = AsyncResult(task_id, app=celery)

    progress_str = r.get(f'task_progress_{task_id}')
    if progress_str is None:
        response = Response(json.dumps({'error': 'Task not found'}), status=404, mimetype='application/json')
        return response

    progress = json.loads(progress_str)
    progress['state'] = task.state
    response = Response(json.dumps(progress), status=200, mimetype='application/json')
    return response

@app.route('/api/get_image/<task_id>')
def get_image(task_id):
    task = generate_image_task.AsyncResult(task_id)
    print(task.state)
    if task.state == 'PENDING':
        response = Response(json.dumps({'error': 'Task not finished'}), status=202, mimetype='application/json')
        return response
    elif task.state != 'SUCCESS':
        response = Response(json.dumps({'error': 'Task failed'}), status=500, mimetype='application/json')
        return response
    else:
        print(task.result)
        image_file = task.result.get('image_file')
        import os
        print(image_file, os.path.exists(image_file))
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