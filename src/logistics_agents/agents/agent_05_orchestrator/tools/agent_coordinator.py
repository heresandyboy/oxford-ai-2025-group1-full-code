"""Agent Coordinator Tool - Simplified for Course Learning."""

from agents import function_tool, RunContextWrapper
from ....models.inventory_data import InventoryContext
from ....utils.logging_config import log_tool_interaction


@function_tool
@log_tool_interaction("AgentCoordinator")
def coordinate_workflow_steps(wrapper: RunContextWrapper[InventoryContext]) -> str:
    """Coordinate the logical workflow steps for multi-agent analysis.

    Focus: Learning orchestration patterns and workflow coordination.
    """
    context = wrapper.context

    # Define logical workflow steps for logistics analysis
    workflow_steps = [
        "1. THRESHOLD CHECK: Identify items below reorder thresholds",
        "2. DEMAND ANALYSIS: Estimate demand patterns for flagged items",
        "3. QUANTITY CALC: Calculate optimal reorder quantities",
        "4. ROUTE PLANNING: Plan delivery routes for restocking",
        "5. CONSOLIDATION: Group orders by supplier for efficiency",
        "6. COST ANALYSIS: Calculate total costs and potential savings"
    ]

    # Simple status based on data
    items_needing_attention = [
        item for item in context.items if item.current_stock <= item.order_quantity * 0.2]

    status_summary = (
        f"📋 Orchestration Workflow for {len(context.items)} total items:\n" +
        "\n".join(workflow_steps) +
        f"\n\n🎯 Current Status: {len(items_needing_attention)} items need immediate attention"
    )

    return status_summary
