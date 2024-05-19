# 🌌 Nebulous AI
## Create AI agents with top-performing algorithms quickly.

### 1. Install Nebulous AI:

`pip install nebulousai`

### 2. Create an agent:

```
from nebulous.core.ability import Ability
from nebulous.core.brain import Brain
from nebulous.core.planning import Planner
from nebulous.core.short_term_memory import ShortTermMemory

from nebulous.agent import PlannerAgent
from nebulous.all_abilities import searchWikipediaAbility

brain = Brain(brain_system_prompt="Answer questions by using Wikipedia as a source.")
planner = Planner(agent_goal="find obama's hobbies")

agent = PlannerAgent(name="wiki_agent",
              brain=brain,
              long_term_memory=[],
              planner=planner)

agent.add_ability(searchWikipediaAbility)
```

### 3. Let the agent plan a task and act on it:

```
result = agent.act()
```

```

>> {'ability_name': 'Wikipedia Search', 'arguments': {'search_term': 'Barack Obama'}}
Performed 'search_wikipedia'.
{'ability_name': 'Reason', 'arguments': {'input_text': 'What hobbies does Barack Obama enjoy?'}}
Performed 'reason'.

Result: Some of Barack Obama's favorite hobbies include playing basketball, reading, writing, and spending time outdoors. He is also known to be a fan of music and enjoys playing the guitar. Additionally, he has been seen golfing and has a passion for cooking and trying new foods.
```