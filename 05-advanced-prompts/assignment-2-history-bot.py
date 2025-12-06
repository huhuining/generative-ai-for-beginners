from openai import OpenAI
from dotenv import load_dotenv
import os 

load_dotenv()
OpenAI.api_key = os.environ["OPENAI_API_KEY"]

my_model = "gpt-4o-mini"

client = OpenAI()

name = input("History figure name (for example, Alan Turing): ")
question = input("question to ask (for example, what is your greatest achievement): ")
my_temp = float(input("temporature: "))

print(question)

completion = client.responses.create(
    model=my_model,
    input=[
        {"role": "system", "content": f"You need to play the role of a history figure {name}. You should answer question like him/her."},
        {"role": "user", "content": f"{question}"}
    ],
    max_output_tokens=1200,
    temperature=my_temp
)


print(completion.output_text)
