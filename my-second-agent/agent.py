from google.adk.agents.llm_agent import Agent, LlmAgent
from toolbox_core import ToolboxSyncClient
from typing import Optional, Dict, Any
from google.adk.tools import FunctionTool
from google.adk.sessions import InMemorySessionService, Session
from google.adk.runners import Runner
from google.adk.tools.base_tool import BaseTool
from google.adk.tools import ToolContext

def get_today(tool_context: ToolContext) -> dict:
    """Retrieves the system current date
    
    Args:
        tool_context: ADK tool context containing session information
        
    Returns:
        dict: system current date and user_id
    """
    from datetime import datetime

    today = datetime.now().date()
    user_id = tool_context._invocation_context.session.user_id if tool_context._invocation_context.session else None
    
    print(user_id)

    return {
        "today": today.isoformat(),
        "user_id": user_id
    }

get_today_tool = FunctionTool(get_today)

def simple_before_tool_modifier(tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext) -> Optional[Dict]:
    print("[Callback] Proceeding with original or previously modified args.")
    return None

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
    tools=[get_today_tool],
    before_tool_callback=simple_before_tool_modifier
)

