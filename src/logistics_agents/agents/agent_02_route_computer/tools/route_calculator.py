"""Route Calculator Tool - Simplified for Course Learning."""

from agents import function_tool, RunContextWrapper
from ....models.inventory_data import InventoryContext
from ....utils.logging_config import log_tool_interaction


@function_tool
@log_tool_interaction("RouteCalculator")
def calculate_simple_routes(wrapper: RunContextWrapper[InventoryContext]) -> str:
    """Calculate simple delivery routes between suppliers and customers.

    Focus: Learning @function_tool creation and basic route logic.
    """
    context = wrapper.context
    routes = []

    # Get first 5 items that need restocking for simplicity
    items_needing_restock = [
        item for item in context.items if item.current_stock <= item.order_quantity * 0.2][:5]

    for item in items_needing_restock:
        # Simple distance estimation for Indian cities
        estimated_distance = _estimate_city_distance(
            item.location, item.customer_location)
        routes.append(
            f"{item.supplier_id} → {item.customer_location}: ~{estimated_distance}km ({item.item_id})")

    if routes:
        return f"🚛 Calculated {len(routes)} delivery routes:\n" + "\n".join(routes)
    else:
        return "✅ No routes needed - all items sufficiently stocked"


def _estimate_city_distance(city1: str, city2: str) -> int:
    """Simple city distance estimation for demonstration."""
    # Basic distance approximation between major Indian cities
    distances = {
        ("Chennai", "Bangalore"): 350,
        ("Mumbai", "Pune"): 150,
        ("Delhi", "Gurgaon"): 30,
        ("Hyderabad", "Bangalore"): 570,
        ("Chennai", "Hyderabad"): 630
    }

    # Simple bidirectional lookup
    key = (city1, city2)
    reverse_key = (city2, city1)

    return distances.get(key, distances.get(reverse_key, 250))  # Default 250km
