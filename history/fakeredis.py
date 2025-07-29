from typing import Any
from collections import OrderedDict

from . import Turn, History, HistoryManager

class FakeRedis:
    """
    A fake, in-memory Redis-like class with an LRU eviction policy
    to simulate session management without a real Redis server.
    It mimics the 'rpush' and 'lrange' commands.
    """
    def __init__(self, max_sessions: int = 100):
        """
        Initializes the fake Redis store.
        :param max_sessions: The maximum number of user sessions to keep in memory.
        """
        self._data: OrderedDict[str, Any] = OrderedDict()
        self.max_sessions = max_sessions

    def _enforce_lru(self):
        """Evicts the least recently used session if the store is full."""
        if len(self._data) > self.max_sessions:
            # popitem(last=False) removes the first item inserted (LRU)
            self._data.popitem(last=False)

    def rpush(self, name: str, *values):
        """
        Mimics Redis RPUSH. Appends values to the list associated with a key.
        Moves the key to the end (most recently used).
        """
        if name not in self._data:
            self._data[name] = []
        
        self._data[name].extend(values)
        # Move to end to mark as most recently used
        self._data.move_to_end(name)
        
        self._enforce_lru()
        return len(self._data[name])

    def lrange(self, name: str, start: int, end: int):
        """
        Mimics Redis LRANGE. Retrieves a range of elements from a list.
        Moves the key to the end (most recently used).
        """
        if name not in self._data:
            return []
        
        # In Python, slicing's `end` is exclusive. In Redis, it's inclusive.
        if end == -1:
            end_slice = None
        else:
            end_slice = end + 1
            
        # Move to end to mark as most recently used
        self._data.move_to_end(name)
        
        return self._data[name][start:end_slice]

    def flushall(self):
        """Mimics Redis FLUSHALL for easy cleanup during testing."""
        self._data.clear()

class FakeRedisHistoryManager(HistoryManager):
    """
    A history manager that uses FakeRedis to store conversation history.
    """
    def __init__(self, redis: FakeRedis = FakeRedis(max_sessions=100)):
        self.redis = redis

    def get_history(self, session_id: str) -> History:
        """
        Retrieve the conversation history for a given session ID.
        """
        return self.redis.lrange(session_id, 0, -1)

    def add_turn(self, session_id: str, turn: Turn):
        """
        Add a new turn to the conversation history for a given session ID.
        """
        self.redis.rpush(session_id, turn)