"""Quantity Optimizer Tool - Simplified for Course Learning."""

import math
from agents import function_tool, RunContextWrapper
from ....models.inventory_data import InventoryContext
from ....utils.logging_config import log_tool_interaction


@function_tool
@log_tool_interaction("QuantityOptimizer")
def calculate_reorder_quantities(wrapper: RunContextWrapper[InventoryContext]) -> str:
    """Calculate simple reorder quantities for low-stock items.

    Focus: Learning @function_tool creation and basic EOQ concepts.
    """
    context = wrapper.context
    reorder_recommendations = []

    # Get items needing restock
    items_to_restock = [
        item for item in context.items if item.current_stock <= item.order_quantity * 0.2][:5]

    for item in items_to_restock:
        # Simple EOQ-inspired calculation
        annual_demand = item.order_quantity * 12  # Assume monthly order quantity
        holding_cost_per_unit = item.unit_cost * 0.25  # 25% holding cost
        ordering_cost = 50  # Simplified ordering cost

        # Basic EOQ formula: sqrt(2 * annual_demand * ordering_cost / holding_cost_per_unit)
        if holding_cost_per_unit > 0:
            eoq = int(math.sqrt(2 * annual_demand *
                      ordering_cost / holding_cost_per_unit))
            # Ensure minimum practical order
            recommended_quantity = max(
                eoq, item.order_quantity - item.current_stock)
        else:
            recommended_quantity = item.order_quantity - item.current_stock

        total_cost = recommended_quantity * item.unit_cost

        reorder_recommendations.append(
            f"{item.item_id}: Order {recommended_quantity} units (${total_cost:.2f}) - Current: {item.current_stock}"
        )

    if reorder_recommendations:
        return f"📦 Reorder quantity recommendations:\n" + "\n".join(reorder_recommendations)
    else:
        return "✅ No items requiring restock calculations"
