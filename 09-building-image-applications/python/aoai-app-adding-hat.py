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

# generate mask dimension top left (306,87), top right (649,87), bottom left (306,477) bottom right (649,477)
# img = Image.open("images/generated-image_by_winny.png")
# mask = Image.new("RGBA", img.size, (0, 0, 0, 255))   # opaque

# draw = ImageDraw.Draw(mask)
# draw.rectangle([(306, 87), (649, 477)], fill=(255, 255, 255, 0))  # transparent hole

# mask.save("mask_generated.png")

try:
    # Update existing image to add a hat on the rabbit
    with open('images/generated-image_by_winny.png', 'rb') as image_file, \
         open('images/mask_generated.png', 'rb') as mask_file:
        result = client.images.edit(
            image=image_file,
            mask=mask_file,
            model=model,
            prompt='An image of a rabbit with hat on his head.',    # Enter your prompt text here
            size='1024x1024',
            n=1
        )
    
        # Set the directory for the stored image
        image_dir = os.path.join(os.curdir, 'images')
    
        # If the directory doesn't exist, create it
        if not os.path.isdir(image_dir):
            os.mkdir(image_dir)
    
        # Initialize the image path (note the filetype should be png)
        image_path = os.path.join(image_dir, 'generated-image-with-hat_by_winny.png')
    
        # Retrieve the generated image
        b64_image = result.data[0].b64_json
        generated_image = base64.b64decode(b64_image)
        
        with open(image_path, "wb") as image_file:
            image_file.write(generated_image)
    
        # Display the image in the default image viewer
        image = Image.open(image_path)
        image.show()

# catch exceptions
# except client.error.InvalidRequestError as err:
#    print(err)
    
finally:
    print("completed!")