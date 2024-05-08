from diffusers import DiffusionPipeline
import torch

from huggingface_hub._login import _login
import os
token = os.environ.get('HUGGINGFACE_TOKEN')

_login(token=token, add_to_git_credential=False) 

pipeline = DiffusionPipeline.from_pretrained(
    "stabilityai/japanese-stable-diffusion-xl", trust_remote_code=True
)

pipeline.to("cuda")

def image_generation(prompt="柴犬、カラフルアート"):
    image = pipeline(prompt=prompt).images[0]
    image.save("output.jpg")
    return image