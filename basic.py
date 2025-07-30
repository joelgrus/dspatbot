"""
The most basic chatbot implementation using DSPy.
"""

import dspy

dspy.configure(lm=dspy.LM('openrouter/google/gemini-2.5-flash-lite'))

chatbot = dspy.Predict('query,history,personality -> answer')

history = []
personality = "You are extremely angry."

while True:
    query = input("You: ")

    # Call the chatbot with the current query and history
    response = chatbot(query=query, history=history, personality=personality)

    # Print the bot's response
    print(f"Bot: {response.answer}")

    # Update history
    history.append({'role': 'user', 'content': query})
    history.append({'role': 'assistant', 'content': response.answer})