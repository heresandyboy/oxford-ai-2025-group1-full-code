"""Order Optimizer Tool - Simplified for Course Learning."""

from agents import function_tool, RunContextWrapper
from ....models.inventory_data import InventoryContext
from ....utils.logging_config import log_tool_interaction


@function_tool
@log_tool_interaction("OrderOptimizer")
def calculate_consolidation_savings(wrapper: RunContextWrapper[InventoryContext]) -> str:
    """Calculate potential savings from order consolidation.

    Focus: Learning @function_tool creation and basic cost optimization.
    """
    context = wrapper.context

    # Get items needing restock
    items_to_restock = [
        item for item in context.items if item.current_stock <= item.order_quantity * 0.2]

    if not items_to_restock:
        return "✅ No items requiring consolidation analysis"

    # Group by supplier for consolidation analysis
    supplier_groups = {}
    for item in items_to_restock:
        supplier_id = item.supplier_id
        if supplier_id not in supplier_groups:
            supplier_groups[supplier_id] = []
        supplier_groups[supplier_id].append(item)

    # Calculate consolidation savings
    savings_analysis = []
    total_savings = 0

    for supplier_id, items in supplier_groups.items():
        if len(items) > 1:  # Only calculate savings if multiple items from same supplier
            # Simple savings model
            # $25 per individual shipment
            individual_shipping_cost = len(items) * 25
            consolidated_shipping_cost = 40  # $40 for consolidated shipment
            shipping_savings = individual_shipping_cost - consolidated_shipping_cost

            # Volume discount (2% on orders over $500)
            total_order_value = sum(
                item.unit_cost * (item.order_quantity - item.current_stock) for item in items)
            volume_discount = total_order_value * 0.02 if total_order_value > 500 else 0

            total_supplier_savings = shipping_savings + volume_discount
            total_savings += total_supplier_savings

            savings_analysis.append(
                f"{supplier_id}: ${total_supplier_savings:.2f} savings "
                f"({len(items)} items, ${total_order_value:.2f} value)"
            )

    if savings_analysis:
        return (f"💰 Consolidation savings analysis:\n" +
                "\n".join(savings_analysis) +
                f"\n\nTotal potential savings: ${total_savings:.2f}")
    else:
        return "📋 No consolidation opportunities (single items per supplier)"
