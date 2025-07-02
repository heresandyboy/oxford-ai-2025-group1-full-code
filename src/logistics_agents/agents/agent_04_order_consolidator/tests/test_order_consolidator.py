"""Tests for Agent 04 - Order Consolidator.

Team Member: Anagha
These tests validate the order consolidator agent with information gathering patterns and WebSearchTool.
"""

import pytest
from agents import Runner, trace
from ..agent import OrderConsolidator


@pytest.mark.agent04
class TestOrderConsolidator:
    """Test suite for the Order Consolidator agent."""

    @pytest.fixture
    def agent(self):
        """Create agent instance for testing."""
        return OrderConsolidator()

    @pytest.mark.asyncio
    async def test_agent_initialization(self, agent):
        """Test that the agent initializes correctly."""
        assert agent.agent is not None
        assert agent.agent.name == "OrderConsolidator"
        # 2 simplified tools + WebSearchTool
        assert len(agent.agent.tools) >= 3

    @pytest.mark.asyncio
    async def test_supplier_grouping(self, agent, urgent_items_context):
        """Test order grouping by supplier."""
        with trace("TestSupplierGrouping"):
            result = await Runner.run(
                agent.agent,
                input="Group orders by supplier for consolidation opportunities",
                context=urgent_items_context
            )

        assert result is not None
        assert result.final_output is not None

    @pytest.mark.asyncio
    async def test_consolidation_savings(self, agent, urgent_items_context):
        """Test consolidation savings calculations."""
        with trace("TestConsolidationSavings"):
            result = await Runner.run(
                agent.agent,
                input="Calculate potential savings from order consolidation",
                context=urgent_items_context
            )

        assert result is not None
        assert result.final_output is not None

    @pytest.mark.asyncio
    async def test_information_gathering(self, agent, sample_inventory_context):
        """Test WebSearchTool integration for supplier information (mock test)."""
        with trace("TestInformationGathering"):
            result = await Runner.run(
                agent.agent,
                input="Analyze supplier consolidation opportunities and market conditions",
                context=sample_inventory_context
            )

        assert result is not None
        # Note: This may require API keys for WebSearch, so we test basic functionality


@pytest.mark.agent04
class TestOrderConsolidatorTools:
    """Test suite for individual order consolidator tools."""

    def test_tools_import_correctly(self):
        """Test that all simplified tools can be imported."""
        from ..tools.supplier_matcher import group_orders_by_supplier
        from ..tools.order_optimizer import calculate_consolidation_savings

        assert group_orders_by_supplier is not None
        assert calculate_consolidation_savings is not None

    def test_tools_are_function_tools(self):
        """Test that tools are properly decorated as function_tools."""
        from ..tools.supplier_matcher import group_orders_by_supplier
        from ..tools.order_optimizer import calculate_consolidation_savings

        # Function tools are instances of FunctionTool class
        assert hasattr(group_orders_by_supplier, 'name')
        assert hasattr(group_orders_by_supplier, 'description')
        assert hasattr(calculate_consolidation_savings, 'name')
        assert hasattr(calculate_consolidation_savings, 'description')
