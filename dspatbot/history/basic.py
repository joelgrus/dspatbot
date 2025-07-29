"""
basic dict-based history management for a chatbot
"""
from collections import defaultdict

from . import History, Turn, HistoryManager

class BasicHistoryManager(HistoryManager):
    """
    A history manager that uses a dict to store conversation history.
    This is a placeholder for a more complex implementation.
    """
    def __init__(self):
        self.turns = defaultdict(list)

    def get_history(self, session_id: str) -> History:
        """
        Retrieve the conversation history for a given session ID.
        """
        return self.turns[session_id]


    def add_turn(self, session_id: str, turn: Turn):
        """
        Add a new turn to the conversation history for a given session ID.
        """
        self.turns[session_id].append(turn)