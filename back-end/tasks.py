from crewai import Task
from textwrap import dedent

class RenameTasks():

    def summery_task(self, agent, history:str):
        return Task(
            description=f"Provide a summary of the following conversation: {history}",
            expected_output="A condensed summary containing important details of the conversation.",
            max_inter=3,
            agent=agent,
        )
    
    def naming_task(self, agent):
        return Task(
            description=f"Given the summary create a title for the conversation.",
            expected_output="A title for the conversation, no more than 5 words.",
            max_inter=3,
            agent=agent,
        )
    
class DynamicTasks():

    def any_task(self, agent, description:str, expected_output:str):
        return Task(
            description=description,
            expected_output=expected_output,
            max_inter=3,
            agent=agent,
        )