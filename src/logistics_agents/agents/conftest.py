"""Shared pytest configuration for all agents.

This file provides common fixtures and utilities for testing all logistics agents.
"""

from src.logistics_agents.models.inventory_data import InventoryContext
from src.logistics_agents.utils.data_loader import load_sample_inventory_context
import pytest
import asyncio
from pathlib import Path
import sys

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def sample_inventory_context() -> InventoryContext:
    """Provide sample inventory context for testing."""
    return load_sample_inventory_context()


@pytest.fixture
def urgent_items_context(sample_inventory_context):
    """Provide context with only urgent items for focused testing."""
    context = sample_inventory_context
    # Filter to only items below threshold for testing
    urgent_items = [
        item for item in context.items if item.current_stock <= item.order_quantity * 0.2][:5]

    # Create a new context with only urgent items for focused testing
    return InventoryContext(
        items=urgent_items,
        suppliers=context.suppliers,
        region=context.region,
        analysis_date=context.analysis_date
    )


@pytest.fixture
def sample_test_data():
    """Provide simple test data for unit testing."""
    return {
        "test_items": 5,
        "test_suppliers": ["SUP001", "SUP002", "SUP003"],
        "test_locations": ["Chennai", "Bangalore", "Mumbai"],
        "threshold_percentage": 0.2
    }
