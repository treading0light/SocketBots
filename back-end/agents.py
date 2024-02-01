from openai import OpenAI

from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

def agent_frank(in_queue, out_queue):
    while True:
        messages = in_queue.get()

        print("here's frank")
        completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
        )
        res = completion.choices[0].message
        res_dict = {
            "content": res.content,
            "role": res.role
        }
        print(res)
        out_queue.put(res_dict)
    