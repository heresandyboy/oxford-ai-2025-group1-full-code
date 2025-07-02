"""Logging configuration with enhanced file logging and agent/tool tracking."""

import getpass
import logging
from datetime import datetime
from functools import wraps
from pathlib import Path
from typing import Awaitable, Callable, Optional, ParamSpec, TypeVar, cast

from rich.logging import RichHandler

from ..config.settings import settings

# Type hints for decorators
P = ParamSpec("P")
T = TypeVar("T")

# Global logger instances
_console_logger: Optional[logging.Logger] = None
_file_logger: Optional[logging.Logger] = None


def setup_logging() -> tuple[logging.Logger, logging.Logger]:
    """Set up application logging with both console and file handlers.

    Returns:
        Tuple of (console_logger, file_logger) for different logging needs
    """
    global _console_logger, _file_logger

    if _console_logger and _file_logger:
        return _console_logger, _file_logger

    # Create logs directory if it doesn't exist
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    # Generate log filename with timestamp and user
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    username = getpass.getuser()
    log_filename = f"logistics_agents_{timestamp}_{username}.log"
    log_filepath = logs_dir / log_filename

    # Console logger with Rich formatting
    _console_logger = logging.getLogger("logistics_console")
    _console_logger.setLevel(getattr(logging, settings.log_level.upper()))

    # Clear existing handlers
    _console_logger.handlers.clear()

    # Rich handler for console
    console_handler = RichHandler(rich_tracebacks=True)
    console_handler.setLevel(getattr(logging, settings.log_level.upper()))
    console_format = logging.Formatter("%(message)s")
    console_handler.setFormatter(console_format)
    _console_logger.addHandler(console_handler)

    # File logger with detailed formatting
    _file_logger = logging.getLogger("logistics_file")
    _file_logger.setLevel(logging.DEBUG)  # Always capture DEBUG to file

    # Clear existing handlers
    _file_logger.handlers.clear()

    # File handler
    file_handler = logging.FileHandler(log_filepath, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)-20s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(file_format)
    _file_logger.addHandler(file_handler)

    # Set specific logger levels for external libraries
    logging.getLogger("openai").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    # Log startup info
    _file_logger.info(f"=== LOGISTICS AGENTS SESSION START ===")
    _file_logger.info(f"User: {username}")
    _file_logger.info(f"Log file: {log_filepath}")
    _file_logger.info(
        f"Settings: model={settings.openai_model}, log_level={settings.log_level}"
    )
    _console_logger.info(f"📝 Logging to: {log_filepath}")

    return _console_logger, _file_logger


def get_loggers() -> tuple[logging.Logger, logging.Logger]:
    """Get the console and file loggers, creating them if needed."""
    if _console_logger and _file_logger:
        return _console_logger, _file_logger
    return setup_logging()


