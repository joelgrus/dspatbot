import dspy

from .history import History, HistoryManager
from .tools import ALL_TOOLS


class ConversationalSignature(dspy.Signature):
    history: History = dspy.InputField(desc="The conversation history.")
    query = dspy.InputField(desc="The user's last question.")
    personality = dspy.InputField(desc="The personality of the assistant.")
    answer = dspy.OutputField(desc="The final answer.")

class Chatbot(dspy.Module):
    def __init__(self, history_manager: HistoryManager, personality: str = "You are a helpful assistant."):
        super().__init__()
        self.agent = dspy.ReAct(ConversationalSignature, tools=ALL_TOOLS)
        self.personality = personality
        self.history_manager = history_manager

    def forward(self, query: str, session_id: str) -> ConversationalSignature:
        # Pass the history to the agent.
        history = self.history_manager.get_history(session_id)
        result = self.agent(query=query, personality=self.personality, history=history)

        # Update the history with the new turn.
        self.history_manager.add_turn(session_id, {"role": "user", "content": query})
        self.history_manager.add_turn(session_id, {"role": "assistant", "content": result.answer})

        return result
