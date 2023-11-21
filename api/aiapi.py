import openai
import os
from dotenv import load_dotenv
load_dotenv()

token = os.environ.get("api-key")

def generateStoryResponse(prompt):
    messages = []
    messages.append({"role": "system", "content": "You are a helpful assistant."})

    question = {}
    question['role'] = 'user'
    question['content'] = prompt
    messages.append(question)
    
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=messages)

    try:
        answer = response['choices'][0]['message']['content'].replace('\n','<br>') # return as html
    except:
        answer = 'cannot get response from API'

    return answer
