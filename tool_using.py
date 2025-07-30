"""
A simple chatbot using dspy with tools for weather and math operations.
"""

import dspy

dspy.configure(lm=dspy.LM('openrouter/google/gemini-2.5-flash-lite'))


def get_weather(location: str) -> str:
    # Placeholder for actual weather fetching logic
    return f"The weather in {location} is sunny with a high of 25°C."

def do_math(expression: str) -> str:
    try:
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception as e:
        return f"Error: {e}"

tools = [dspy.Tool(get_weather), dspy.Tool(do_math)]
chatbot = dspy.ReAct('query,history,personality -> answer', tools=tools)

history = []
personality = "You are extremely angry."

while True:
    query = input("You: ")
    if query.lower() == "exit":
        break

    # Update history with the new query
    history.append({'role': 'user', 'content': query})

    # Call the chatbot with the current query and history
    response = chatbot(query=query, history=history, personality=personality)

    # Print the bot's response
    print(f"Bot: {response.answer}")

    # Update history with the bot's response
    history.append({'role': 'assistant', 'content': response.answer})