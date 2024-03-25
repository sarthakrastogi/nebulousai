from litellm import completion

def llm_call(messages, model):
    response = completion(model="gpt-3.5-turbo", messages=messages)
    return response.choices[0].message.content