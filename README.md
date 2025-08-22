# Python Agent Development Kit Repository

This repository contains multiple agent implementations using Google's Agent Development Kit (ADK), demonstrating different patterns and approaches for building LLM-powered agents.

## Project Structure

```
├── hotel-agent-app/          # Basic agent template
├── multi_tool_agent/         # Weather and time agent with custom tools
├── my-first-agent/          # Tennis court booking agent with external toolbox
├── my-second-agent/         # Additional agent implementation
├── test.py                  # Test runner for agents
├── deploy-first-agent.sh    # Deployment script
└── CLAUDE.md               # Development guidelines
```

## Agent Implementations

### 1. Hotel Agent (`hotel-agent-app/`)
- **Type**: Basic agent using `google.adk.agents.llm_agent.Agent`
- **Purpose**: Template implementation with minimal configuration
- **Features**: Model, name, description, and instruction setup

### 2. Multi-Tool Agent (`multi_tool_agent/`)
- **Type**: Function tool agent using `google.adk.agents.Agent`
- **Purpose**: Weather and time information provider
- **Features**: Custom Python functions with proper docstrings, structured return values

### 3. Tennis Court Booking Agent (`my-first-agent/`)
- **Type**: External toolbox integration using `google.adk.agents.llm_agent.LlmAgent`
- **Purpose**: Tennis court booking system
- **Features**: External toolbox integration, session management, combined tool sets

### 4. Second Agent (`my-second-agent/`)
- **Type**: Additional agent implementation
- **Purpose**: Extended functionality demonstration

## Key Dependencies

- `google.adk.agents` - Google Agent Development Kit core
- `google.adk.tools` - ADK tools including `FunctionTool`
- `google.adk.sessions` - Session management with `InMemorySessionService`
- `toolbox_core` - External toolbox client integration
- `zoneinfo` - Timezone handling for time-based functions

## Getting Started

### Prerequisites

1. Python 3.8+
2. Google ADK installed
3. External toolbox service running on `http://127.0.0.1:5001` (for `my-first-agent`)

### Installation

1. Clone the repository
2. Install dependencies for specific agents:
   ```bash
   cd my-first-agent
   pip install -r requirements.txt
   ```

### Running Agents

Test basic functionality:
```bash
python test.py
```

Deploy the first agent:
```bash
./deploy-first-agent.sh
```

## Architecture Patterns

### Basic Agent Pattern
- Uses `google.adk.agents.llm_agent.Agent`
- Minimal configuration approach
- Suitable for simple conversational agents

### Function Tool Agent Pattern
- Custom Python functions with comprehensive docstrings
- Structured return dictionaries with status/result or error_message
- Uses `google.adk.agents.Agent` with tools parameter

### External Toolbox Integration
- `LlmAgent` from `google.adk.agents.llm_agent`
- External toolbox via `ToolboxSyncClient`
- Session management with `InMemorySessionService`
- Combines external and custom tools

## Development Guidelines

- All agent files include `__init__.py` for proper module structure
- Functions require comprehensive docstrings with Args and Returns sections
- Custom tools return structured dictionaries with consistent patterns
- External toolbox must be running for full functionality testing

## Contributing

When developing new agents:
1. Follow existing architectural patterns
2. Include proper documentation and docstrings
3. Test with `python test.py`
4. Update this README if adding new agent types

## License

[Add your license information here]