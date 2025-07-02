"""
Data models package for logistics agents.

This package contains all data models and schemas used throughout the
logistics agents system, including:

- Inventory data models (items, suppliers, orders)
- Analysis result models (threshold monitoring, route computation, etc.)
- Context models for agent communication
- Validation and serialization helpers

The models are designed to work with the CSV data structure and provide
type safety and validation for the entire system.
"""

# Core inventory data models
from .inventory_data import (
    InventoryItem,
    Supplier,
    RestockOrder,
    InventoryContext
)

# Analysis result models
from .analysis_results import (
    ThresholdMonitorResult,
    RouteComputationResult,
    RestockCalculationResult,
    OrderConsolidationResult,
    ComprehensiveSupplyChainAnalysis
)

__all__ = [
    # Inventory data models
    "InventoryItem",
    "Supplier",
    "RestockOrder",
    "InventoryContext",
    # Analysis result models
    "ThresholdMonitorResult",
    "RouteComputationResult",
    "RestockCalculationResult",
    "OrderConsolidationResult",
    "ComprehensiveSupplyChainAnalysis"
]
