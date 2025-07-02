"""Priority Classifier Tool - Simple priority classification for learning agent patterns.

Single Responsibility: Item priority classification based on urgency.
Team Member: Martin
"""

from agents import function_tool, RunContextWrapper
from ....models.inventory_data import InventoryContext
from ....utils.logging_config import log_tool_interaction


@function_tool
@log_tool_interaction("PriorityClassifier")
def classify_item_priority(wrapper: RunContextWrapper[InventoryContext]) -> str:
    """
    Classify items by priority level based on urgency and business factors.

    Simple implementation focusing on agent pattern learning rather than
    complex business logic.
    """
    context = wrapper.context

    # Group items by priority levels
    high_priority = []
    medium_priority = []
    low_priority = []

    for item in context.items:
        if item.is_below_threshold:
            # Simple priority logic based on stock levels
            stock_ratio = item.current_stock / max(item.reorder_threshold, 1)

            if stock_ratio < 0.3:  # Very low stock
                high_priority.append(item)
            elif stock_ratio < 0.6:  # Moderately low stock
                medium_priority.append(item)
            else:  # Just below threshold
                low_priority.append(item)

    # Build priority summary
    summary = f"🎯 PRIORITY CLASSIFICATION:\n"
    summary += f"🔴 HIGH Priority: {len(high_priority)} items (urgent restocking)\n"
    summary += f"🟡 MEDIUM Priority: {len(medium_priority)} items (plan restocking)\n"
    summary += f"🟢 LOW Priority: {len(low_priority)} items (monitor closely)\n\n"

    # Show examples of high priority items
    if high_priority:
        summary += "🔴 High Priority Items:\n"
        for item in high_priority[:3]:  # Show first 3
            summary += f"• {item.item_id}: {item.current_stock} units ({item.category})\n"
        if len(high_priority) > 3:
            summary += f"... and {len(high_priority) - 3} more high priority items\n"

    summary += "\n💡 Recommendation: Focus immediate attention on HIGH priority items"
    return summary
