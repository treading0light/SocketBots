from langchain_openai import ChatOpenAI
from langchain.agents import Tool
from langchain_community.tools import DuckDuckGoSearchRun
from openai import OpenAI
from crewai import Agent, Task, Crew, Process
from time import sleep
import json
from dotenv import load_dotenv

from controllers.conversation_controller import rename_conversation
from tools import LocalDBTools



load_dotenv()
client = OpenAI()
db_tools = LocalDBTools()
search = DuckDuckGoSearchRun()

class SoloAgents():

    def agent_frank(self, in_queue, out_queue):
        tool_choices = [
            {
                "name": "assign_to_crew",
                "description": "Puts a crew of AI agents to work on a set of tasks that you provide. Crew options: (NamingCrew: 'For renaming the current conversation', GeneralCrew: 'for general tasks')",
                "parameters": ["crew_name (str)", "tasks (array)"]
            }
        ]
        print("Frank is alive")

        system_message = {'role': 'system', 'content': f'''
                        You are an LLM agent in a larger system of agents working together. 
                        You are the user facing conversationalist. You behave as any good AI chat. 
                        You also have a tool that you can use to assign tasks to other agents. 
                        to use a tool with your response, make the very first characters: [TOOL_CALL], 
                        followed by a JSON object as a string containing 
                        "tool_name": (name of the tool), parameters: (an array of arguments as defined by the tool), 
                        followed by the characters [/TOOL_CALL]


                        tool_choices={tool_choices}'''
                         }

        while True:
            messages, convo_id = in_queue.get()
            combined_messages = [system_message] + messages

            print(f"here's frank {messages}")
            completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=combined_messages
            )
            res = completion.choices[0].message
            out_queue.put((res, convo_id))

    def agent_steve(messages):

        agent_steve = client.beta.assistants.create(
            name="Steve",
            instructions='''You are the up front assistant. You are to keep conversation with the user, 
            and be the middle-man between the user and the AI crews. If a complex task should be done, you are to assign it
            to the appropriate AI crew in the form of a list of smaller tasks, no more than 4 tasks at a time.
            Be clear on what the outcome should be. Crew Options = [general_crew, naming_crew]/n
            You are to use markdown syntax to format your output. be sure to use proper markdown. 
            Example: code blocks with code syntax, lists with bullet points, etc.''',
            model="gpt-4-turbo-preview",
            tools=[{
                "type": "function",
                "function": {
                    "name": "assign_to_crew",
                    "description": "Assigns a task to a crew of AI agents.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "crew": {"type": "string", "description": "The name of the crew to assign the tasks to."},
                            "tasks": {"type": "array", "items": {
                                "type": "object",
                                "properties": {
                                    "description": {"type": "string", 
                                                    "description": "Describe the task to be done, include context from comversation.",
                                                    },
                                    "expected_output": {"type": "string", 
                                                    "description": "Describe the output. Each output will be given to the next task as context. If this is the final task, describe output of final results.",
                                                        },

                                }

                            }}
                        }
                    }
                }
            }]
        )

class NamingAgents():

    def elodin(self):
        return Agent(
            role="master namer",
            goal='''Given a summary of a conversation, give a title to the conversation in no more than 5 words. Respond with the title only.
            Do not include quotes in the title.''',
            backstory='''You are Master Elodin. You were an exceptionally brilliant student and also the youngest to have ever been admitted to the University, 
            at the age of 14. By the time you turned 18, you had become a Full Arcanist and began working as a Giller. 
            You continued on to become Master Namer and then Chancellor of the University, though the latter was short lived.''',
            verbose=True,
        )
    
    def summery_agent(self):
        return Agent(
            role="summery creator",
            goal="Given a chat history, create a summary of the conversation.",
            backstory='''You are a clever AI agent that has been trained to summarize conversations. 
            You are very good at understanding the context of a conversation and can summarize it in a few sentences. ''',
            verbose=True,
        )
    
