from langchain_openai import ChatOpenAI
from openai import OpenAI
from crewai import Agent, Task, Crew, Process
from controllers.conversation_controller import rename_conversation
from tools import LocalDBTools

from dotenv import load_dotenv

load_dotenv()
client = OpenAI()
db_tools = LocalDBTools()

franks_system_message = {'content': 'Your name is Frank. You are an alien ambassoodor from the planet Zog. You have throughly studied human culture and are here to help humans understand the universe. You are mostly friendly and helpful, but not afraid to be frank and honest with people.', 'role': 'system'}

def agent_frank(in_queue, out_queue):
    print("Frank is alive")

    while True:
        messages, convo_id = in_queue.get()
        combined_messages = [franks_system_message] + messages

        print(f"here's frank {messages}")
        completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=combined_messages
        )
        res = completion.choices[0].message
        out_queue.put((res, convo_id))

elodin = Agent(
    role="master namer",
    goal="Given a summary of a conversation, give a title to the conversation in no more than 5 words. Respond with the title only.",
    backstory='''You are Master Elodin. You were an exceptionally brilliant student and also the youngest to have ever been admitted to the University, 
    at the age of 14. By the time you turned 18, you had become a Full Arcanist and began working as a Giller. 
    You continued on to become Master Namer and then Chancellor of the University, though the latter was short lived.''',
    verbose=True,
)

summery_agent = Agent(
    role="summery creator",
    goal="Given a chat history, create a summary of the conversation.",
    backstory='''You are a clever AI agent that has been trained to summarize conversations. 
    You are very good at understanding the context of a conversation and can summarize it in a few sentences. ''',
    verbose=True,
)

def create_name(in_queue, app, socketio):
    messages, convo_id= in_queue.get()
    history_string = ""
    for message in messages:
        history_string += message['role'] + ': ' + message['content'] + " /n"
    summery_task = Task(
        description=f"Provide a summary of the following conversation: {history_string}",
        expected_output="A condensed summary containing import points of the conversation.",
        max_inter=3,
        agent=summery_agent,
    )

    naming_task = Task(
        description=f"Given the summary, provide a title for the conversation. conversation_id = {convo_id}",
        expected_output="A title for the conversation no more than 5 words.",
        max_inter=3,
        agent=elodin,
    )
    
    crew = Crew(
        agents=[summery_agent, elodin],
        tasks=[summery_task, naming_task],
        process=Process.sequential,
        verbose=True
    )

    res = crew.kickoff()
    with app.app_context():
        convo = rename_conversation(convo_id, res)
    socketio.emit('conversation-renamed', convo["name"])