def log_agent_interaction(
    agent_name: str,
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """Decorator to log agent inputs and outputs.

    Args:
        agent_name: Name of the agent for logging identification

    Returns:
        Decorated function with input/output logging
    """

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @wraps(func)
        async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            console_logger, file_logger = get_loggers()

            # Log input
            input_msg = (
                f"🤖 {agent_name} INPUT: {args[1] if len(args) > 1 else 'No input'}"
            )
            console_logger.info(f"🤖 {agent_name} starting...")

            # Use truncation settings for agent input
            input_text = args[1] if len(args) > 1 else "No input"
            truncated_input = settings.truncate_text(
                str(input_text), settings.log_truncate_agent_input
            )
            file_logger.info(f"AGENT_INPUT | {agent_name} | {truncated_input}")

            try:
                # Execute function
                result = await cast(Callable[P, Awaitable[T]], func)(*args, **kwargs)

                # Log output
                output_str = (
                    str(result.final_output)
                    if hasattr(result, "final_output")
                    else str(result)
                )
                console_logger.info(f"✅ {agent_name} completed")

                # Use truncation settings for agent output
                truncated_output = settings.truncate_text(
                    output_str, settings.log_truncate_agent_output
                )
                file_logger.info(
                    f"AGENT_OUTPUT | {agent_name} | SUCCESS | {truncated_output}"
                )

                return result

            except Exception as e:
                # Log error
                console_logger.error(f"❌ {agent_name} failed: {str(e)}")
                file_logger.error(f"AGENT_ERROR | {agent_name} | {str(e)}")
                raise

        @wraps(func)
        def sync_wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            console_logger, file_logger = get_loggers()

            # Log input
            input_msg = (
                f"🤖 {agent_name} INPUT: {args[1] if len(args) > 1 else 'No input'}"
            )
            console_logger.info(f"🤖 {agent_name} starting...")

            # Use truncation settings for agent input
            input_text = args[1] if len(args) > 1 else "No input"
            truncated_input = settings.truncate_text(
                str(input_text), settings.log_truncate_agent_input
            )
            file_logger.info(f"AGENT_INPUT | {agent_name} | {truncated_input}")

            try:
                # Execute function
                result = func(*args, **kwargs)

                # Log output
                output_str = (
                    str(result.final_output)
                    if hasattr(result, "final_output")
                    else str(result)
                )
                console_logger.info(f"✅ {agent_name} completed")

                # Use truncation settings for agent output
                truncated_output = settings.truncate_text(
                    output_str, settings.log_truncate_agent_output
                )
                file_logger.info(
                    f"AGENT_OUTPUT | {agent_name} | SUCCESS | {truncated_output}"
                )

                return result

            except Exception as e:
                # Log error
                console_logger.error(f"❌ {agent_name} failed: {str(e)}")
                file_logger.error(f"AGENT_ERROR | {agent_name} | {str(e)}")
                raise

        # Return appropriate wrapper based on function type
        import inspect

        if inspect.iscoroutinefunction(func):
            return async_wrapper  # type: ignore
        else:
            return sync_wrapper  # type: ignore

    return decorator


def log_tool_interaction(tool_name: str) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """Decorator to log tool inputs and outputs.

    Args:
        tool_name: Name of the tool for logging identification

    Returns:
        Decorated function with input/output logging
    """

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            console_logger, file_logger = get_loggers()

            # Extract context info if available
            context_info = "No context"
            if args and hasattr(args[0], "context"):
                ctx = args[0].context
                if hasattr(ctx, "items"):
                    context_info = f"{len(ctx.items)} items"

            # Log input
            console_logger.info(f"🔧 {tool_name} executing...")

            # Use truncation settings for tool input
            truncated_context = settings.truncate_text(
                context_info, settings.log_truncate_tool_input
            )
            file_logger.info(f"TOOL_INPUT | {tool_name} | Context: {truncated_context}")

            try:
                # Execute function
                result = func(*args, **kwargs)

                # Log output
                output_str = str(result)
                console_logger.info(f"🔧 {tool_name} completed")

                # Use truncation settings for tool output
                truncated_output = settings.truncate_text(
                    output_str, settings.log_truncate_tool_output
                )
                file_logger.info(
                    f"TOOL_OUTPUT | {tool_name} | SUCCESS | {truncated_output}"
                )

                return result

            except Exception as e:
                # Log error
                console_logger.error(f"❌ {tool_name} failed: {str(e)}")
                file_logger.error(f"TOOL_ERROR | {tool_name} | {str(e)}")
                raise

        return wrapper

    return decorator


def log_system_event(event: str, details: str = "") -> None:
    """Log a system-level event.

    Args:
        event: Event name/type
        details: Additional event details
    """
    console_logger, file_logger = get_loggers()
    console_logger.info(f"🔄 {event}")
    file_logger.info(f"SYSTEM_EVENT | {event} | {details}")


def log_session_end() -> None:
    """Log session end marker."""
    console_logger, file_logger = get_loggers()
    file_logger.info("=== LOGISTICS AGENTS SESSION END ===")
    console_logger.info("📝 Session logged successfully")
