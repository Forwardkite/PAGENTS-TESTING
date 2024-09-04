# Planner Agent

import autogen
import os

SYSTEM_MESSAGE = open(os.path.join(os.path.dirname(__file__), "planner.md")).read().strip()

def get_planner(llm_config):
    return autogen.AssistantAgent(
        llm_config=llm_config,
        name="Planner",
        system_message=SYSTEM_MESSAGE
    )
