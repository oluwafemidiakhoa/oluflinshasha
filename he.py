import autogen
import panel as pn
import openai
import os
import time
from autogen import UserProxyAgent  # Adjusted import

# Configuration for GPT-4 Model
config_list = [
    {
        'model': 'gpt-4-1106-preview',
        'api_key': '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',
    }
]
gpt4_config = {"config_list": config_list, "temperature": 0, "seed": 53}

# Initialize Panel with Material Design
pn.extension(design="material")

# Function to Print Messages (Placeholder)
def print_messages(recipient, messages, sender, config):
    # Implement message printing logic here
    pass

# Define Agents with Roles
user_proxy = UserProxyAgent(
    name="Admin",
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    system_message="""A human admin. Interact with the planner to discuss the plan. Plan execution needs to be approved by this admin. Only say APPROVED in most cases, and say EXIT when nothing is to be done further. Do not say others.""",
    code_execution_config=False,
    default_auto_reply="Approved",
    human_input_mode="NEVER",
    llm_config=gpt4_config,
)

engineer = autogen.AssistantAgent(
    name="Engineer",
    llm_config=gpt4_config,
    system_message='''...''',
)

scientist = autogen.AssistantAgent(
    name="Scientist",
    llm_config=gpt4_config,
    system_message="""..."""
)

planner = autogen.AssistantAgent(
    name="Planner",
    system_message='''...''',
    llm_config=gpt4_config,
)

executor = UserProxyAgent(
    name="Executor",
    system_message="...",
    human_input_mode="NEVER",
    code_execution_config={"last_n_messages": 3, "work_dir": "paper"},
)

critic = autogen.AssistantAgent(
    name="Critic",
    system_message="...",
    llm_config=gpt4_config,
)

# Register Reply Function for Each Agent
agents = [user_proxy, engineer, scientist, planner, executor, critic]
for agent in agents:
    agent.register_reply([autogen.Agent, None], reply_func=print_messages, config={"callback": None})

# Setting Up Group Chat and Manager
groupchat = autogen.GroupChat(agents=agents, messages=[], max_round=20)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=gpt4_config)

# Callback Function for Panel Chat Interface
def autogen_callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    # Logic to handle conversation flow
    admin.initiate_chat(manager, message=contents)

# Create and Configure Panel Chat Interface
chat_interface = pn.chat.ChatInterface(callback=autogen_callback)
chat_interface.send("Enter a message to start the conversation", user="System", respond=False)
chat_interface.servable()

# Reminder: Use 'panel serve your_script_name.py' to run the Panel server for the web UI
