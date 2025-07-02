"""Demand Forecaster Tool - Simplified for Course Learning."""

from agents import function_tool, RunContextWrapper
from ....models.inventory_data import InventoryContext
from ....utils.logging_config import log_tool_interaction


@function_tool
@log_tool_interaction("DemandForecaster")
def estimate_simple_demand(wrapper: RunContextWrapper[InventoryContext]) -> str:
    """Estimate simple demand patterns for restocking decisions.

    Focus: Learning @function_tool creation and basic demand analysis.
    """
    context = wrapper.context
    demand_analysis = []

    # Get items below threshold for demand estimation
    low_stock_items = [
        item for item in context.items if item.current_stock <= item.order_quantity * 0.2][:5]

    for item in low_stock_items:
        # Simple demand estimation based on current stock patterns
        consumption_rate = (item.order_quantity -
                            item.current_stock) / item.order_quantity

        if consumption_rate > 0.8:
            demand_level = "HIGH"
        elif consumption_rate > 0.5:
            demand_level = "MEDIUM"
        else:
            demand_level = "LOW"

        estimated_monthly_demand = int(
            item.order_quantity * consumption_rate * 1.2)  # 20% buffer

        demand_analysis.append(
            f"{item.item_id}: {demand_level} demand (~{estimated_monthly_demand} units/month)"
        )

    if demand_analysis:
        return f"📊 Demand estimation for {len(demand_analysis)} items:\n" + "\n".join(demand_analysis)
    else:
        return "✅ No high-demand items requiring immediate analysis"
