from openai import OpenAI
import os
import requests
from PIL import Image, ImageDraw
import dotenv
import json
import base64

# import dotenv
dotenv.load_dotenv()

# Assign the API version (DALL-E is currently supported for the 2023-06-01-preview API version only)
client = OpenAI(
  api_key=os.environ['OPENAI_API_KEY'],  # this is also the default, it can be omitted
)

model = "gpt-image-1"

try:
    # Create an image by using the image generation API
    number_of_image=2
    generation_response = client.images.generate(
        model=model,
        prompt='Bunny on horse, holding a lollipop, on a foggy meadow where it grows daffodils',    # Enter your prompt text here
        size='1024x1024',
        n=number_of_image
    )
    # Set the directory for the stored image
    image_dir = os.path.join(os.curdir, 'images')

    # If the directory doesn't exist, create it
    if not os.path.isdir(image_dir):
        os.mkdir(image_dir)

    for index in range(number_of_image):
        # Retrieve the generated image
        b64_image = generation_response.data[index].b64_json
        generated_image = base64.b64decode(b64_image)
        # Initialize the image path (note the filetype should be png)
        image_path = os.path.join(image_dir, f'generated-image-by-openai_{index}.png')
        with open(image_path, "wb") as image_file:
            image_file.write(generated_image)
    
        # Display the image in the default image viewer
        image = Image.open(image_path)
        image.show()

# catch exceptions
except Exception as err:
    print(err)

# ---creating variation below---
# response = client.images.create_variation(
#   image=open(image_path, "rb"),
#   n=1,
#   size="1024x1024"
# )