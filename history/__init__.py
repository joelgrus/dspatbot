from typing import Literal
from typing_extensions import TypedDict
from abc import ABC, abstractmethod

class Turn(TypedDict):
    role: Literal["user", "assistant"]
    content: str

History = list[Turn]


class HistoryManager(ABC):
    @abstractmethod
    def get_history(self, session_id: str) -> History:
        """
        Retrieve the conversation history for a given session ID.
        """
        raise NotImplementedError
    
    @abstractmethod
    def add_turn(self, session_id: str, turn: Turn):
        """
        Add a new turn to the conversation history for a given session ID.
        """
        raise NotImplementedError

