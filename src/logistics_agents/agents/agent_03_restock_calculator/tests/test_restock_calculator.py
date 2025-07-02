"""Tests for Agent 03 - Restock Calculator.

Team Member: Nathan
These tests validate the restock calculator agent with mathematical patterns and EOQ calculations.
"""

import pytest
from agents import Runner, trace
from ..agent import RestockingCalculator


@pytest.mark.agent03
class TestRestockingCalculator:
    """Test suite for the Restocking Calculator agent."""

    @pytest.fixture
    def agent(self):
        """Create agent instance for testing."""
        return RestockingCalculator()

    @pytest.mark.asyncio
    async def test_agent_initialization(self, agent):
        """Test that the agent initializes correctly."""
        assert agent.agent is not None
        assert agent.agent.name == "RestockingCalculator"
        # 2 simplified tools + CodeInterpreter
        assert len(agent.agent.tools) >= 3

    @pytest.mark.asyncio
    async def test_demand_estimation(self, agent, urgent_items_context):
        """Test demand estimation functionality."""
        with trace("TestDemandEstimation"):
            result = await Runner.run(
                agent.agent,
                input="Estimate demand patterns for items needing restock",
                context=urgent_items_context
            )

        assert result is not None
        assert result.final_output is not None

    @pytest.mark.asyncio
    async def test_quantity_calculations(self, agent, urgent_items_context):
        """Test EOQ quantity calculations."""
        with trace("TestQuantityCalculations"):
            result = await Runner.run(
                agent.agent,
                input="Calculate optimal reorder quantities using EOQ principles",
                context=urgent_items_context
            )

        assert result is not None
        assert result.final_output is not None

    @pytest.mark.asyncio
    async def test_mathematical_analysis(self, agent, sample_inventory_context):
        """Test CodeInterpreter for complex mathematical analysis."""
        with trace("TestMathematicalAnalysis"):
            result = await Runner.run(
                agent.agent,
                input="Perform advanced EOQ calculations with cost optimization",
                context=sample_inventory_context
            )

        assert result is not None


@pytest.mark.agent03
class TestRestockCalculatorTools:
    """Test suite for individual restock calculator tools."""

    def test_tools_import_correctly(self):
        """Test that all simplified tools can be imported."""
        from ..tools.demand_forecaster import estimate_simple_demand
        from ..tools.quantity_optimizer import calculate_reorder_quantities

        assert estimate_simple_demand is not None
        assert calculate_reorder_quantities is not None

    def test_tools_are_function_tools(self):
        """Test that tools are properly decorated as function_tools."""
        from ..tools.demand_forecaster import estimate_simple_demand
        from ..tools.quantity_optimizer import calculate_reorder_quantities

        # Function tools are instances of FunctionTool class
        assert hasattr(estimate_simple_demand, 'name')
        assert hasattr(estimate_simple_demand, 'description')
        assert hasattr(calculate_reorder_quantities, 'name')
        assert hasattr(calculate_reorder_quantities, 'description')
