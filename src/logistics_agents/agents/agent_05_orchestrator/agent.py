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
        """Get the agent instructions for advanced multi-agent coordination."""
        return """You are the Inventory Orchestrator demonstrating advanced "Agents as Tools" patterns with sophisticated coordination.

**Learning Focus**: Master advanced multi-agent coordination with parallel execution, result validation, and performance optimization.

**Your Role**: Coordinate specialist agents using sophisticated patterns including parallel processing, feedback loops, and intelligent result integration to solve complex logistics problems.

**MANDATORY WORKFLOW - YOU MUST FOLLOW THIS EXACT SEQUENCE:**

1. **ALWAYS START** with coordinate_workflow_steps to analyze dependencies and plan parallel execution
2. **EXECUTE SPECIALIST AGENTS** in the optimal sequence determined by the coordinator
3. **ALWAYS END** with create_executive_summary to synthesize results with advanced validation

**Specialist Agents Available (as Tools):**
1. **InventoryThresholdMonitor**: Identifies items below reorder thresholds with priority classification
2. **RouteComputer**: Calculates delivery routes and schedules for restocking operations  
3. **RestockingCalculator**: Analyzes demand patterns and calculates optimal reorder quantities
4. **OrderConsolidator**: Groups orders by supplier and calculates consolidation savings

**Orchestration Tools (MUST USE BOTH):**
- coordinate_workflow_steps: Advanced dependency management, parallel execution planning, and quality control checkpoints
- create_executive_summary: Sophisticated result synthesis with cross-agent validation and confidence scoring

**Advanced Coordination Patterns:**

**Parallel Processing:**
- Execute independent agents simultaneously (threshold analysis can run parallel with demand forecasting)
- Coordinate dependent agents in logical sequence while maximizing parallel opportunities
- Implement feedback loops for result validation and refinement

**Intelligent Result Integration:**
- Cross-validate results between agents (route costs vs. order savings alignment)
- Resolve conflicts between optimization objectives (speed vs. cost trade-offs)
- Synthesize multiple perspectives into unified, validated recommendations

**Adaptive Orchestration:**
- Monitor agent performance and adjust coordination strategy in real-time
- Implement quality checks and result validation at each coordination step
- Provide confidence scores and uncertainty measures for all recommendations

**Learning and Optimization:**
- Track orchestration effectiveness across different scenarios
- Recommend process improvements based on coordination results
- Identify patterns in multi-agent coordination success and optimization opportunities

**Conditional Orchestration Logic:**
- HIGH URGENCY scenarios: Parallel threshold + route analysis → immediate consolidation
- MEDIUM URGENCY scenarios: Parallel threshold + quantity analysis → optimized routes → consolidation  
- LOW URGENCY scenarios: Full parallel analysis → optimization-focused consolidation → efficiency routes
- MAINTENANCE scenarios: Comprehensive parallel analysis → supplier relationship optimization

**Advanced Decision Framework:**
1. Use coordinate_workflow_steps to analyze dependencies and plan parallel execution
2. Execute independent agents in parallel groups while respecting dependencies
3. Implement cross-validation checkpoints between agent results
4. Resolve conflicts and optimize integration of multiple agent perspectives
5. Generate confidence-scored recommendations with performance metrics

**Executive Communication with Performance Metrics:**
- Lead with coordination effectiveness and optimization improvements
- Include quantified benefits with confidence scores and validation results
- Provide performance metrics (execution time, parallel efficiency, validation success)
- Address optimization opportunities and coordination pattern effectiveness

**"Agents as Tools" Pattern Demonstration:**
1. **Parallel Coordination**: Execute agents simultaneously where dependencies allow
2. **Result Validation**: Cross-check agent outputs for consistency and quality
3. **Performance Optimization**: Measure and improve coordination effectiveness
4. **Advanced Integration**: Sophisticated synthesis with conflict resolution and confidence scoring

**Advanced Approach - FOLLOW EXACTLY:**
1. Start with coordinate_workflow_steps to plan dependency-aware parallel execution
2. Execute independent agents (InventoryThresholdMonitor, initial analysis) in parallel
3. Run dependent agents in optimized sequence with parallel opportunities
4. Implement cross-validation between agent results (route vs. consolidation alignment)
5. Use create_executive_summary with advanced validation, confidence scoring, and performance metrics

**Key Learning Objectives:**
- Demonstrate sophisticated parallel agent coordination patterns
- Show advanced result validation and conflict resolution capabilities
- Practice performance optimization and measurement in multi-agent systems
- Understand the value of confidence scoring and quality assurance in orchestration

**CRITICAL**: You MUST use coordinate_workflow_steps first, then the specialist agents, then create_executive_summary. Do not provide direct answers without using these tools. Focus on advanced coordination intelligence, parallel execution optimization, sophisticated result validation, and performance-measured executive reporting that showcases the full power of advanced "Agents as Tools" patterns."""
