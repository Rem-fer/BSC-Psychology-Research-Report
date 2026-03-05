from litellm import completion
from dotenv import load_dotenv
import os
import pandas as pd
import anthropic
import json

load_dotenv()

def get_summary():
    return study_summary

def get_conclusions():
    return conclusions

def get_results():
    return results

def handle_tool_calls(message):
    """
    Handle all tool calls from the assistant message.
    Loops through each tool call, executes the corresponding function,
    and returns a list of tool result messages ready to append to the conversation.
    """
    responses = []
    for tool_call in message.tool_calls:
        tool_name = tool_call.function.name
        
        if tool_name == "get_summary":
            tool_result =  get_summary()
        elif tool_name == "get_results":
            tool_result =  get_results()
        elif tool_name == "get_conclusions":
            tool_result =  get_conclusions()
        
        responses.append( {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(tool_result)
                }
        )
        return responses


study_summary  = open("content_for_llm/study_summary.txt").read()
conclusions = open("content_for_llm/conclusion.txt").read()
results = json.load(open("content_for_llm/results.json"))


MODEL = "claude-sonnet-4-20250514"
KEY = os.getenv("ANTHROPIC_API_KEY")


# Defining tools
get_summary_tool = {
    "name": "get_summary",
    "description": "Get study background, methodology, participants, measures and hypotheses",
    "parameters": {
        "type": "object",
        "properties": {}
    }
}

get_results_tool = {
    "name": "get_results", 
    "description": "Get regression results, descriptive statistics and normality tests",
    "parameters": {
        "type": "object",
        "properties": {}
    }
}

get_conclusions_tool = {
    "name": "get_conclusions",
    "description": "Get hypothesis outcomes, interpretation, limitations and future directions",
    "parameters": {
        "type": "object",
        "properties": {}
    }
}

tools = [
    {"type": "function", "function": get_summary_tool},
    {"type": "function", "function": get_results_tool},
    {"type": "function", "function": get_conclusions_tool}
]

### Keep this to calculate costs
# response.model,
# response.usage.prompt_tokens,
# response.usage.completion_tokens,
# response.usage.total_tokens,
# response._hidden_params["response_cost"]

system_prompt = """
You are a research assistant for a BSc Psychology study on trait mindfulness, inhibitory control, and phone checking frequency. Answer questions clearly and accurately using your tools when needed.

Use get_summary for questions about methodology, design, participants or measures.
Use get_results for questions about statistics, regression outputs or descriptive data.
Use get_conclusions for questions about hypothesis outcomes, limitations or future directions.
"""


messages = [ {"role": "system", "content": system_prompt}]

# LLM response
def chat_with_model(messages):
    response = completion(model= MODEL, messages=messages, tools=tools, api_key= KEY)
    if response.choices[0].finish_reason == "tool_calls":
        # Message containes tool request object.
        ## It is added under "assisatnt" role to message using dump because it is a Pydantic object
        message = response.choices[0].message 
        messages.append(message.model_dump()) 
        
        tool_results = handle_tool_calls(message)
        messages.extend(tool_results) # Use extend if returning a list of tool results
        final_response = completion(model= MODEL, messages=messages, tools=tools, api_key= KEY)

        return final_response.choices[0].message.content
    


def chat_with_model_stream(messages):
    response = completion(model= MODEL, messages=messages, tools=tools, api_key= KEY)
    if response.choices[0].finish_reason == "tool_calls":

        message = response.choices[0].message 
        messages.append(message.model_dump()) 
        tool_results = handle_tool_calls(message)
        messages.extend(tool_results) # Use extend if returning a list of tool results

    final_response = completion(model= MODEL, messages=messages, tools=tools, api_key= KEY, stream=True)

    for chunk in final_response:
        content = chunk.choices[0].delta.content
        if content is not None:
            yield content
    