"""Delivery Scheduler Tool - Simplified for Course Learning."""

from agents import function_tool, RunContextWrapper
from ....models.inventory_data import InventoryContext
from ....utils.logging_config import log_tool_interaction
from datetime import datetime, timedelta


@function_tool
@log_tool_interaction("DeliveryScheduler")
def create_delivery_schedule(wrapper: RunContextWrapper[InventoryContext]) -> str:
    """Create simple delivery schedule for urgent items.

    Focus: Learning @function_tool patterns and basic scheduling logic.
    """
    context = wrapper.context
    schedules = []

    # Get urgent items (below 20% threshold)
    urgent_items = [
        item for item in context.items if item.current_stock <= item.order_quantity * 0.2][:5]

    base_date = datetime.now()

    for i, item in enumerate(urgent_items):
        # Simple scheduling: next day + index days for different urgency
        delivery_date = base_date + timedelta(days=i+1)

        # Simple priority based on stock percentage
        stock_percentage = (item.current_stock / item.order_quantity) * 100
        priority = "HIGH" if stock_percentage < 10 else "MEDIUM"

        schedules.append(
            f"{delivery_date.strftime('%Y-%m-%d')}: {item.item_id} "
            f"({item.supplier_id} → {item.customer_location}) - {priority} priority"
        )

    if schedules:
        return f"📅 Delivery schedule created:\n" + "\n".join(schedules)
    else:
        return "✅ No urgent deliveries needed"
