# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Structure

This is a Python agent development repository containing multiple agent implementations using Google ADK (Agent Development Kit). The repository has three main agent projects:

- `hotel-agent-app/` - Basic agent template using `google.adk.agents.llm_agent.Agent`
- `multi_tool_agent/` - Weather and time agent with custom tool functions using `google.adk.agents.Agent`  
- `my-first-agent/` - Tennis court booking agent with external toolbox integration using `google.adk.agents.llm_agent.LlmAgent`

## Key Dependencies

- `google.adk.agents` - Google Agent Development Kit for creating LLM agents
- `google.adk.tools` - ADK tools including `FunctionTool` for wrapping functions
- `google.adk.sessions` - Session management with `InMemorySessionService`
- `toolbox_core` - External toolbox client for loading external toolsets
- `zoneinfo` - Timezone handling for time-based functions

## Agent Architecture Patterns

### Basic Agent Pattern (`hotel-agent-app/`)
Uses `google.adk.agents.llm_agent.Agent` with minimal configuration - just model, name, description, and instruction.

### Function Tool Agent Pattern (`multi_tool_agent/`)
- Defines custom Python functions with proper docstrings
- Uses `google.adk.agents.Agent` with tools parameter
- Functions return structured dictionaries with status/result or error_message

### External Toolbox Integration (`my-first-agent/`)
- Uses `LlmAgent` from `google.adk.agents.llm_agent`
- Integrates with external toolbox via `ToolboxSyncClient`
- Combines external tools with custom `FunctionTool` instances
- Implements session management with `InMemorySessionService`

## Running Agents

To test basic functionality:
```bash
python test.py
```

## Development Notes

- All agent files are located in their respective directories with `__init__.py` files
- Agent functions should include comprehensive docstrings with Args and Returns sections
- External toolbox runs on `http://127.0.0.1:5001` (ensure it's running for `my-first-agent`)
- Custom tools should return structured dictionaries with consistent status/error patterns