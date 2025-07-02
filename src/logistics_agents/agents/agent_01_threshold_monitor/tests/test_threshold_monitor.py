"""Tests for Agent 01 - Inventory Threshold Monitor.

Team Member: Martin
These tests validate the threshold monitoring agent and its simplified tools.
"""

import pytest
from agents import Runner, trace
from ..agent import InventoryThresholdMonitor


@pytest.mark.agent01
class TestInventoryThresholdMonitor:
    """Test suite for the Inventory Threshold Monitor agent."""

    @pytest.fixture
    def agent(self):
        """Create agent instance for testing."""
        return InventoryThresholdMonitor()

    @pytest.mark.asyncio
    async def test_agent_initialization(self, agent):
        """Test that the agent initializes correctly."""
        assert agent.agent is not None
        assert agent.agent.name == "InventoryThresholdMonitor"
        assert len(agent.agent.tools) >= 2  # At least our 2 simplified tools

    @pytest.mark.asyncio
    async def test_agent_with_sample_data(self, agent, sample_inventory_context):
        """Test agent with sample inventory data."""
        with trace("TestThresholdMonitor"):
            result = await Runner.run(
                agent.agent,
                input="Analyze inventory thresholds and identify items needing attention",
                context=sample_inventory_context
            )

        assert result is not None
        assert result.final_output is not None
        # The agent should return string output based on our simplified implementation

    @pytest.mark.asyncio
    async def test_agent_with_urgent_items(self, agent, urgent_items_context):
        """Test agent focusing on urgent items only."""
        with trace("TestUrgentItems"):
            result = await Runner.run(
                agent.agent,
                input="Focus on the most urgent threshold violations",
                context=urgent_items_context
            )

        assert result is not None
        assert result.final_output is not None

    @pytest.mark.skip(reason="Model validation doesn't allow empty items list")
    @pytest.mark.asyncio
    async def test_agent_empty_context(self, agent):
        """Test agent behavior with minimal context."""
        # Skip this test since InventoryContext doesn't allow empty items
        pass


@pytest.mark.agent01
class TestThresholdMonitorTools:
    """Test suite for individual threshold monitor tools."""

    def test_tools_import_correctly(self):
        """Test that all simplified tools can be imported."""
        from ..tools.threshold_checker import check_inventory_thresholds
        from ..tools.priority_classifier import classify_item_priority

        assert check_inventory_thresholds is not None
        assert classify_item_priority is not None

    def test_tools_are_function_tools(self):
        """Test that tools are properly decorated as function_tools."""
        from ..tools.threshold_checker import check_inventory_thresholds
        from ..tools.priority_classifier import classify_item_priority

        # Function tools are instances of FunctionTool class
        assert hasattr(check_inventory_thresholds, 'name')
        assert hasattr(check_inventory_thresholds, 'description')
        assert hasattr(classify_item_priority, 'name')
        assert hasattr(classify_item_priority, 'description')


@pytest.mark.agent01
@pytest.mark.integration
class TestThresholdMonitorIntegration:
    """Integration tests for threshold monitor with other system components."""

    @pytest.mark.asyncio
    async def test_agent_output_structure(self, sample_inventory_context):
        """Test that agent output can be used by other agents."""
        agent = InventoryThresholdMonitor()

        with trace("TestIntegration"):
            result = await Runner.run(
                agent.agent,
                input="Provide threshold analysis for integration with other agents",
                context=sample_inventory_context
            )

        assert result is not None
        # Output should be structured for use by orchestrator
        # Based on our simplified implementation
        assert isinstance(result.final_output, str)
