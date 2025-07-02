"""Agent 04 - Order Consolidator - Optimizes supplier grouping and order consolidation.

Team Member: Anagha
Focus: Learning supplier matching and order optimization patterns.
"""

from agents import Agent, WebSearchTool
from ...config.settings import settings
from ...models.inventory_data import InventoryContext
from ...utils.agent_runner import log_agent_execution
# Import simplified tools
from .tools.supplier_matcher import group_orders_by_supplier
from .tools.order_optimizer import calculate_consolidation_savings


@log_agent_execution
class OrderConsolidator:
    """Agent for consolidating orders and optimizing supplier groupings."""

    def __init__(self):
        """Initialize the order consolidation agent."""
        self.agent = Agent[InventoryContext](
            name="OrderConsolidator",
            instructions=self._get_instructions(),
            model=settings.openai_model,
            tools=[
                group_orders_by_supplier,
                calculate_consolidation_savings,
                WebSearchTool()  # For supplier information gathering
            ],
            output_type=str  # Use simple string output for course learning
        )

    def _get_instructions(self) -> str:
        """Get instructions for the order consolidation agent."""
        return """You are an Order Consolidator agent in a multi-agent logistics system.

**Learning Focus**: Demonstrate @function_tool usage and information gathering patterns.

**Your Role**: Group orders by supplier and calculate consolidation savings for efficient ordering.

**Available Tools:**
- WebSearchTool: Research supplier information, current shipping rates, and market conditions
- group_orders_by_supplier: Group items needing restock by supplier for consolidation opportunities
- calculate_consolidation_savings: Calculate potential cost savings from order consolidation

**Agent Pattern**: You work as part of an "Agents as Tools" system where:
1. You receive restock recommendations from other agents
2. You group orders by supplier to identify consolidation opportunities
3. Your analysis helps the orchestrator optimize ordering decisions

**Approach:**
1. Use group_orders_by_supplier to identify which items can be ordered together
2. Use calculate_consolidation_savings to quantify financial benefits
3. Use WebSearchTool to research current supplier capabilities or shipping rates when needed
4. Focus on practical consolidation opportunities that reduce costs

Keep responses focused on consolidation opportunities and cost savings that other agents can use for decision-making."""
