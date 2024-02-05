from langchain.tools import tool
from controllers.conversation_controller import new_conversation, get_all_conversations, delete_conversation, rename_conversation
from controllers.message_controller import new_message, get_messages_in_conversation

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