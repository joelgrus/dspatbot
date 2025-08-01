#!/usr/bin/env python
import dspy
import uuid
from dotenv import load_dotenv

from dspatbot import Chatbot
from dspatbot.llm import configure_llm
from dspatbot.history.basic import BasicHistoryManager

def main():
    # Load environment variables from .env file
    load_dotenv()

    configure_llm()

    chatbot = Chatbot(history_manager=BasicHistoryManager(), personality="You are extremely angry.")

    print("Welcome to the Chatbot!")
    print("Ask questions or use tools. For example: 'What is 2+2?' or 'What is the date today?'")
    print("Type 'exit' to end the conversation.")

    session_id = str(uuid.uuid4())  # Generate a unique session ID for the conversation

    while True:
        query = input("You: ")
        if query.lower() == "exit":
            break

        # The chatbot is stateful, so we only need to pass the query
        response = chatbot(query=query, session_id=session_id)

        print(f"Bot: {response.answer}")

if __name__ == "__main__":
    main()