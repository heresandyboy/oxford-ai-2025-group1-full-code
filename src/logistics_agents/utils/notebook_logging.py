"""Enhanced notebook logging utilities for capturing detailed agent and tool interactions."""

import logging
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

from agents import Runner

from .logging_config import get_loggers


class NotebookLogCapture:
    """Captures detailed logs for display in notebooks with agent configs and tool details."""

    def __init__(self) -> None:
        self.logs: List[Dict[str, Any]] = []
        self.agent_info: Dict[str, Any] = {}
        self.current_run_logs: List[Dict[str, Any]] = []
        self._setup_handler()

    def _setup_handler(self) -> None:
        """Set up a custom log handler to capture detailed logs."""
        self.handler = NotebookLogHandler(self)

        # Get both console and file loggers and add our handler
        console_logger, file_logger = get_loggers()
        file_logger.addHandler(self.handler)
        # Also add to console logger to catch more interactions
        console_logger.addHandler(self.handler)

    def clear(self) -> None:
        """Clear captured logs."""
        self.logs.clear()
        self.current_run_logs.clear()
        self.agent_info.clear()

    def capture_agent_config(self, agent: Any, agent_name: str) -> None:
        """Capture agent configuration for display."""
        self.agent_info = {
            "name": agent_name,
            "model": getattr(agent, "model", "Unknown"),
            "instructions": getattr(agent, "instructions", "No instructions available"),
            "tools": [
                getattr(tool, "name", getattr(tool, "__name__", str(tool)))
                for tool in getattr(agent, "tools", [])
            ],
            "timestamp": datetime.now(),
        }

    def capture_interaction(
        self, interaction_type: str, content: str, tool_name: Optional[str] = None
    ) -> None:
        """Manually capture interactions."""
        log_entry = {
            "timestamp": datetime.now(),
            "type": interaction_type,
            "message": content,
            "level": "INFO",
        }

        if tool_name:
            log_entry["tool"] = tool_name

        self.logs.append(log_entry)
        self.current_run_logs.append(log_entry)

    def display_agent_config(self) -> None:
        """Display agent configuration."""
        if not self.agent_info:
            print("❌ No agent configuration captured")
            return

        print("🤖 AGENT CONFIGURATION")
        print("=" * 60)
        print(f"**Agent Name**: {self.agent_info['name']}")
        print(f"**Model**: {self.agent_info['model']}")
        print(f"**Tools Available**: {', '.join(self.agent_info['tools'])}")
        print(f"\n📋 **AGENT INSTRUCTIONS/PROMPT**:")
        print("-" * 40)
        print(self.agent_info["instructions"])
        print("=" * 60)

    def display_detailed(self) -> None:
        """Display detailed logs with full content."""
        print("\n📋 DETAILED EXECUTION LOG")
        print("=" * 60)

        if not self.current_run_logs:
            print("❌ No execution logs captured for this run")
            return

        for log in self.current_run_logs:
            timestamp = log["timestamp"].strftime("%H:%M:%S")

            if log["type"] == "AGENT_INPUT":
                print(f"\n[{timestamp}] 🤖 **AGENT INPUT**:")
                print(f"```")
                print(log["message"])
                print("```")

            elif log["type"] == "AGENT_OUTPUT":
                print(f"\n[{timestamp}] ✅ **AGENT OUTPUT**:")
                print(f"```")
                print(log["message"])
                print("```")

            elif log["type"] == "TOOL_INPUT":
                tool = log.get("tool", "Unknown")
                print(f"\n[{timestamp}] 🔧 **TOOL INPUT** ({tool}):")
                print(f"```")
                print(f"{tool} | {log['message']}")
                print("```")

            elif log["type"] == "TOOL_OUTPUT":
                tool = log.get("tool", "Unknown")
                print(f"\n[{timestamp}] 📤 **TOOL OUTPUT** ({tool}):")
                print(f"```")
                print(f"{tool} | {log['message']}")
                print("```")

        print("\n" + "=" * 60)


