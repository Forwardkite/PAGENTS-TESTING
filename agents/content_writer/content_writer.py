# Copy Writer Agent

import autogen
import os

SYSTEM_MESSAGE = open(os.path.join(os.path.dirname(__file__), "content_writer.md")).read().strip()

def get_content_writer(llm_config):
    return autogen.AssistantAgent(
        llm_config=llm_config,
        name="Content_Writer_Agent",
        system_message=SYSTEM_MESSAGE
    )
