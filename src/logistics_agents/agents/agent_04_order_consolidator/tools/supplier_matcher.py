"""Supplier Matcher Tool - Simplified for Course Learning."""

from agents import function_tool, RunContextWrapper
from ....models.inventory_data import InventoryContext
from ....utils.logging_config import log_tool_interaction


@function_tool
@log_tool_interaction("SupplierMatcher")
def group_orders_by_supplier(wrapper: RunContextWrapper[InventoryContext]) -> str:
    """Group items needing restock by supplier for consolidation opportunities.

    Focus: Learning @function_tool creation and basic grouping logic.
    """
    context = wrapper.context
    supplier_groups = {}

    # Get items that need restocking
    items_to_restock = [
        item for item in context.items if item.current_stock <= item.order_quantity * 0.2]

    # Group by supplier
    for item in items_to_restock:
        supplier_id = item.supplier_id
        if supplier_id not in supplier_groups:
            supplier_groups[supplier_id] = {
                'items': [],
                'total_cost': 0,
                'locations': set()
            }

        reorder_quantity = item.order_quantity - item.current_stock
        item_cost = reorder_quantity * item.unit_cost

        supplier_groups[supplier_id]['items'].append({
            'item_id': item.item_id,
            'quantity': reorder_quantity,
            'cost': item_cost
        })
        supplier_groups[supplier_id]['total_cost'] += item_cost
        supplier_groups[supplier_id]['locations'].add(item.location)

    # Format results
    consolidation_summary = []
    for supplier_id, group in supplier_groups.items():
        item_count = len(group['items'])
        total_cost = group['total_cost']
        location_count = len(group['locations'])

        consolidation_summary.append(
            f"{supplier_id}: {item_count} items, ${total_cost:.2f} total, {location_count} locations"
        )

    if consolidation_summary:
        return f"🏢 Order consolidation by supplier:\n" + "\n".join(consolidation_summary)
    else:
        return "✅ No orders requiring consolidation"
