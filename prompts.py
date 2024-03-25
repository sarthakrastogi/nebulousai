class AbilitySearchPrompt:
    def __init__(self, abilities):
        self.abilities = abilities

    def generate_prompt(self):
        prompt = """
        You are part of an autonomous agent.
        You are provided with a list of abilities the agent has. The user will provide a task they want to accomplish.
        You will return the name of the most suitable ability to be used for this task.
        Only return this ability name and nothing else. Do not add any comments or explanations, or your response will not be parsed correctly.
        Below are the abilities:
        - """

        prompt += "\n".join([f"- {ability.ability_name}: {ability.description}" for ability in self.abilities])
        return prompt