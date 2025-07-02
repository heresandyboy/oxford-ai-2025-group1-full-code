"""Main application logic."""

import asyncio
import logging
from datetime import datetime
from pathlib import Path

from agents import Runner, trace

from .config.settings import settings
from .models.inventory_data import InventoryContext
from .utils.logging_config import setup_logging, log_system_event, log_session_end
from .utils.agent_runner import LoggedAgentRunner
from .utils.data_loader import load_sample_inventory_context


async def run_inventory_analysis(context: InventoryContext) -> None:
    """Run comprehensive inventory management analysis."""
    console_logger, file_logger = setup_logging()

    log_system_event("ANALYSIS_START",
                     f"Items: {len(context.items)}, Region: {context.region}")

    # Import orchestrator only when needed to avoid circular imports
    from .agents.agent_05_orchestrator.agent import InventoryOrchestrator

    orchestrator = InventoryOrchestrator()

    with trace("InventoryAnalysis"):
        # Use logged agent runner for comprehensive tracking
        result = await LoggedAgentRunner.run_agent(
            agent=orchestrator.agent,
            input_message="Analyze the inventory management operations and provide comprehensive restocking recommendations.",
            context=context,
            agent_name="InventoryOrchestrator"
        )

        console_logger.info("📊 Analysis Results:")
        console_logger.info(result.final_output)
        file_logger.info(f"ANALYSIS_RESULT | {result.final_output}")

    log_system_event("ANALYSIS_COMPLETE",
                     "Full orchestration finished successfully")


def main() -> None:
    """Main entry point."""
    console_logger, file_logger = setup_logging()

    log_system_event("APPLICATION_START", f"Model: {settings.openai_model}")

    try:
        # Load actual inventory data from CSV
        console_logger.info("Loading inventory data from CSV...")
        log_system_event("DATA_LOADING", "Starting CSV data load")

        context = load_sample_inventory_context()

        console_logger.info(
            f"Loaded {len(context.items)} items, {len(context.items_below_threshold)} below threshold")
        log_system_event(
            "DATA_LOADED", f"Items: {len(context.items)}, Below threshold: {len(context.items_below_threshold)}")

    except Exception as e:
        console_logger.error(f"Failed to load inventory data: {e}")
        file_logger.error(f"DATA_LOAD_ERROR | {str(e)}")
        console_logger.info("Creating minimal fallback context")

        # Fallback to minimal context if data loading fails
        context = InventoryContext(
            items=[],
            suppliers=[],
            analysis_date=datetime.now(),
            region="UK",
            total_locations=1
        )
        log_system_event(
            "DATA_FALLBACK", "Using minimal context due to load failure")

    try:
        asyncio.run(run_inventory_analysis(context))
    except Exception as e:
        console_logger.error(f"Analysis failed: {e}")
        file_logger.error(f"ANALYSIS_ERROR | {str(e)}")
        raise
    finally:
        log_session_end()


if __name__ == "__main__":
    main()
