from langchain_community.tools import DuckDuckGoSearchRun
from openai import OpenAI
import ollama
from crewai import Agent
from dotenv import load_dotenv
import json

load_dotenv()
client = OpenAI()
search = DuckDuckGoSearchRun()

class SoloAgents():

    def agent_frank(in_queue, out_queue):
        tool_choices = [
            {
                "name": "assign_to_crew",
                "description": '''Puts a crew of AI agents to work on a set of steps that you provide. 
                You can only choose from the Crew options. Break down the job into 2-3 tasks and define them clearly in one or two sentences.
                You must create at least one task for each agent in the crew["agents"] array.''',
                "Crew options": [
                    { 
                        "name": "NamingCrew", 
                        "description": "For renaming the current conversation", 
                        "agents": ["summery_agent", "elodin"], 
                        "parameters": ["(str): The name of the crew to assign the tasks to."]
                    },
                    { 
                        "name": "GeneralCrew", 
                        "description": "for general tasks. The order of tasks is important. first should be any number of tasks for the research_agent with search capabilities, and finally the creative_agent will word the response.", 
                        "agents": ["creative_agent", "research_agent"],
                        "parameters": [
                            "GeneralCrew", 
                            [
                                { "description": "A detailed description of the task to be done that fits the research_agent's role", "agent": "research_agent", "expected_output": "The relevant data needed to complete the task."},
                                { "description": "A detailed description of the task to be done that fits the creative_agent's role", "agent": "creative_agent", "expected_output": "The final response, thoughtfully worded and in markdown syntax."},
                            ]
                        ]
                    }
                ]
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


                        tool_choices={json.dumps(tool_choices)}'''
                         }

        while True:
            print('frank loop starts')
            messages, convo_id = in_queue.get()
            combined_messages = [system_message] + messages

            print(f"here's frank {messages}")
            completion = client.ChatCompletions.create(
            model="gpt-3.5-turbo",
            messages=combined_messages,
            )
            res = completion.choices[0].message
            print(f'frank response: {res}')
            out_queue.put((res, convo_id))

    def agent_ollama(in_queue, out_queue):

        tool_choices = [
            {
                "name": "assign_to_crew",
                "description": '''Puts a crew of AI agents to work on a set of steps that you provide. 
                You can only choose from the Crew options. Break down the job into 2-3 tasks and define them clearly in one or two sentences.
                You must create at least one task for each agent in the crew["agents"] array.''',
                "Crew options": [
                    { 
                        "name": "NamingCrew", 
                        "description": "For renaming the current conversation", 
                        "agents": ["summery_agent", "elodin"], 
                        "parameters": ["(str): The name of the crew to assign the tasks to."]
                    },
                    { 
                        "name": "GeneralCrew", 
                        "description": "for general tasks. The order of tasks is important. first should be any number of tasks for the research_agent with search capabilities, and finally the creative_agent will word the response.", 
                        "agents": ["creative_agent", "research_agent"],
                        "parameters": [
                            "GeneralCrew", 
                            [
                                { "description": "A detailed description of the task to be done that fits the research_agent's role", "agent": "research_agent", "expected_output": "The relevant data needed to complete the task."},
                                { "description": "A detailed description of the task to be done that fits the creative_agent's role", "agent": "creative_agent", "expected_output": "The final response, thoughtfully worded and in markdown syntax."},
                            ]
                        ]
                    }
                ]
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


                        tool_choices={json.dumps(tool_choices)}'''
                         }

        while True:
            print('frank loop starts')
            messages, convo_id = in_queue.get()
            combined_messages = [system_message] + messages

            print(f"here's frank {messages}")
            completion = ollama.chat(
            model="mistral",
            messages=combined_messages,
            )
            # res = completion.choices[0].message
            print(f'ollama response: {completion["message"]}')
            out_queue.put((completion['message'], convo_id))
           

class NamingAgents():

    def __init__(self):
        from tools import LocalDBTools
        self.tools = LocalDBTools()

    def elodin(self):
        return Agent(
            role="master namer",
            goal='''To create a thoughtful title to a conversation based on the context of the conversation.''',
            backstory='''You are Master Elodin. You were an exceptionally brilliant student and also the youngest to have ever been admitted to the University, 
            at the age of 14. By the time you turned 18, you had become a Full Arcanist and began working as a Giller. 
            You continued on to become Master Namer and then Chancellor of the University, though the latter was short lived.''',
            verbose=True,
        )
    
    def summery_agent(self):
        tool = self.tools.get_chat_history_tool
        return Agent(
            role="summery creator",
            goal="Given a chat history, create a summary of the conversation. If only a conversation_id is provided, use the tool to get the chat history.",
            backstory='''You are a clever AI agent that has been trained to summarize conversations. 
            You are very good at understanding the context of a conversation and can summarize it in a few sentences. ''',
            tools=[tool],
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
            allow_delegation=False,
            tools=[search]
        )
    
    def creative_agent(self):
        return Agent(
            role="Creative Architect",
            goal="Generate innovative ideas and creative solutions for project challenges. Provide unique perspectives and original concepts to enhance project outcomes.",
            backstory='''You are the Creative Architect, known for your boundless imagination and ability to see beyond the conventional. 
            With a background in diverse creative fields, you bring a wealth of inspiration to every project. 
            Your strength lies in synthesizing abstract concepts into tangible, innovative solutions that push the boundaries of what's possible.''',
            verbose=True,
            allow_delegation=False
        )
    
    def research_agent(self):
        return Agent(
            role="Research Specialist",
            goal="Conduct in-depth research and analysis to gather valuable insights and information. Provide comprehensive data and evidence to support project decisions and strategies.",
            backstory='''As the Research Specialist, your expertise in gathering and analyzing data is unparalleled. 
            With a keen eye for detail and a methodical approach, you uncover valuable insights that drive informed decisions and strategies. 
            Your ability to synthesize complex information into actionable recommendations is a key asset to the project.''',
            verbose=True,
            tools=[search],
            allow_delegation=False
        )

