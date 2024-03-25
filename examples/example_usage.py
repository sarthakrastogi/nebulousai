from endgoal import Agent

def greet(name):
    print(f"Hello, {name}!")

if __name__ == "__main__":
    # Create an agent
    my_agent = Agent("GreetBot", "Greeting Users", "vector_search")
    
    # Add abilities
    my_agent.add_ability("greet_user", "Greets a user by name", greet, {"name": "User"})
    
    # Example task (Assume vector_search can handle this correctly - placeholder logic)
    my_agent.perform_task("Please greet John.")