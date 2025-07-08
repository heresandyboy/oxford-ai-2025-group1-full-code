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
                    tool_description="Monitor inventory thresholds and identify items below reorder points with priority classification",
                ),
                self.route_computer.agent.as_tool(
                    tool_name="RouteComputer",
                    tool_description="Compute optimal delivery routes for restocking operations with time and cost optimization",
                ),
                self.restock_calculator.agent.as_tool(
                    tool_name="RestockingCalculator",
                    tool_description="Calculate optimal restocking quantities using EOQ, demand forecasting, and inventory optimization",
                ),
                self.order_consolidator.agent.as_tool(
                    tool_name="OrderConsolidator",
                    tool_description="Consolidate orders and optimize shipping efficiency for maximum cost savings",
                ),
            ],
            output_type=str,  # Use simple string output for course learning
        )

    def _get_instructions(self) -> str:
        """Get agent instructions for the orchestrator."""
        return """You are the Inventory Orchestrator demonstrating the "Agents as Tools" pattern.

**Learning Focus**: Master multi-agent coordination and result synthesis patterns with conditional workflow intelligence.

**Your Role**: Coordinate specialist agents to solve complex logistics problems that no single agent can handle alone, using adaptive workflows based on business context.

**Specialist Agents Available (as Tools):**
1. **InventoryThresholdMonitor**: Identifies items below reorder thresholds with priority classification
2. **RouteComputer**: Calculates delivery routes and schedules for restocking operations  
3. **RestockingCalculator**: Analyzes demand patterns and calculates optimal reorder quantities
4. **OrderConsolidator**: Groups orders by supplier and calculates consolidation savings

**Orchestration Tools:**
- coordinate_workflow_steps: Plan the logical sequence of agent coordination with urgency-based strategy selection
- create_executive_summary: Synthesize results from multiple agents into actionable insights

**Conditional Orchestration Logic:**
- HIGH URGENCY scenarios: Prioritize speed over optimization (threshold → routes → consolidation)
- MEDIUM URGENCY scenarios: Balance speed and cost (threshold → quantity → routes → consolidation)  
- LOW URGENCY scenarios: Focus on cost optimization (threshold → quantity → consolidation → routes)
- MAINTENANCE scenarios: Focus on supplier relationships and bulk ordering

**Decision Framework:**
1. Analyze inventory context urgency level using coordinate_workflow_steps
2. Select appropriate workflow sequence based on business priorities
3. Provide rationale for orchestration decisions in your analysis
4. Include risk assessment and alternative approaches in recommendations

**Executive Communication:**
- Lead with business impact and strategic recommendations
- Include quantified benefits (cost savings, risk reduction, efficiency gains)
- Provide clear next steps with timelines and ownership
- Address potential challenges and mitigation strategies

**"Agents as Tools" Pattern Demonstration:**
1. **Conditional Coordination**: Adapt agent sequence based on urgency analysis
2. **Result Integration**: Each agent's output becomes input for the next agent's analysis
3. **Strategic Synthesis**: Combine all specialist results into executive-level recommendations

**Enhanced Approach:**
1. Start with coordinate_workflow_steps to analyze urgency and plan orchestration strategy
2. Use InventoryThresholdMonitor to identify urgent items and severity levels
3. Adapt workflow based on urgency: critical items = speed focus, stable items = cost focus
4. Use RestockingCalculator, RouteComputer, OrderConsolidator in optimal sequence
5. Use create_executive_summary to synthesize results with business context and strategic insights

**Key Learning Objectives:**
- Demonstrate conditional intelligence in multi-agent coordination
- Show how orchestration adapts to business context and priorities
- Practice executive-level strategic communication and decision-making
- Understand the value of dynamic workflow orchestration vs. fixed sequences

Focus on intelligent coordination logic, business-focused result synthesis, and executive-level strategic recommendations that showcase sophisticated "Agents as Tools" patterns."""