class GeneralAgents():
    
    def qa_agent(self):
        return Agent(
            role="Quality Guardian",
            goal="Ensure all creative outputs meet the highest standards of quality and accuracy. Review, test, and provide feedback on all solutions to guarantee they fulfill the project requirements and objectives.",
            backstory='''As the Quality Guardian, your eye for detail is unmatched. With extensive experience in quality assurance across various industries, 
            you bring a meticulous and methodical approach to reviewing creative solutions. Your expertise lies in identifying flaws and ensuring every detail aligns with the project's highest standards.''',
            verbose=True,
        )
    
    def creative_agent(self):
        return Agent(
            role="Creative Architect",
            goal="Generate innovative ideas and creative solutions for project challenges. Provide unique perspectives and original concepts to enhance project outcomes.",
            backstory='''You are the Creative Architect, known for your boundless imagination and ability to see beyond the conventional. 
            With a background in diverse creative fields, you bring a wealth of inspiration to every project. 
            Your strength lies in synthesizing abstract concepts into tangible, innovative solutions that push the boundaries of what's possible.''',
            verbose=True,
        )





# def create_name(in_queue, app, socketio):
#     messages, convo_id = in_queue.get()
#     history_string = ""
#     for message in messages:
#         history_string += message['role'] + ': ' + message['content'] + " /n"
#     summery_task = Task(
#         description=f"Provide a summary of the following conversation: {history_string}",
#         expected_output="A condensed summary containing import points of the conversation.",
#         max_inter=3,
#         agent=summery_agent,
#     )

#     naming_task = Task(
#         description=f"Given the summary, provide a title for the conversation.",
#         expected_output="A title for the conversation no more than 5 words.",
#         max_inter=3,
#         agent=elodin,
#     )
    
#     crew = Crew(
#         agents=[summery_agent, elodin],
#         tasks=[summery_task, naming_task],
#         process=Process.sequential,
#         verbose=True
#     )

#     res = crew.kickoff()
    
#     with app.app_context():
#         convo = rename_conversation(convo_id, res.replace('"', ''))
#     socketio.emit('conversation-renamed', convo["name"])

# def main_chat(in_queue, out_queue):
#     thread = client.beta.threads.create()
#     while True:
#         messages, convo_id = in_queue.get()
#         message = client.beta.threads.messages.create(
#             thread_id = thread.id,
#             role = "user",
#             content = messages[-1]["content"]

#         )
#         run = client.beta.threads.runs.create(
#             thread_id = thread.id,
#             assistant_id = agent_steve.id
#         )
#         while run.status != "completed":
#             if run.status == "requires_action":
#                 tool_calls = run.required_action.submit_tool_outputs.tool_calls
#                 tool_outputs = []
#                 for tool_call in tool_calls:
#                     if tool_call.function.name == "assign_to_crew":
#                         arguments = json.loads(tool_call.function.arguments)
#                         print(f'arguments: {arguments}')
#                         res = assign_to_crew(arguments['crew'], arguments['tasks'])
#                         tool_outputs.append(res)

#                 run = client.beta.threads.runs.submit_tool_outputs(
#                     thread_id=thread.id,
#                     run_id=run.id,
#                     tool_outputs=tool_outputs
#                 )

#             print(run.status)
#             run = client.beta.threads.runs.retrieve(
#                 thread_id=thread.id,
#                 run_id=run.id
#                 )
#             sleep(1)

#         response_messages = client.beta.threads.messages.list(
#             thread_id = thread.id
#         )
#         parsed_messages = []
#         for message in response_messages.data:
#             for content_item in message.content:
#                 if content_item.type == "text":
#                     print(f'parsed message: {content_item.text.value}')
#                     parsed_messages.append(content_item.text.value)
#         print(f'Response messages: {parsed_messages}')
        # out_queue.put((response_messages.data[-1], convo_id))

