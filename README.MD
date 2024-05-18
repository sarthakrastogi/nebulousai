# 🌌 Nebulous AI
## Create AI agents with top-performing algorithms quickly.

### 1. Install Nebulous AI:

`pip install nebulousai`

### 2. Create an agent:

```
from nebulous.agent import Agent

from nebulous.core.brain import Brain
from nebulous.core.ability import Ability
from nebulous.core.planning import Planner

brain = Brain(brain_system_prompt="Answer questions by using Wikipedia as a source.")
planner = Planner(agent_goal="find obama's hobbies")

agent = Agent(name="wiki agent",
              agent_type="plan_in_advance",
              brain=brain,
              long_term_memory=[],
              planner=planner)
```

### 3. Let the agent plan a task and act on it:

```
agent.plan()
agent.act()
```

```
{'ability_name': 'Wikipedia Search', 'arguments': {'search_term': 'Barack Obama'}}
Performed 'search_wikipedia'.

{'ability_name': 'Reason', 'arguments': {'input_text': "What are Barack Obama's hobbies?"}}
Performed 'reason'.
Result: Barack Obama's hobbies include playing basketball, reading, writing, and spending time with his family. He has also been known to enjoy golf, fishing, and watching sports. Additionally, he is a music lover and has been seen attending concerts and music festivals.
```

