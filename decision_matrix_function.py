from openai import OpenAI
import json

client = OpenAI()

def decision_matrix(messages):

    tools = [
        {
            "type": "function",
            "function": {
                "name": "decision_matrix",
                "description": "what does the user want to do? Do they want to create a new event or return events that have already been scheduled?",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": 
                            '''
                            If they want to create a new event.
                            If they want to return existing events.
                            e.g. create_event, return_event
                            '''
                        },
                    },
                    "required": ["path"],
                },
            },
        }
    ]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=messages,
        tools=tools,
        tool_choice="auto",  # auto is default, but we'll be explicit
    )
    # this is the big response with all of the stuff inside
    response_message = response.choices[0].message

    # returns the raw response for the first ai stuff
    tool_calls = response_message.tool_calls 
    function_arguments_json = tool_calls[0].function.arguments  
    arguments_dict = json.loads(function_arguments_json)
    path_value = arguments_dict["path"]

    # print("The path is:", path_value)
    print("decision matrix is all done now")
    return path_value
