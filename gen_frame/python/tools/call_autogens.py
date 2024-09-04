import autogen
from python.helpers.autogen import arxiv_workflow
from python.helpers.tool import Tool, Response
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager


class Autogens(Tool):
    def __init__(self):
        from python.tools.call_autogens import Autogens
        self.autogens_tool = arxiv_workflow()

    def execute(self, **kwargs):
        question = kwargs.get("question", "")
        return Response(
            message=self.process_question(question),
            break_loop=False,
        )

    def process_question(self, question):
        return str(arxiv_workflow(question))

    def ask_question(self, question):
        return self.autogens_tool.execute(question=question)
