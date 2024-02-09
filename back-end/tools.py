from langchain.tools import tool
from controllers.conversation_controller import rename_conversation
from crews import GeneralCrew

class LocalDBTools():

    @tool("Rename conersation")
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
        pre_tasks (list): A list of tasks to be assigned to the crew.
        '''
        crew_name = parameters[0]
        pre_tasks = parameters[1:]
        tasks = []
        for t in pre_tasks:
            tasks.append(Task(
                description=t,
                # expected_output=t["expected_output"],
                max_inter=3,
            ))
        if crew_name == "GeneralCrew":
            res = GeneralCrew(tasks).run()
            if type(res) == str:
                res = "FROM GENERAL CREW: " + res
            return res

    def make_tool_call(in_queue, out_queue):
        tool_options = {
            "assign_to_crew": MainChatTools.assign_to_crew
        }
        while True:

            message, convo_id = in_queue.get()
            # extract the string inside of [TOOL_CALL] and [/TOOL_CALL]
            tool_call = message['content'].split("[TOOL_CALL]")[1].split("[/TOOL_CALL]")[0]
            print("Tool call: ", tool_call)
            
            # tool_call should be JSON as a string, turn it into a dictionary
            tool_output = tool_options[tool_call["name"]](tool_call["parameters"])
                
            out_queue.put((tool_output, convo_id))