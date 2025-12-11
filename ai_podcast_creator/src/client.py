import os
from restack_ai import Restack

# Initialize Restack client
client = Restack(
    engine_id=os.getenv("RESTACK_ENGINE_ID"),
    engine_address=os.getenv("RESTACK_ENGINE_ADDRESS"),
)
