### call_autogens:
Use autogens to solve subtasks.
Use "message" argument to send message. Instruct autogens about the workflow (arxive papper researcher,...) and his task in detail.
Use "reset" argument with "true" to start with autogen or "false" to continue with existing. For brand new tasks use "true", for followup conversation use "false". 
Explain to your autogens what is the higher level goal and what is his part.
Give him detailed instructions as well as good overview to understand what to do.
**Example usage**:
~~~json
{
    "thoughts": [
        "This task include complex workflows...",
        "I will ask autogens to fix...",
    ],
    "tool_name": "Call_autogens",
    "tool_args": {
        "message": "Well done, ...",
        "reset": "false"
    }
}
~~~