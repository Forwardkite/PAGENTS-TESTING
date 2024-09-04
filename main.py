import os
import json
import autogen
from dotenv import load_dotenv

from autogen import OpenAIWrapper, register_function

from agents.user_proxy.user_proxy import get_user_proxy
from agents.planner.planner import get_planner
from agents.web_scraper.web_scraper import get_web_scraper
from agents.image_generation.image_generation import get_image_generation
from agents.conversible import get_conversible
from agents.facebook_poster.facebook_poster import get_facebook_poster
from agents.meta_authenticator.meta_authenticator import get_meta_authenticator
from agents.copy_writer.copy_writer import get_copy_writer
from agents.content_writer.content_writer import get_content_writer

from tools.ScraperFunc import scrape_website
from tools.imageGenerator import generate_and_save_images
from tools.facebookSheduler import post_to_facebook

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
web_scraper = get_web_scraper(llm_config)
image_generation = get_image_generation(llm_config)
facebook_poster = get_facebook_poster(llm_config)
conversible = get_conversible(llm_config)
meta_authenticator = get_meta_authenticator(llm_config)
copy_writer = get_copy_writer(llm_config)
content_writer = get_content_writer(llm_config)


groupchat = autogen.GroupChat(
    agents=[
        user_proxy,
        web_scraper,
        image_generation,
        conversible,
        facebook_poster,
        copy_writer,
        content_writer,
    ],
    messages=[],
    max_round=30,
)

register_function(
    scrape_website,
    caller=web_scraper,
    executor=user_proxy,
    name="ScraperFunctions",
    description="A simple website scraping tool",
)

register_function(
    generate_and_save_images,
    caller=image_generation,
    executor=user_proxy,
    name="Image_Generation_Agent",
    description="A simple image generator",
)

register_function(
    post_to_facebook,
    caller=facebook_poster,
    executor=user_proxy,
    name="facebook_poster",
    description="Used to post the generated images to facebook",
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
