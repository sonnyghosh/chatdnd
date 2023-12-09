from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

token = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=token)

sys_pt = '''
You are the dungeon master of the wonderful game of chatDND. 
You provide completions to the storyline with user options to pick what to do next. 
Format of response:
Story{
    continuation of story
}
Variables{
    variable:value change
}
'''

def generateStoryResponse(prompt, context='', max_len=250):
    messages = []
    messages.append({"role": "system", "content": sys_pt})
    messages.append({"role": "system", "content": context})
    question = {}
    question['role'] = 'user'
    question['content'] = prompt
    messages.append(question)
    
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages, max_tokens=max_len)
    try:
        answer = response.choices[0].message.content.replace('\n','<br>') # return as html
    except Exception as e:
        print(e)
        answer = 'cannot get response from API'

    # TODO: parse out the message to find the options and the story

    return answer


'''
Example of a chat completion object
ChatCompletion(
    id='chatcmpl-8Np6lx28vkijp95wIkelV54neBrlg', 
    choices=[
        Choice(
            finish_reason='length', 
            index=0, 
            message=ChatCompletionMessage(
                content='You decide to continue exploring the cavern, leaving the rare gem behind for now. As you venture deeper into the darkness, you notice a faint glow up ahead. Curiosity gets the better of you, and you cautiously move towards the source of the light.\n\nAs you draw closer, you discover a chamber filled with glowing mushrooms. The soft bioluminescent light they emit illuminates the area, revealing a hidden pathway leading deeper into the depths of the cavern. However, you also spot a cluster of', 
                role='assistant', 
                function_call=None, 
                tool_calls=None
            )
        )
    ],
    created=1700688695, 
    model='gpt-3.5-turbo-0613', 
    object='chat.completion', 
    system_fingerprint=None, 
    usage=CompletionUsage(
        completion_tokens=100, 
        prompt_tokens=87, 
        total_tokens=187
    )
)

'''