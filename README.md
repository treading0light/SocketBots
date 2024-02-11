# SocketBots

"SocketBots" use the power of websockets (SocketIO), modular AI teams (CrewAI, LangChain), and multithreading adjacency to provide a more seamless interaction with your AI.

## Features
- Maintain conversation with your main AI personality while crews of Agents work in the background.
- Asynchronous Tool calls from main AI.
- SQLlite database for conversations
- More to come
SocketBots is meant to be an easy to set up AI teams using a Nuxt.js UI. Once crew's are defined in the server, you can either let your main AI delegate to them, or give them tasks manually from the UI.

# Setup
create a .env file in the back-end directory and add your openai key. 
```
OPENAI_API_KEY={your_key}
```
open a new terminal and:
```bash
cd back-end
pip install requirements.txt
flask run
```

In another terminal:
```bash
cd front-end
npm install
npm run dev
```

Open your browser to http://localhost:3000/