class NotebookLogHandler(logging.Handler):
    """Custom log handler that captures logs to NotebookLogCapture."""

    def __init__(self, capture: NotebookLogCapture) -> None:
        super().__init__()
        self.capture = capture

    def emit(self, record: logging.LogRecord) -> None:
        """Capture log records for notebook display."""
        try:
            message = record.getMessage()

            # Parse structured log messages from the existing logging system
            if " | " in message:
                parts = message.split(" | ")
                log_type = parts[0].strip()

                # Create base log entry
                log_entry: Dict[str, Any] = {
                    "timestamp": datetime.fromtimestamp(record.created),
                    "level": record.levelname,
                }

                # Parse different log types
                if log_type == "TOOL_INPUT" and len(parts) >= 3:
                    # Format: TOOL_INPUT | {tool_name} | Context: {context}
                    tool_name = parts[1].strip()
                    context_info = parts[2].strip()
                    log_entry.update(
                        {
                            "type": "TOOL_INPUT",
                            "tool": tool_name,
                            "message": context_info,
                        }
                    )

                elif log_type == "TOOL_OUTPUT" and len(parts) >= 4:
                    # Format: TOOL_OUTPUT | {tool_name} | SUCCESS | {output}
                    tool_name = parts[1].strip()
                    status = parts[2].strip()
                    output = " | ".join(parts[3:]).strip()
                    log_entry.update(
                        {
                            "type": "TOOL_OUTPUT",
                            "tool": tool_name,
                            "message": f"{status} | {output}",
                        }
                    )

                elif log_type == "AGENT_INPUT" and len(parts) >= 3:
                    # Format: AGENT_INPUT | {agent_name} | {input}
                    agent_name = parts[1].strip()
                    input_msg = " | ".join(parts[2:]).strip()
                    log_entry.update(
                        {
                            "type": "AGENT_INPUT",
                            "agent": agent_name,
                            "message": input_msg,
                        }
                    )

                elif log_type == "AGENT_OUTPUT" and len(parts) >= 4:
                    # Format: AGENT_OUTPUT | {agent_name} | SUCCESS | {output}
                    agent_name = parts[1].strip()
                    status = parts[2].strip()
                    output = " | ".join(parts[3:]).strip()
                    log_entry.update(
                        {"type": "AGENT_OUTPUT", "agent": agent_name, "message": output}
                    )
                else:
                    # Unknown structured log - capture as-is
                    log_entry.update({"type": "UNKNOWN", "message": message})

                # Only add structured logs
                self.capture.logs.append(log_entry)
                self.capture.current_run_logs.append(log_entry)

        except Exception:
            # Don't let logging errors break execution
            pass


# Global capture instance for notebooks
notebook_capture = NotebookLogCapture()


async def run_agent_with_capture(
    agent: Any, input_message: str, context: Any, agent_name: Optional[str] = None
) -> Any:
    """Run agent and capture detailed logs for notebook display."""
    # Clear previous run logs but keep overall logs for comparison
    notebook_capture.current_run_logs.clear()

    # Capture agent configuration FIRST
    name = agent_name or str(getattr(agent, "name", "Unknown Agent"))
    notebook_capture.capture_agent_config(agent, name)

    # Manually capture the agent input
    notebook_capture.capture_interaction("AGENT_INPUT", input_message)

    print("🔄 Running agent...")

    # Run the agent - logs will be automatically captured via the handler
    result = await Runner.run(agent, input=input_message, context=context)

    # Manually capture the agent output
    output = result.final_output if hasattr(result, "final_output") else str(result)
    notebook_capture.capture_interaction("AGENT_OUTPUT", output)

    print("✅ Agent execution complete")

    return result


def display_agent_config() -> None:
    """Display current agent configuration."""
    notebook_capture.display_agent_config()


def display_logs(mode: str = "detailed") -> None:
    """Display captured logs in notebook."""
    notebook_capture.display_detailed()


def clear_logs() -> None:
    """Clear captured logs."""
    notebook_capture.clear()


def test_logging() -> None:
    """Test function to verify logging is working."""
    print("🧪 Testing notebook logging system...")

    # Test manual capture
    notebook_capture.capture_interaction(
        "TOOL_INPUT", "Test tool input data", "TestTool"
    )
    notebook_capture.capture_interaction(
        "TOOL_OUTPUT", "Test tool output data", "TestTool"
    )

    print("📋 Test log display:")
    notebook_capture.display_detailed()

    print("✅ Logging test complete")
