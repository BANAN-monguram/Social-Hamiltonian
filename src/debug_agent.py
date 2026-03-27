from mesa import Agent, Model
from agents import HumanAgent
import sys

class MockModel(Model):
    def __init__(self):
        self.agents = []

try:
    print("Mesa Version check:")
    import mesa
    from mesa import Agent
    print(mesa.__version__)
    
    print("\n[DEBUG] Agent.__init__ signature inspection:")
    import inspect
    print(inspect.signature(Agent.__init__))
    
    print("\nInitializing Model...")
    model = MockModel()
    
    print("Attempt 1: Agent(unique_id, model)")
    try:
        a = Agent(1, model)
        print("Success: Agent(unique_id, model)")
    except Exception as e:
        print(f"Failed: {e}")

    print("Attempt 2: Agent(model)")
    try:
        a = Agent(model)
        print("Success: Agent(model)")
        print(f"ID assigned: {a.unique_id}")
    except Exception as e:
        print(f"Failed: {e}")

except Exception as e:
    print("\n[ERROR] Exception occurred:")
    print(e)
    import traceback
    traceback.print_exc()
