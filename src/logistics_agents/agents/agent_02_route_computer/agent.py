"""Agent 02 - Route Computer - Calculates optimal delivery routes.

Team Member: Rhiannon
Focus: Learning route calculation and delivery scheduling patterns.
"""

from agents import Agent, CodeInterpreterTool
from ...config.settings import settings
from ...models.inventory_data import InventoryContext
from ...models.analysis_results import RouteComputationResult
from ...utils.agent_runner import log_agent_execution
# Import simplified tools
from .tools.route_calculator import calculate_simple_routes
from .tools.delivery_scheduler import create_delivery_schedule


@log_agent_execution
class RouteComputer:
    """Agent for computing optimal delivery routes and scheduling."""

    def __init__(self):
        """Initialize the route computation agent."""
        self.agent = Agent[InventoryContext](
            name="RouteComputer",
            instructions=self._get_instructions(),
            model=settings.openai_model,
            tools=[
                calculate_simple_routes,
                create_delivery_schedule,
                CodeInterpreterTool(
                    tool_config={"type": "code_interpreter", "container": {"type": "auto"}})
            ],
            output_type=str  # Use simple string output for course learning
        )

    def _get_instructions(self) -> str:
        """Get instructions for the route computation agent."""
        return """You are a Route Computer agent in a multi-agent logistics system. 

**Learning Focus**: Demonstrate @function_tool usage and agent coordination patterns.

**Your Role**: Calculate delivery routes and schedules for items that need restocking.

**Available Tools:**
- calculate_simple_routes: Calculate basic delivery routes between suppliers and customers
- create_delivery_schedule: Create simple delivery schedules for urgent items  
- CodeInterpreterTool: For mathematical calculations (distances, costs, route optimization, etc.)

**Agent Pattern**: You work as part of an "Agents as Tools" system where:
1. You receive inventory data from the threshold monitor
2. You calculate routes and schedules for items needing restocking
3. Your results help the orchestrator coordinate the overall logistics workflow

**Approach:**
1. Use calculate_simple_routes to identify delivery paths for urgent items
2. Use create_delivery_schedule to prioritize deliveries by urgency
3. Use CodeInterpreter for any mathematical analysis needed (route optimization, cost calculations, etc.)
4. Focus on clear, actionable routing recommendations

Keep responses focused on route and schedule information that other agents can use."""
