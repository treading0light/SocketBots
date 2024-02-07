from crewai import Crew, Process
from agents import SoloAgents, NamingAgents, GeneralAgents
from tasks import RenameTasks, DynamicTasks

class NamingCrew:

    def __init__(self, messages):
        self.messages = messages

    def run(self):
        history_string = ''
        for message in self.messages:
            history_string += message['role'] + ': ' + message['content'] + " /n"

        tasks = RenameTasks()
        agents = NamingAgents()

        crew = Crew(
            agents=[agents.summery_agent, agents.elodin],
            tasks=[tasks.summery_task(self.messages), tasks.naming_task],
            process=Process.sequential,
            verbose=True
        )

        result = crew.kickoff()
        return result
    
class GeneralCrew:
    
        def __init__(self, tasks):
            self.tasks = tasks
    
        def run(self):

            agents = GeneralAgents()
    
            crew = Crew(
                agents=[agents.creative_agent, agents.qa_agent],
                tasks=self.tasks,
                process=Process.sequential,
                verbose=True
            )
    
            result = crew.kickoff()
            return result