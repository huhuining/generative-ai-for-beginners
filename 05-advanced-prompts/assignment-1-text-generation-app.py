from openai import OpenAI
from dotenv import load_dotenv
import os 

load_dotenv()
OpenAI.api_key = os.environ["OPENAI_API_KEY"]

my_model = "gpt-4o-mini"

client = OpenAI()

no_recipes = input("No of recipes (for example, 5): ")

ingredients = input("List of ingredients (for example, chicken, potatoes, and carrots): ")

my_input = f"Show me {no_recipes} recipes for a dish with the following ingredients: {ingredients}. Per recipe, list all the ingredients used"

print(my_input)

completion = client.responses.create(
    model=my_model,
    input=my_input
)


print(completion.output_text)

my_input_result = completion.output_text

additional_input = "Produce a shopping list for the generated recipes and please don't include ingredients that I already have."

new_input = f"{my_input_result} {additional_input}"

new_result = client.responses.create(
    model=my_model,
    input=new_input,
    max_output_tokens=1200
)

print(new_result.output_text)

