from langchain.tools import tool
from crewai import Task
from controllers.conversation_controller import db, rename_conversation
from crews import GeneralCrew
from tasks import DynamicTasks
from controllers.message_controller import get_messages_in_conversation
import json

class LocalDBTools():

    @tool("Rename conversation")
    def rename_conversation_tool(conversation_id, new_name):
        """
        Renames an existing conversation to a new name.
        
        Parameters:
        conversation_id (int): The unique identifier of the conversation to be renamed.
        new_name (str): The new name for the conversation.
        
        Returns:
        The result of the rename operation, typically a success message or updated conversation object.
        """
        return rename_conversation(conversation_id, new_name)
    
    @tool("Get chat history")
    def get_chat_history_tool(conversation_id):
        """
        Gets the chat history of a conversation.
        
        Parameters:
        conversation_id (int): The unique identifier of the conversation to get the chat history of.
        
        Returns:
        The chat history of the conversation as one str.
        """
        messages = get_messages_in_conversation(conversation_id)
        chat_history = ''
        for message in messages:
            chat_history += message['role'] + ': ' + message['content'] + " /n"
        return messages
    
class MainChatTools():

    def __init__(self):
        pass

    @staticmethod
    def assign_to_crew(parameters):
        '''
        Puts a crew of AI agents to work on a set of tasks that you provide.
        Crew options: {naming_crew: "For renaming the current conversation", general_crew: "for general tasks"}

        Parameters:
        crew (str): The name of the crew to assign the tasks to.
        task_list (list): (dict) { description (str): A list of tasks to be assigned to the crew. agent (str): The name of the agent to be assigned to the task.}
        '''
        from agents import NamingAgents, GeneralAgents
        general_agents = GeneralAgents()
        naming_agents = NamingAgents()
        agents = {
                'qa_agent': general_agents.qa_agent(),
                'creative_agent': general_agents.creative_agent(),
                'research_agent': general_agents.research_agent(),
                'summery_agent': naming_agents.summery_agent(),
                'elodin': naming_agents.elodin()

            }
        crew_name = parameters[0]
        task_list = parameters[1]
        print(f'pre tasks {task_list}')
        tasks = []
        for t in task_list:

            print(f'one task: {t}')
            
            tasks.append(Task(
                description=t["description"],
                # expected_output=t["expected_output"],
                agent=agents[t["agent"]],
                max_inter=3,
            ))
            print(f'task array: {tasks}')
        if crew_name == "GeneralCrew":
            res = GeneralCrew(tasks).run()
            if type(res) == str:
                res = "FROM GENERAL CREW: " + res
            return res

    @staticmethod
    def make_tool_call(in_queue, out_queue):
        '''Tool to be used by standard completion endpoint.'''
        tool_options = {
            "assign_to_crew": MainChatTools.assign_to_crew
        }
        while True:

            message, convo_id = in_queue.get()
            # extract the string inside of [TOOL_CALL] and [/TOOL_CALL]
            tool_call = json.loads(message['content'].split("[TOOL_CALL]")[1].split("[/TOOL_CALL]")[0])
            print("Tool call: ", tool_call)
            
            # tool_call should be JSON as a string, turn it into a dictionary
            tool = tool_options[tool_call["tool_name"]]
            tool_output = tool(tool_call["parameters"])
            message = {"role": "assistant", "content": tool_output}
                
            out_queue.put((message, convo_id))

    @staticmethod
    def refine_tool_call(tool_call: dict):
        '''Refines the tool call message to be used by the tool call function.'''

        pass

    