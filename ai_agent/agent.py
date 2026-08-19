from openai import OpenAI
from tools import run_command, read_file
from config import OPENAI_API_KEY


client = OpenAI(
    api_key=OPENAI_API_KEY
)


history = []


while True:

    prompt = input("\nPVIMP > ")

    if prompt == "exit":
        break


    history.append({
        "role":"user",
        "content":prompt
    })


    response = client.chat.completions.create(
        model="gpt-5",
        messages=history
    )


    answer = response.choices[0].message.content


    print("\nGPT:")
    print(answer)


    history.append({
        "role":"assistant",
        "content":answer
    })