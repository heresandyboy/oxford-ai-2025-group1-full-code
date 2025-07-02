"""Agent 04 Order Consolidator Tools Package - Simplified for Course Learning."""

from .supplier_matcher import group_orders_by_supplier
from .order_optimizer import calculate_consolidation_savings

__all__ = [
    "group_orders_by_supplier",
    "calculate_consolidation_savings"
]
