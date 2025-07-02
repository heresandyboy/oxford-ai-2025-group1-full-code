"""Agent 03 Restocking Calculator Tools Package - Simplified for Course Learning."""

from .demand_forecaster import estimate_simple_demand
from .quantity_optimizer import calculate_reorder_quantities

__all__ = [
    "estimate_simple_demand",
    "calculate_reorder_quantities"
]
