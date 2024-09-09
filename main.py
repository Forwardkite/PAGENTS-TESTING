import os
import json
import autogen
from dotenv import load_dotenv

from autogen import OpenAIWrapper, register_function

from agents.user_proxy.user_proxy import get_user_proxy
from agents.planner.planner import get_planner
from agents.copy_writer.copy_writer import get_copy_writer
from agents.content_writer.content_writer import get_content_writer

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
model = os.getenv("OPENAI_MODEL")

if not api_key or not model:
    raise ValueError("API key or model is missing. Ensure they are set in the .env file.")

llm_config = {"model": model, "api_key": api_key, "cache_seed": 42}

client = OpenAIWrapper(config_list=[llm_config])

os.environ["OPENAI_API_KEY"] = api_key

user_proxy = get_user_proxy(llm_config)
planner = get_planner(llm_config)
copy_writer = get_copy_writer(llm_config)
content_writer = get_content_writer(llm_config)


groupchat = autogen.GroupChat(
    agents=[
        user_proxy,
        copy_writer,
        content_writer,
    ],
    messages=[],
    max_round=30,
)


manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)


def ask_for_more():
    while True:
        more_input = (
            input("\nIs there anything else I can assist you with? (yes/no): ")
            .strip()
            .lower()
        )
        if more_input == "yes":
            user_message = input("Please enter your message: ")
            user_proxy.initiate_chat(
                manager,
                message=user_message,
            )
        elif more_input == "no":
            print("Thank you! Have a great day!")
            break
        else:
            print("Please enter 'yes' or 'no'.")


user_message = input("Please enter your message: ")

user_proxy.initiate_chat(
    manager,
    message=user_message,
)

ask_for_more()

client.print_usage_summary()
