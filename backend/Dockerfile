# Use the official Python 3.10 image as the base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the working directory
COPY diffusion.py /app
COPY app.py /app
COPY celery_app.py /app
# COPY pipeline_stable_diffusion_xl.py /opt/conda/envs/diffusion-xl/lib/python3.10/site-packages/diffusers/pipelines/stable_diffusion_xl/
COPY pipeline_stable_diffusion_xl.py /usr/local/lib/python3.10/site-packages/diffusers/pipelines/stable_diffusion_xl/pipeline_stable_diffusion_xl.py

ENV PYTHONUNBUFFERED 1
EXPOSE 80

# Set the command to run the application
CMD [ "python", "-u","app.py" ]