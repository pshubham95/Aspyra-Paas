__author__ = 'Shubham'
from PIL import Image
import os
basedir = os.path.abspath(os.path.dirname(__file__))

def save_image(image_path,id,updir):
    image = Image.open(image_path)
    image = image.resize((48,48), Image.ANTIALIAS)
    quality_val = 90
    image.save(os.path.join(updir, id + '_48.png'), 'PNG', quality=quality_val)



