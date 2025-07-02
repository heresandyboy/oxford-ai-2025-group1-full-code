# Comprehensive Logging System Guide

**All agent and tool interactions are automatically logged for learning and debugging!**

## 🔍 What Gets Logged

- **Agent Inputs & Outputs**: Every agent execution with full input/output capture
- **Tool Executions**: All tool calls with context and results
- **System Events**: Application start/stop, data loading, errors
- **Performance Tracking**: Execution timing and success/failure status

## 📁 Log Files Location

All logs are automatically saved to `/logs/` folder with format:

```
logs/logistics_agents_YYYYMMDD_HHMMSS_username.log
```

## ⚙️ **Controlling Log Output Truncation**

**Want to see FULL agent instructions and tool outputs?** Add these to your `.env` file:

```bash
# For COMPLETE output visibility (recommended for development)
LOG_TRUNCATE_AGENT_INSTRUCTIONS=0
LOG_TRUNCATE_AGENT_INPUT=0
LOG_TRUNCATE_AGENT_OUTPUT=0
LOG_TRUNCATE_TOOL_OUTPUT=0
LOG_TRUNCATE_TOOL_INPUT=0
```

**Available Truncation Controls:**

- `LOG_TRUNCATE_AGENT_INSTRUCTIONS` - Agent prompts/instructions (0 = full text)
- `LOG_TRUNCATE_AGENT_INPUT` - Input messages to agents (0 = full text)
- `LOG_TRUNCATE_AGENT_OUTPUT` - Agent response outputs (0 = full text)
- `LOG_TRUNCATE_TOOL_OUTPUT` - Tool execution results (0 = full text)
- `LOG_TRUNCATE_TOOL_INPUT` - Tool input context (0 = full text)

**Setting values:**

- `0` = **No truncation** (show complete text) - **RECOMMENDED for development**
- `>0` = Maximum characters before truncation

**Example for limited output:**

```bash
# For shorter logs in production/demo
LOG_TRUNCATE_AGENT_INSTRUCTIONS=500
LOG_TRUNCATE_AGENT_OUTPUT=800
LOG_TRUNCATE_TOOL_OUTPUT=400
```

## 🧪 Running Tests with Full Logging Visibility

**Basic Test Execution with Logging**:

```bash
# Run tests with live logging output visible
python -m pytest -m agent01 -v -s --log-cli-level=INFO

# Run tests with detailed file logging (shows all inputs/outputs)
python -m pytest -m agent01 -v -s --log-cli-level=DEBUG

# Run specific agent tests with full logging
python -m pytest -m agent02 -v -s --log-cli-level=INFO --tb=short
```

**Advanced Logging Commands**:

```bash
# Show ONLY agent/tool interactions (filter system noise)
python -m pytest -m agent01 -v -s --log-cli-level=INFO | grep -E "(🤖|🔧|✅|❌)"

# Run tests and save output to separate file
python -m pytest -m agent01 -v -s --log-cli-level=INFO > test_run_$(date +%Y%m%d_%H%M%S).log

# Run all tests except expensive ones with full logging
python -m pytest -m "not expensive" -v -s --log-cli-level=INFO --tb=short
```

**View Recent Logs**:

```bash
# View latest log file
ls -la logs/ | tail -1  # Show most recent log
tail -f logs/logistics_agents_*.log  # Follow latest log in real-time

# Search for specific agent interactions
grep "AGENT_OUTPUT" logs/logistics_agents_*.log | tail -10
grep "TOOL_OUTPUT" logs/logistics_agents_*.log | tail -10
```

**Cost-Aware Testing** (manage OpenAI API usage):

```bash
# Run cheap tests only (skip expensive orchestration)
python -m pytest -m "agent05 and not expensive" -v -s --log-cli-level=INFO

# Run the full end-to-end orchestration test (expensive!)
python -m pytest -m "agent05 and expensive" -v -s --log-cli-level=INFO

# Run all agents except expensive tests
python -m pytest -m "not expensive" -v -s --log-cli-level=INFO
```

**Log Analysis Commands**:

```bash
# View all agent executions from latest run
grep "🤖" logs/logistics_agents_*.log | tail -20

# View all tool executions
grep "🔧" logs/logistics_agents_*.log | tail -20

# View errors and failures
grep "❌\|ERROR" logs/logistics_agents_*.log

# View successful completions
grep "✅" logs/logistics_agents_*.log | tail -10
```

**Note**: Settings automatically reload from `.env` file - no manual reload needed! 🔄

## 🔍 Understanding the Logs

**Log Entry Types**:

- `AGENT_START`: Agent begins execution
- `AGENT_CONTEXT`: Shows data being processed
- `AGENT_SUCCESS`: Agent completed successfully
- `AGENT_OUTPUT`: Agent's final output
- `TOOL_INPUT`: Tool receives input data
- `TOOL_OUTPUT`: Tool produces result
- `SYSTEM_EVENT`: Application lifecycle events

**Example Log Entries**:

```
2025-01-XX 10:30:15 | INFO     | logistics_file       | AGENT_START | InventoryThresholdMonitor | Input: Analyze inventory thresholds...
2025-01-XX 10:30:15 | INFO     | logistics_file       | AGENT_CONTEXT | InventoryThresholdMonitor | 157 items, 23 below threshold
2025-01-XX 10:30:16 | INFO     | logistics_file       | TOOL_INPUT | ThresholdChecker | Context: 157 items
2025-01-XX 10:30:16 | INFO     | logistics_file       | TOOL_OUTPUT | ThresholdChecker | SUCCESS | ⚠️ THRESHOLD VIOLATIONS FOUND...
2025-01-XX 10:30:17 | INFO     | logistics_file       | AGENT_SUCCESS | InventoryThresholdMonitor | Output length: 1247 chars
```

## Daily Development Workflow

**Tests + Logs = quick development with full visibility**

1. Edit code → Run tests with logging → Review logs → When happy → Document in notebook
2. Check `/logs/` folder after every run for detailed execution traces
3. Use logging to understand agent/tool interactions and debug issues
