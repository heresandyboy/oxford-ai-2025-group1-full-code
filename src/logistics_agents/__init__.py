"""
Supply Chain Inventory Management Multi-Agent System

Oxford AI Summit 2025 - Agents as Tools Pattern Implementation

This package implements a multi-agent system for optimizing supply chain
inventory management through intelligent threshold monitoring, route computation,
restocking calculations, order consolidation, and coordinated orchestration.

Team Agent Assignments:
- Agent 01 (Martin): Inventory Threshold Monitor
- Agent 02 (Rhiannon): Route Computer  
- Agent 03 (Nathan): Restocking Calculator
- Agent 04 (Anagha): Order Consolidation
- Agent 05 (Andy): Orchestrator
"""

__version__ = "0.1.0"
__author__ = "Team Logistics - Oxford AI Summit 2025"

# Package exports
from .main import main

__all__ = ["main"]
