"""Agent execution helper with comprehensive logging.

This module provides centralized agent execution with automatic logging of
inputs, outputs, and performance metrics for all logistics agents.
"""

from typing import Any, Optional, TypeVar, Generic, Callable
from functools import wraps
from agents import Runner, Agent
from .logging_config import get_loggers, log_system_event
from ..config.settings import settings

T = TypeVar('T')


def log_agent_execution(agent_class):
    """
    Class decorator to automatically log agent execution.

    This decorator wraps the agent's __init__ method to set up logging
    and can be used to monitor agent creation and execution patterns.

    Args:
        agent_class: The agent class to wrap with logging

    Returns:
        Wrapped agent class with logging capabilities
    """
    original_init = agent_class.__init__

    @wraps(original_init)
    def logged_init(self, *args, **kwargs):
        # Call original init
        original_init(self, *args, **kwargs)

        # Log agent initialization
        console_logger, file_logger = get_loggers()
        agent_name = getattr(self.agent, 'name', agent_class.__name__)
        instructions = getattr(self.agent, 'instructions',
                               'No instructions available')
        model = getattr(self.agent, 'model', 'Unknown model')

        console_logger.info(f"🤖 {agent_name} initialized")
        file_logger.info(f"AGENT_INIT | {agent_name} | Model: {model}")

        # Use truncation settings for agent instructions
        truncated_instructions = settings.truncate_text(
            instructions, settings.log_truncate_agent_instructions)
        file_logger.info(
            f"AGENT_INSTRUCTIONS | {agent_name} | {truncated_instructions}")

        # Store original agent for logging wrapper
        self._original_agent = self.agent

        # Wrap the agent's execution if it has tools
        if hasattr(self.agent, 'tools') and self.agent.tools:
            tool_names = [getattr(tool, 'name', str(tool))
                          for tool in self.agent.tools]
            file_logger.info(
                f"AGENT_TOOLS | {agent_name} | Tools: {tool_names}")

    agent_class.__init__ = logged_init
    return agent_class


class LoggedAgentRunner:
    """Helper class for running agents with comprehensive logging."""

    @staticmethod
    async def run_agent(
        agent: Agent[T],
        input_message: str,
        context: T,
        agent_name: Optional[str] = None
    ) -> Any:
        """
        Run an agent with comprehensive input/output logging.

        Args:
            agent: The agent to run
            input_message: Input message for the agent
            context: Context data for the agent
            agent_name: Optional agent name for logging (defaults to agent.name)

        Returns:
            Agent execution result
        """
        console_logger, file_logger = get_loggers()

        # Use provided name or extract from agent
        name = agent_name or getattr(agent, 'name', 'UnknownAgent')

        # Log agent execution start
        console_logger.info(f"🤖 {name} starting...")

        # Use truncation settings for agent input
        truncated_input = settings.truncate_text(
            input_message, settings.log_truncate_agent_input)
        file_logger.info(f"AGENT_START | {name} | Input: {truncated_input}")

        # Log context information
        context_info = "No context"
        if hasattr(context, 'items'):
            context_info = f"{len(context.items)} items"
            below_threshold = len([item for item in context.items if hasattr(
                item, 'is_below_threshold') and item.is_below_threshold])
            context_info += f", {below_threshold} below threshold"

        file_logger.info(f"AGENT_CONTEXT | {name} | {context_info}")

        try:
            # Execute the agent
            result = await Runner.run(agent, input=input_message, context=context)

            # Log successful completion
            output_str = str(result.final_output) if hasattr(
                result, 'final_output') else str(result)
            console_logger.info(f"✅ {name} completed successfully")
            file_logger.info(
                f"AGENT_SUCCESS | {name} | Output length: {len(output_str)} chars")

            # Use truncation settings for agent output
            truncated_output = settings.truncate_text(
                output_str, settings.log_truncate_agent_output)
            file_logger.info(f"AGENT_OUTPUT | {name} | {truncated_output}")

            return result

        except Exception as e:
            # Log error
            console_logger.error(f"❌ {name} failed: {str(e)}")
            file_logger.error(f"AGENT_ERROR | {name} | {str(e)}")

            # Re-raise the exception
            raise

    @staticmethod
    def log_agent_call(agent_name: str, tool_name: str, input_data: str = "") -> None:
        """
        Log when an agent calls a tool (for manual logging in agents).

        Args:
            agent_name: Name of the calling agent
            tool_name: Name of the tool being called
            input_data: Input data being passed to the tool
        """
        console_logger, file_logger = get_loggers()
        console_logger.info(f"🤖 {agent_name} → 🔧 {tool_name}")

        # Use truncation settings for tool input data
        truncated_input = settings.truncate_text(
            input_data, settings.log_truncate_tool_input)
        file_logger.info(
            f"AGENT_TOOL_CALL | {agent_name} | {tool_name} | {truncated_input}")


# Convenience function for backward compatibility
async def run_agent_with_logging(
    agent: Agent[T],
    input_message: str,
    context: T,
    agent_name: Optional[str] = None
) -> Any:
    """
    Convenience function to run an agent with logging.

    Args:
        agent: The agent to run
        input_message: Input message for the agent
        context: Context data for the agent
        agent_name: Optional agent name for logging

    Returns:
        Agent execution result
    """
    return await LoggedAgentRunner.run_agent(agent, input_message, context, agent_name)
