"""Result Synthesizer Tool - Simplified for Course Learning."""

from agents import function_tool, RunContextWrapper
from ....models.inventory_data import InventoryContext
from ....utils.logging_config import log_tool_interaction


@function_tool
@log_tool_interaction("ResultSynthesizer")
def create_executive_summary(wrapper: RunContextWrapper[InventoryContext]) -> str:
    """Create executive summary of multi-agent analysis results.

    Focus: Learning result synthesis and reporting patterns.
    """
    context = wrapper.context

    # Simple analysis for demonstration
    total_items = len(context.items)
    low_stock_items = [
        item for item in context.items if item.current_stock <= item.order_quantity * 0.2]
    critical_items = [
        item for item in low_stock_items if item.current_stock <= item.order_quantity * 0.1]

    # Basic cost estimation
    total_restock_cost = sum(
        (item.order_quantity - item.current_stock) * item.unit_cost
        for item in low_stock_items
    )

    # Group by supplier for consolidation insight
    suppliers = set(item.supplier_id for item in low_stock_items)

    executive_summary = f"""
📊 EXECUTIVE SUMMARY - Multi-Agent Logistics Analysis

🎯 SITUATION OVERVIEW:
• Total inventory items analyzed: {total_items}
• Items requiring restock: {len(low_stock_items)}
• Critical items (urgent): {len(critical_items)}
• Suppliers involved: {len(suppliers)}

💰 FINANCIAL IMPACT:
• Estimated restock cost: ${total_restock_cost:.2f}
• Potential consolidation opportunities: {len(suppliers)} supplier groups

🚀 RECOMMENDED ACTIONS:
1. Immediate restock for {len(critical_items)} critical items
2. Plan consolidated orders with {len(suppliers)} suppliers  
3. Optimize delivery routes for cost efficiency
4. Monitor {total_items - len(low_stock_items)} stable items

This summary demonstrates how an orchestrator synthesizes results from multiple specialist agents.
"""

    return executive_summary.strip()
