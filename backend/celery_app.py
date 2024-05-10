from celery import Celery, uuid
from diffusion import image_generation, load_pipeline

celery = Celery('tasks', broker='redis://redis:6379', backend='redis://redis:6379')

pipeline = None

@celery.task(bind=True)
def generate_image_task(self, prompt, filename):
    global pipeline
    # Generate image
    if pipeline is None:
        pipeline = load_pipeline()

    task_id = self.request.id

    image = image_generation(task_id, pipeline,prompt)
    image_file = 'data/' + filename + '.jpg'

    # Save image
    image.save(image_file)

    # Save prompt
    with open('data/' + filename + '.txt', 'w') as f:
        f.write(prompt)
    
    print("---->",self.request.id)

    self.update_state(state='SUCCESS', meta={'image_file': image_file})
    return image_file