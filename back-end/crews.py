from crewai import Crew, Process, Task
from agents import NamingAgents, GeneralAgents
from tasks import RenameTasks
from controllers.message_controller import get_messages_in_conversation

class NamingCrew:

    def __init__(self, convo_id):
        self.convo_id = convo_id

    def run(self):
        messages = get_messages_in_conversation(self.convo_id)
        history_string = '# Chat History: \n'
        for message in messages:
            history_string += message['role'] + ': ' + message['content'] + " /n"

        tasks = RenameTasks()
        agents = NamingAgents()

        crew = Crew(
            agents=[agents.summery_agent, agents.elodin],
            tasks=[tasks.summery_task(history_string), tasks.naming_task],
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
                agents=[agents.research_agent(), agents.creative_agent()],
                tasks=self.tasks,
                process=Process.sequential,
                verbose=True,
                callback=self.report_progress
            )
    
            result = crew.kickoff()
            return result
        
        def report_progress(self):
            pass