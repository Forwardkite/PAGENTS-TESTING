import autogen
from agent import Agent
from python.helpers.tool import Tool, Response
from python.helpers import files
from python.helpers.print_style import PrintStyle
import os
import json
from autogen import OpenAIWrapper, register_function

from agents.user_proxy.user_proxy import get_user_proxy
from agents.planner.planner import get_planner
from agents.web_scraper.web_scraper import get_web_scraper
from agents.image_generation.image_generation import get_image_generation
from agents.conversible import get_conversible
from agents.facebook_poster.facebook_poster import get_facebook_poster
from agents.meta_authenticator.meta_authenticator import get_meta_authenticator

from tools.ScraperFunc import scrape_website
from tools.imageGenerator import generate_and_save_images
from tools.facebookSheduler import post_to_facebook

class Delegation(Tool):
    def execute(self, message="", reset="", **kwargs):
        # Load configuration list from JSON file
        with open('OAI_CONFIG_LIST', 'r') as file:
            config_list = json.load(file)

        llm_config = next((config for config in config_list if config["model"]), None)

        client = OpenAIWrapper(config_list=config_list)

        if not llm_config:
            raise ValueError("No valid configuration found for the specified model.")

        api_key = llm_config.get("api_key")
        model = llm_config.get("model")

        # Set the OpenAI API key as an environment variable internally
        os.environ['OPENAI_API_KEY'] = api_key

        llm_config = {
            "model": model,
            "api_key": api_key,
            "cache_seed": 42
        }

        user_proxy = get_user_proxy(llm_config)
        planner = get_planner(llm_config)
        web_scraper = get_web_scraper(llm_config)
        image_generation = get_image_generation(llm_config)
        facebook_poster = get_facebook_poster(llm_config)
        conversible = get_conversible(llm_config)
        meta_authenticator = get_meta_authenticator(llm_config)

        # Set up the GroupChat with the defined agents
        groupchat = autogen.GroupChat(
            agents=[user_proxy, web_scraper, image_generation, conversible, facebook_poster, meta_authenticator],
            messages=[],
            max_round=7,
            speaker_selection_method='round_robin',
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

        # Initiate the chat with the UserProxyAgent
        user_proxy.initiate_chat(
            manager,
            message=message,
        )

        """
        Prints a summary of the usage statistics for the OpenAI API client.
        """
        client.print_usage_summary()

        return "Chat initiated with message: " + message
