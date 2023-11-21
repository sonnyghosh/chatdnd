import openai
import os
from dotenv import load_dotenv
load_dotenv()

token = os.environ.get("OPENAI_API_KEY")

def generateStoryResponse(prompt, context):
    messages = []
    messages.append({"role": "system", "content": "You are the dungeon master of the wonderful game of chatDND. You provide completions to the storyline with user options to pick what to do next. The storyline should be interesting and challenging."})
    messages.append({"role": "system", "content": context})
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
