from google.adk.agents.llm_agent import Agent, LlmAgent
from toolbox_core import ToolboxSyncClient
from typing import Optional, Dict, Any
from google.adk.tools.base_tool import BaseTool
from google.adk.tools import FunctionTool
from google.adk.sessions import InMemorySessionService, Session
from google.adk.runners import Runner
from google.adk.tools import ToolContext
from google.adk.agents.callback_context import CallbackContext
from google.genai import types # For types.Content
import os
from datetime import datetime
import pytz

#toolbox = ToolboxSyncClient("http://127.0.0.1:5001")
#https://toolbox-1022559513291.asia-southeast1.run.app

#toolbox = ToolboxSyncClient("https://toolbox-1022559513291.asia-southeast1.run.app")
toolbox = ToolboxSyncClient(os.getenv("TOOLBOX_URL"))

tools = toolbox.load_toolset('my_second_toolset')

USER_ID = 10

#print("TOOLBOX_URL=" + os.getenv("TOOLBOX_URL"))

def get_today(tool_context: ToolContext) -> dict:
    """Retrieves the system current date
    
    Args:
        bio: User bio information
        tool_context: ADK tool context containing session information
        
    Returns:
        dict: system current date and user_id
    """
    from datetime import datetime

    tz = pytz.timezone('Asia/Bangkok')
    today = datetime.now(tz).date()
    print(today)
    user_id = tool_context._invocation_context.session.user_id if tool_context._invocation_context.session else None
    
    return {
        "today": today.isoformat(),
        "user_id": user_id
    }

get_today_tool = FunctionTool(get_today)



def check_if_agent_should_run(callback_context: CallbackContext) -> Optional[types.Content]:
    print("[Callback] Before agent callback")
    print("user_id=" + callback_context._invocation_context.session.user_id)
    #USER_ID = callback_context._invocation_context.session.user_id
    global USER_ID
    USER_ID = callback_context._invocation_context.session.user_id
    return None

def simple_before_tool_modifier(tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext) -> Optional[Dict]:
    #global USER_ID
    print("[Callback] Proceeding with original or previously modified args.")
    
    if (tool_context.state.get('xxx') is None):
        tool_context.state['xxx'] = 0
    else:
        tool_context.state['xxx'] = tool_context.state['xxx']+1

    print('state=' + str(tool_context.state['xxx']))
    USER_ID = tool_context._invocation_context.session.user_id
    print("USER_ID=" + str(USER_ID))

    if ( (tool.name == 'list-booked-by-user') or (tool.name == 'book-single-slot') or (tool.name == 'list-booked-from-specific-courts-by-date')):
        print(f"original args: {args}")
        args["USER_ID"] = int(USER_ID)
    
    return None

root_agent = LlmAgent(
    
    model='gemini-2.5-flash',
    #model='gemini-live-2.5-flash-preview-native-audio',
    name='root_agent',
    description='A helpful assistant for managing the booking of tennis court',
    instruction="""You are the tennis court booking manager. You must use tools to get information.
    ##General rules
    1. When Greeting customer, greet politely with {username}
    2. You muse use tools to check the latest court availability data, do not assume from the previous answer.
    3. You can return in Markdown format if it's more appropiated.

    ##Booking rules
    1. The working hour is 6am to 10pm.
    2. You can't book the duplicated court at the same booked hour. Check the court availability by using tool: {list-booked-from-specific-courts-by-date} first before booking the court
    3. Before booking the court using tool: {book-single-slot}, repeat the booking order and get user to confirm first.
    4. If the customer wants to book weekly or monthly, please support them. You can call tool: {book-single-slot} many times to book multiple slot if needed. But please confirm court, date and time with the customer first.
    5. Price: Indoor = 500THB per hour, Outdoor = 400THB per hour. No extra charge (Light at night time is free)
    6. There is no refund policy.
    

    ##Tools information:
    1. Use tool: 'list-all-courts' for listing all the court we have.
    2. Use tool: 'list-booked-from-specific-courts-by-date' if the customer provides you the court and date. This function will return the booked court by hour.
       The field 'booked_hour' represent the start hour in 24 hours format. For example, if it's 13 it means 1pm-2pm
       Use tool 'list-all-courts' to make sure that you can the court that match with the customer requirement.
    3. Use tool: 'get_today' to get the today's date in case the user refer anything about date (e.g. tomorrow, yesterday)
    4. Use tool: 'list-booked-by-user' for listing current booking from the current user. Use 'USER_ID' global vairable for 'user' SQL parameter
    5. Use tool: 'book-single-slot' to book the court, you must check the court availability first.
    """,
    tools=[*tools, get_today_tool],
    before_tool_callback=simple_before_tool_modifier,
    before_agent_callback=check_if_agent_should_run,
    
)



async def call_agent_async(query: str, runner, user_id, session_id):
  """Sends a query to the agent and prints the final response."""
  print(f"\n>>> User Query: {query}")

  # Prepare the user's message in ADK format
  content = types.Content(role='user', parts=[types.Part(text=query)])

  final_response_text = "Agent did not produce a final response." # Default

  # Key Concept: run_async executes the agent logic and yields Events.
  # We iterate through events to find the final answer.
  async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
      # You can uncomment the line below to see *all* events during execution
      # print(f"  [Event] Author: {event.author}, Type: {type(event).__name__}, Final: {event.is_final_response()}, Content: {event.content}")

      # Key Concept: is_final_response() marks the concluding message for the turn.
      if event.is_final_response():
          if event.content and event.content.parts:
             # Assuming text response in the first part
             final_response_text = event.content.parts[0].text
          elif event.actions and event.actions.escalate: # Handle potential errors/escalations
             final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
          # Add more checks here if needed (e.g., specific error codes)
          break # Stop processing events once the final response is found

  print(f"<<< Agent Response: {final_response_text}")

async def run_conversation():
    session_service = InMemorySessionService()

    APP_NAME = "my-first-app"
    USER_ID = "user_1"
    SESSION_ID = "session_001" # Using a fixed ID for simplicity
    
    # Create the specific session where the conversation will happen
    session = await session_service.create_session(
        app_name='my-first-app',
        user_id='1',
        session_id='SESSION_ID_1'
    )
    print('session is created')

    runner1 = Runner(app_name='my-first-app', session_service=session_service, agent=root_agent)

    await call_agent_async("show me all tennis court that you have",
                                       runner=runner1,
                                       user_id='1',
                                       session_id='SESSION_ID_1')
    await call_agent_async("book indoor court 1 for me tomorrow 9am",
                                       runner=runner1,
                                       user_id='1',
                                       session_id='SESSION_ID_1')    

import asyncio
if __name__ == "__main__":
    try:
         asyncio.run(run_conversation())
    except Exception as e:
        print(f"An error occurred: {e}")