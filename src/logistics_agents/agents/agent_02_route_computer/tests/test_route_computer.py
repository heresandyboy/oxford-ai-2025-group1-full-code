"""Tests for Agent 02 - Route Computer.

Team Member: Rhiannon
These tests validate the route computer agent and its simplified tools with CodeInterpreter.
"""

import pytest
from agents import Runner, trace
from ..agent import RouteComputer


@pytest.mark.agent02
class TestRouteComputer:
    """Test suite for the Route Computer agent."""

    @pytest.fixture
    def agent(self):
        """Create agent instance for testing."""
        return RouteComputer()

    @pytest.mark.asyncio
    async def test_agent_initialization(self, agent):
        """Test that the agent initializes correctly."""
        assert agent.agent is not None
        assert agent.agent.name == "RouteComputer"
        # 2 simplified tools + CodeInterpreter
        assert len(agent.agent.tools) >= 3

    @pytest.mark.asyncio
    async def test_route_calculation(self, agent, urgent_items_context):
        """Test route calculation with urgent items."""
        with trace("TestRouteCalculation"):
            result = await Runner.run(
                agent.agent,
                input="Calculate delivery routes for items needing restocking",
                context=urgent_items_context
            )

        assert result is not None
        assert result.final_output is not None

    @pytest.mark.asyncio
    async def test_delivery_scheduling(self, agent, urgent_items_context):
        """Test delivery scheduling functionality."""
        with trace("TestDeliveryScheduling"):
            result = await Runner.run(
                agent.agent,
                input="Create delivery schedule for urgent inventory items",
                context=urgent_items_context
            )

        assert result is not None
        assert result.final_output is not None

    @pytest.mark.asyncio
    async def test_mathematical_calculations(self, agent, sample_inventory_context):
        """Test CodeInterpreter integration for mathematical operations."""
        with trace("TestMathCalculations"):
            result = await Runner.run(
                agent.agent,
                input="Calculate total distances and delivery costs for all routes",
                context=sample_inventory_context
            )

        assert result is not None


@pytest.mark.agent02
class TestRouteComputerTools:
    """Test suite for individual route computer tools."""

    def test_tools_import_correctly(self):
        """Test that all simplified tools can be imported."""
        from ..tools.route_calculator import calculate_simple_routes
        from ..tools.delivery_scheduler import create_delivery_schedule

        assert calculate_simple_routes is not None
        assert create_delivery_schedule is not None

    def test_tools_are_function_tools(self):
        """Test that tools are properly decorated as function_tools."""
        from ..tools.route_calculator import calculate_simple_routes
        from ..tools.delivery_scheduler import create_delivery_schedule

        # Function tools are instances of FunctionTool class
        assert hasattr(calculate_simple_routes, 'name')
        assert hasattr(calculate_simple_routes, 'description')
        assert hasattr(create_delivery_schedule, 'name')
        assert hasattr(create_delivery_schedule, 'description')
