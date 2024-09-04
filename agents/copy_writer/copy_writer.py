# Copy Writer Agent

import autogen
import os

SYSTEM_MESSAGE = open(os.path.join(os.path.dirname(__file__), "copy_writer.md")).read().strip()

def get_copy_writer(llm_config):
    return autogen.AssistantAgent(
        llm_config=llm_config,
        name="Copy_Writer_Agent",
        system_message=SYSTEM_MESSAGE
    )
