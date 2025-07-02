"""Agents package for logistics inventory management system.

This package contains all the specialized agents for supply chain optimization:
- Agent 01: Inventory Threshold Monitor (Martin)
- Agent 02: Route Computer (Rhiannon) 
- Agent 03: Restocking Calculator (Nathan)
- Agent 04: Order Consolidator (Anagha)
- Agent 05: Orchestrator (Andy)

Each agent has specialized MCP tools and follows the single responsibility principle.
"""

# Import all agents for easy access
from .agent_01_threshold_monitor.agent import InventoryThresholdMonitor
from .agent_02_route_computer.agent import RouteComputer
from .agent_03_restock_calculator.agent import RestockingCalculator
from .agent_04_order_consolidator.agent import OrderConsolidator
from .agent_05_orchestrator.agent import InventoryOrchestrator

__all__ = [
    "InventoryThresholdMonitor",
    "RouteComputer",
    "RestockingCalculator",
    "OrderConsolidator",
    "InventoryOrchestrator",
]
