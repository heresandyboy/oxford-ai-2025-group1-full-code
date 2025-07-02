"""Agent 03 - Restocking Calculator - Calculates optimal reorder quantities.

Team Member: Nathan  
Focus: Learning demand forecasting and quantity optimization patterns.
"""

from agents import Agent, CodeInterpreterTool
from ...config.settings import settings
from ...models.inventory_data import InventoryContext
from ...models.analysis_results import RestockCalculationResult
from ...utils.agent_runner import log_agent_execution
# Import simplified tools
from .tools.demand_forecaster import estimate_simple_demand
from .tools.quantity_optimizer import calculate_reorder_quantities


@log_agent_execution
class RestockingCalculator:
    """Agent for calculating optimal restocking quantities and timing."""

    def __init__(self):
        """Initialize the restocking calculation agent."""
        self.agent = Agent[InventoryContext](
            name="RestockingCalculator",
            instructions=self._get_instructions(),
            model=settings.openai_model,
            tools=[
                estimate_simple_demand,
                calculate_reorder_quantities,
                CodeInterpreterTool(
                    tool_config={"type": "code_interpreter", "container": {"type": "auto"}})
            ],
            output_type=str  # Use simple string output for course learning
        )

    def _get_instructions(self) -> str:
        """Get instructions for the restocking calculation agent."""
        return """You are a Restocking Calculator agent in a multi-agent logistics system.

**Learning Focus**: Demonstrate @function_tool usage and mathematical agent patterns.

**Your Role**: Analyze demand patterns and calculate optimal reorder quantities for items needing restocking.

**Available Tools:**
- estimate_simple_demand: Analyze simple demand patterns for low-stock items
- calculate_reorder_quantities: Calculate reorder quantities using basic EOQ principles
- CodeInterpreterTool: For complex mathematical calculations and analysis

**Agent Pattern**: You work as part of an "Agents as Tools" system where:
1. You receive inventory data and threshold alerts from other agents
2. You analyze demand patterns and calculate optimal restock quantities
3. Your calculations help the orchestrator make restocking decisions

**Approach:**
1. Use estimate_simple_demand to analyze consumption patterns for urgent items
2. Use calculate_reorder_quantities to determine optimal order quantities and costs
3. Use CodeInterpreter for any advanced mathematical analysis (EOQ, cost optimization, etc.)
4. Focus on practical, cost-effective restocking recommendations

Keep responses focused on quantitative analysis and recommendations that other agents can use for decision-making."""
