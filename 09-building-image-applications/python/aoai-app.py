from openai import AzureOpenAI
import os
import requests
from PIL import Image
import dotenv
import json

# import dotenv
dotenv.load_dotenv()

# Assign the API version (DALL-E is currently supported for the 2023-06-01-preview API version only)
client = AzureOpenAI(
  api_key=os.environ['AZURE_OPENAI_IMAGE_API_KEY'],  # this is also the default, it can be omitted
  api_version = "2023-12-01-preview",
  azure_endpoint=os.environ['AZURE_OPENAI_IMAGE_ENDPOINT'] 
  )

model = os.environ['AZURE_OPENAI_IMAGE_DEPLOYMENT']


try:
    # Create an image by using the image generation API

    number_of_images = 1
    result = client.images.generate(
        model=model,
        prompt='Bunny on horse, holding a lollipop, on a foggy meadow where it grows daffodils. It says "hello"',    # Enter your prompt text here
        size='1024x1024'
    )

    generation_response = json.loads(result.model_dump_json())
    # Set the directory for the stored image
    image_dir = os.path.join(os.curdir, 'images')

    # If the directory doesn't exist, create it
    if not os.path.isdir(image_dir):
        os.mkdir(image_dir)

    # Retrieve the generated image
    for index in range(number_of_images):
        image_url = generation_response["data"][index]["url"]  # extract image URL from response
        generated_image = requests.get(image_url).content  # download the image
        # Initialize the image path (note the filetype should be png)
        image_path = os.path.join(image_dir, f'generated-image_by_winny_{index}.png')
        with open(image_path, "wb") as image_file:
            image_file.write(generated_image)
        # Display the image in the default image viewer
        image = Image.open(image_path)
        image.show()

# catch exceptions
#except client.error.InvalidRequestError as err:
#    print(err)

finally:
    print("completed!")