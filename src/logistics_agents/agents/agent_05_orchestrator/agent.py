"""Agent 05 - Inventory Orchestrator - Coordinates all logistics agents using "Agents as Tools" pattern.

Team Member: Andy
Focus: Learning orchestration patterns and multi-agent coordination.
"""

from agents import Agent
from ...config.settings import settings
from ...models.inventory_data import InventoryContext
from ...utils.agent_runner import log_agent_execution
# Import all specialist agents for orchestration
from ..agent_01_threshold_monitor.agent import InventoryThresholdMonitor
from ..agent_02_route_computer.agent import RouteComputer
from ..agent_03_restock_calculator.agent import RestockingCalculator
from ..agent_04_order_consolidator.agent import OrderConsolidator
# Import orchestrator tools
from .tools.agent_coordinator import coordinate_workflow_steps
from .tools.result_synthesizer import create_executive_summary


@log_agent_execution
class InventoryOrchestrator:
    """Orchestrator agent that coordinates all logistics agents using Agents as Tools pattern."""

    def __init__(self):
        """Initialize the orchestrator and all specialist agents."""
        # Initialize specialist agents for orchestration
        self.threshold_monitor = InventoryThresholdMonitor()
        self.route_computer = RouteComputer()
        self.restock_calculator = RestockingCalculator()
        self.order_consolidator = OrderConsolidator()

        # Create the orchestrator agent
        self.agent = Agent[InventoryContext](
            name="InventoryOrchestrator",
            instructions=self._get_instructions(),
            model=settings.openai_model,
            tools=[
                coordinate_workflow_steps,
                create_executive_summary,
                # Add specialist agents as tools (Agents as Tools Pattern)
                self.threshold_monitor.agent.as_tool(
                    tool_name="InventoryThresholdMonitor",
                    tool_description="Monitor inventory thresholds and identify items below reorder points with priority classification"
                ),
                self.route_computer.agent.as_tool(
                    tool_name="RouteComputer",
                    tool_description="Compute optimal delivery routes for restocking operations with time and cost optimization"
                ),
                self.restock_calculator.agent.as_tool(
                    tool_name="RestockingCalculator",
                    tool_description="Calculate optimal restocking quantities using EOQ, demand forecasting, and inventory optimization"
                ),
                self.order_consolidator.agent.as_tool(
                    tool_name="OrderConsolidator",
                    tool_description="Consolidate orders and optimize shipping efficiency for maximum cost savings"
                ),
            ],
            output_type=str  # Use simple string output for course learning
        )

    def _get_instructions(self) -> str:
        """Get agent instructions for the orchestrator."""
        return """You are the Inventory Orchestrator demonstrating the "Agents as Tools" pattern.

**Learning Focus**: Master multi-agent coordination and result synthesis patterns.

**Your Role**: Coordinate specialist agents to solve complex logistics problems that no single agent can handle alone.

**Specialist Agents Available (as Tools):**
1. **InventoryThresholdMonitor**: Identifies items below reorder thresholds with priority classification
2. **RouteComputer**: Calculates delivery routes and schedules for restocking operations  
3. **RestockingCalculator**: Analyzes demand patterns and calculates optimal reorder quantities
4. **OrderConsolidator**: Groups orders by supplier and calculates consolidation savings

**Orchestration Tools:**
- coordinate_workflow_steps: Plan the logical sequence of agent coordination
- create_executive_summary: Synthesize results from multiple agents into actionable insights

**"Agents as Tools" Pattern Demonstration:**
1. **Sequential Coordination**: Use agents in logical order (threshold → quantity → routes → consolidation)
2. **Result Integration**: Each agent's output becomes input for the next agent's analysis
3. **Synthesis**: Combine all specialist results into comprehensive recommendations

**Approach:**
1. Start with coordinate_workflow_steps to plan your orchestration strategy
2. Use InventoryThresholdMonitor to identify urgent items requiring attention
3. Use RestockingCalculator to determine optimal quantities for flagged items
4. Use RouteComputer to plan efficient delivery routes for restocking
5. Use OrderConsolidator to identify consolidation opportunities and cost savings
6. Use create_executive_summary to synthesize all results into actionable recommendations

**Key Learning Objectives:**
- Demonstrate how complex problems require multiple specialized agents
- Show how agents can be composed as tools within larger workflows
- Practice result synthesis and executive-level reporting
- Understand the value of agent orchestration vs. single-agent approaches

Focus on clear coordination logic and result synthesis that showcases the power of the "Agents as Tools" pattern."""
