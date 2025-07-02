"""Tests for Agent 05 - Inventory Orchestrator.

Team Member: Andy
These tests validate the orchestrator agent and the "Agents as Tools" pattern.
"""

import pytest
from agents import Runner, trace
from ..agent import InventoryOrchestrator


@pytest.mark.agent05
class TestInventoryOrchestrator:
    """Test suite for the Inventory Orchestrator agent."""

    @pytest.fixture
    def agent(self):
        """Create agent instance for testing."""
        return InventoryOrchestrator()

    @pytest.mark.asyncio
    async def test_agent_initialization(self, agent):
        """Test that the orchestrator initializes correctly."""
        assert agent.agent is not None
        assert agent.agent.name == "InventoryOrchestrator"
        # 4 specialist agents + 2 coordination tools
        assert len(agent.agent.tools) >= 6

    @pytest.mark.asyncio
    async def test_agents_as_tools_pattern(self, agent):
        """Test that other agents are properly configured as tools."""
        tools = agent.agent.tools
        tool_names = [getattr(tool, 'name', str(tool)) for tool in tools]

        # Should have specialist agents as tools
        expected_agents = [
            "InventoryThresholdMonitor",
            "RouteComputer",
            "RestockingCalculator",
            "OrderConsolidator"
        ]

        for expected in expected_agents:
            assert any(
                expected in tool_name for tool_name in tool_names), f"Missing {expected} as tool"

    @pytest.mark.asyncio
    @pytest.mark.expensive  # Mark as expensive - uses multiple agents
    async def test_end_to_end_orchestration(self, agent, sample_inventory_context):
        """
        **EXPENSIVE TEST**: Complete end-to-end orchestration using all specialist agents.

        This test validates the entire "Agents as Tools" pattern by having the orchestrator
        coordinate all 4 specialist agents to provide a complete logistics analysis.
        """
        print("\n🚀 Starting End-to-End Orchestration Test...")
        print("⏱️  This test orchestrates 4+ agents and may take 30-60 seconds")
        print("💰 This test will consume OpenAI API credits")
        print("📊 Progress will be shown below:\n")

        # Debug: Check what's in the context
        print(f"📋 Context Debug:")
        print(f"   → Items in context: {len(sample_inventory_context.items)}")
        print(f"   → Suppliers: {len(sample_inventory_context.suppliers)}")
        if sample_inventory_context.items:
            sample_item = sample_inventory_context.items[0]
            print(
                f"   → Sample item: {sample_item.item_id} - Stock: {sample_item.current_stock}")
        print()

        with trace("TestEndToEndOrchestration"):
            print("🎯 Orchestrator: Starting complete logistics analysis...")
            print("   → Will coordinate: Threshold Monitor, Route Computer, Restock Calculator, Order Consolidator")

            result = await Runner.run(
                agent.agent,
                input="Using the provided inventory data, perform complete logistics analysis: identify urgent items, calculate optimal quantities, plan delivery routes, and consolidate orders. Analyze the inventory items in the context.",
                context=sample_inventory_context
            )

            print("✅ Orchestration completed successfully!")

        assert result is not None
        assert result.final_output is not None

        # Validate that the orchestrator actually processed the inventory data
        output = result.final_output.lower()

        # Check that the result contains evidence of actual analysis
        assert len(
            result.final_output) > 100, "Output too short - likely not a proper analysis"

        # The output should NOT ask for more information (previous bug)
        problematic_phrases = [
            "could you provide",
            "i need specific items",
            "provide the names",
            "more information needed"
        ]
        for phrase in problematic_phrases:
            assert phrase not in output, f"Orchestrator asking for more info: '{phrase}' found in output"

        # Should contain evidence of analysis (at least some of these terms)
        analysis_terms = ["inventory", "stock", "threshold",
                          "urgent", "items", "supplier", "analysis"]
        found_terms = [term for term in analysis_terms if term in output]
        assert len(
            found_terms) >= 3, f"Output lacks analysis terms. Found: {found_terms}"

        print(f"\n🎯 End-to-End Orchestration Result:\n{result.final_output}")
        print(
            f"\n✅ Validation: Found {len(found_terms)} analysis terms: {found_terms}")
        print("\n✅ Agent 05 (Orchestrator) - All tests passed! 🎉")


@pytest.mark.agent05
class TestOrchestratorTools:
    """Test suite for orchestrator coordination tools."""

    def test_tools_import_correctly(self):
        """Test that coordination tools can be imported."""
        from ..tools.agent_coordinator import coordinate_workflow_steps
        from ..tools.result_synthesizer import create_executive_summary

        assert coordinate_workflow_steps is not None
        assert create_executive_summary is not None

    def test_tools_are_function_tools(self):
        """Test that tools are properly decorated as function_tools."""
        from ..tools.agent_coordinator import coordinate_workflow_steps
        from ..tools.result_synthesizer import create_executive_summary

        # Function tools are instances of FunctionTool class
        assert hasattr(coordinate_workflow_steps, 'name')
        assert hasattr(coordinate_workflow_steps, 'description')
        assert hasattr(create_executive_summary, 'name')
        assert hasattr(create_executive_summary, 'description')


# Integration test moved to main test class as test_end_to_end_orchestration
# This avoids duplicate expensive tests while still validating the "Agents as Tools" pattern
