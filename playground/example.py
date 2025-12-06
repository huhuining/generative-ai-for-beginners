from openai import OpenAI
client = OpenAI()

response = client.responses.create(
    model="gpt-5-mini",
    input="Write a one-sentence bedtime story about a hero."
)

print(response.output_text)
