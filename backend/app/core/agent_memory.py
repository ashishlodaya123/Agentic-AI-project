import threading
from typing import Dict, Any, List
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentMemory:
    """
    Shared memory system for agent communication and context propagation.
    Provides a centralized store for sharing information between agents.
    """
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(AgentMemory, cls).__new__(cls)
                    cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize the shared memory store."""
        self.memory_store: Dict[str, Any] = {}
        self.conversation_history: List[Dict[str, Any]] = []
        self.agent_outputs: Dict[str, Any] = {}
        self.lock = threading.RLock()  # Reentrant lock for thread safety
    
    def store(self, key: str, value: Any) -> None:
        """Store a value in the shared memory."""
        with self.lock:
            self.memory_store[key] = value
            logger.info(f"Stored {key} in agent memory")
    
    def retrieve(self, key: str, default: Any = None) -> Any:
        """Retrieve a value from the shared memory."""
        with self.lock:
            return self.memory_store.get(key, default)
    
    def update(self, key: str, value: Any) -> None:
        """Update an existing value in the shared memory."""
        with self.lock:
            if key in self.memory_store:
                self.memory_store[key] = value
                logger.info(f"Updated {key} in agent memory")
            else:
                self.store(key, value)
    
    def delete(self, key: str) -> bool:
        """Delete a key from the shared memory."""
        with self.lock:
            if key in self.memory_store:
                del self.memory_store[key]
                logger.info(f"Deleted {key} from agent memory")
                return True
            return False
    
    def get_all(self) -> Dict[str, Any]:
        """Get all stored values."""
        with self.lock:
            return self.memory_store.copy()
    
    def clear(self) -> None:
        """Clear all stored values."""
        with self.lock:
            self.memory_store.clear()
            self.conversation_history.clear()
            self.agent_outputs.clear()
            logger.info("Cleared agent memory")
    
    def add_to_history(self, agent_name: str, input_data: Any, output_data: Any) -> None:
        """Add an agent interaction to the conversation history."""
        with self.lock:
            self.conversation_history.append({
                "agent": agent_name,
                "input": input_data,
                "output": output_data,
                "timestamp": self._get_timestamp()
            })
    
    def get_history(self) -> List[Dict[str, Any]]:
        """Get the conversation history."""
        with self.lock:
            return self.conversation_history.copy()
    
    def store_agent_output(self, agent_name: str, output: Any) -> None:
        """Store an agent's output for other agents to access."""
        with self.lock:
            self.agent_outputs[agent_name] = output
            logger.info(f"Stored output for agent {agent_name}")
    
    def get_agent_output(self, agent_name: str, default: Any = None) -> Any:
        """Retrieve an agent's output."""
        with self.lock:
            return self.agent_outputs.get(agent_name, default)
    
    def get_all_agent_outputs(self) -> Dict[str, Any]:
        """Get all agent outputs."""
        with self.lock:
            return self.agent_outputs.copy()
    
    def clear_agent_outputs(self) -> None:
        """Clear all agent outputs."""
        with self.lock:
            self.agent_outputs.clear()
    
    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        import datetime
        return datetime.datetime.now().isoformat()
    
    def get_context_for_agent(self, agent_name: str) -> Dict[str, Any]:
        """Get relevant context for a specific agent."""
        with self.lock:
            context = {
                "shared_memory": self.memory_store.copy(),
                "agent_outputs": self.agent_outputs.copy(),
                "conversation_history": self.conversation_history[-5:] if self.conversation_history else [],  # Last 5 interactions
                "agent_name": agent_name
            }
            return context
    
    def merge_context(self, context: Dict[str, Any]) -> None:
        """Merge external context into the shared memory."""
        with self.lock:
            if "shared_memory" in context:
                self.memory_store.update(context["shared_memory"])
            if "agent_outputs" in context:
                self.agent_outputs.update(context["agent_outputs"])
            if "conversation_history" in context:
                self.conversation_history.extend(context["conversation_history"])

# Global instance
agent_memory = AgentMemory()

def get_agent_memory() -> AgentMemory:
    """Get the singleton agent memory instance."""
    return agent_memory