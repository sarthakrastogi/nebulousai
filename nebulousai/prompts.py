class AbilitySearchPrompt:
    def __init__(self, abilities):
        self.abilities = abilities

    def generate_prompt(self):
        prompt = """
        You are part of an autonomous agent.
        You are provided with a list of abilities the agent has. The user will provide a task they want to accomplish.
        You will return the name of the most suitable ability to be used for this task, as well as the values of the arguments to be plugged in.
        
        # Example ability:
        create_sheet: Creates a new worksheet.
        Arguments: sheet_name, company_name

        # Example user task:
        - Make a sheet named Sarthak for OpenAI.

        # Example response:
        {"ability_name" : "create_sheet", "sheet_name" : "Sarthak", "company_name" : "OpenAI"}

        Return your response strictly in the above JSON format. Only return this JSON and nothing else.
        Do not add any comments or explanations, or your response will not be parsed correctly.
        Below are the abilities:
        - """

        prompt += "\n".join([f"- {ability.ability_name}: {ability.description}\nArguments: {', '.join(ability.args)}\n" for ability in self.abilities])
        return prompt