# User Proxy Agent

import autogen
import os

SYSTEM_MESSAGE = open(os.path.join(os.path.dirname(__file__), "userproxy.md")).read().strip()

def get_user_proxy(llm_config):
    return autogen.UserProxyAgent(
        name="User_Proxy",
        system_message=SYSTEM_MESSAGE,
        code_execution_config={
            "last_n_messages": 2,
            "work_dir": "groupchat",
            "use_docker": False,
        },
        human_input_mode="NEVER",
    )