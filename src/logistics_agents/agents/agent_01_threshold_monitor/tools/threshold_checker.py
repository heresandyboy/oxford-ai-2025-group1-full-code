"""Threshold Checker Tool - Simple threshold checking for learning agent patterns.

Single Responsibility: Basic threshold violation detection.
Team Member: Martin
"""

from agents import function_tool, RunContextWrapper
from ....models.inventory_data import InventoryContext
from ....utils.logging_config import log_tool_interaction


@function_tool
@log_tool_interaction("ThresholdChecker")
def check_inventory_thresholds(wrapper: RunContextWrapper[InventoryContext]) -> str:
    """
    Check which inventory items are below their reorder thresholds.

    Simple implementation focusing on agent pattern learning rather than
    complex business logic.
    """
    context = wrapper.context

    items_below = []
    total_items = len(context.items)

    for item in context.items:
        if item.is_below_threshold:
            items_below.append({
                "item_id": item.item_id,
                "current_stock": item.current_stock,
                "threshold": item.reorder_threshold,
                "category": item.category
            })

    if items_below:
        summary = f"⚠️ THRESHOLD VIOLATIONS FOUND:\n"
        summary += f"📊 {len(items_below)} of {total_items} items below threshold\n\n"

        for item in items_below[:5]:  # Show first 5 for simplicity
            summary += f"• {item['item_id']}: {item['current_stock']} units "
            summary += f"(threshold: {item['threshold']}) - {item['category']}\n"

        if len(items_below) > 5:
            summary += f"... and {len(items_below) - 5} more items\n"

        summary += f"\n💡 Recommendation: Prioritize restocking for these items"
        return summary
    else:
        return f"✅ All {total_items} items are above their reorder thresholds"
