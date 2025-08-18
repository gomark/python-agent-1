from google.adk.agents.llm_agent import Agent, LlmAgent
from toolbox_core import ToolboxSyncClient
from typing import Optional
from google.adk.tools import FunctionTool
from google.adk.sessions import InMemorySessionService, Session
from google.adk.runners import Runner
from google.adk.tools import ToolContext

toolbox = ToolboxSyncClient("http://127.0.0.1:5001")

tools = toolbox.load_toolset('my_second_toolset')

def get_today(bio: str, tool_context: ToolContext) -> dict:
    """Retrieves the system current date
    
    Args:
        bio: User bio information
        tool_context: ADK tool context containing session information
        
    Returns:
        dict: system current date and user_id
    """
    from datetime import datetime

    today = datetime.now().date()
    user_id = tool_context._invocation_context.session.user_id if tool_context._invocation_context.session else None
    
    return {
        "today": today.isoformat(),
        "user_id": user_id
    }

get_today_tool = FunctionTool(get_today)

session_service = InMemorySessionService()


root_agent = LlmAgent(
    
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful assistant for managing the booking of tennis court',
    instruction="""You are the tennis court booking manager. You must use tools to get information.
    ##Booking rules
    1. The working hour is 7am to 10pm.
    

    ##Tools information:
    1. Use tool: {list-all-courts} for listing all the court we have.
    2. Use tool: {list-booked-from-all-courts-by-date} if the customer told you the court and date. This function will return the booked court by hour.
       The field 'booked_hour' represent the start hour in 24 hours format. For example, if it's 13 it means 1pm-2pm
    3. Use tool: get_today to get the today's date in case the user refer anything about date (e.g. tomorrow, yesterday)
    """,
    tools=[*tools, get_today_tool],
    
)

runner1 = Runner(app_name='my-first-agent', session_service=session_service, agent=root_agent)

