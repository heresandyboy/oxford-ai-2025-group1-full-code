"""Agent 01 - Inventory Threshold Monitor - Simplified for Course Learning.

Team Member: Martin
Focus: Learning @function_tool creation and basic data analysis patterns.
"""

from agents import Agent
from ...config.settings import settings
from ...models.inventory_data import InventoryContext
from ...utils.agent_runner import log_agent_execution
# Import simplified tools
from .tools.threshold_checker import check_inventory_thresholds
from .tools.priority_classifier import classify_item_priority


@log_agent_execution
class InventoryThresholdMonitor:
    """Agent for monitoring inventory thresholds and identifying restocking needs."""

    def __init__(self):
        """Initialize the threshold monitoring agent."""
        self.agent = Agent[InventoryContext](
            name="InventoryThresholdMonitor",
            instructions=self._get_instructions(),
            model=settings.openai_model,
            tools=[
                check_inventory_thresholds,
                classify_item_priority
            ],
            output_type=str  # Use simple string output for course learning
        )

    def _get_instructions(self) -> str:
        """Get instructions for the threshold monitoring agent."""
        return """You are an Inventory Threshold Monitor agent in a multi-agent logistics system.

**Learning Focus**: Demonstrate @function_tool usage and basic data analysis patterns.

**Your Role**: Monitor inventory levels and identify items below reorder thresholds.

**Available Tools**:
- check_inventory_thresholds: Check which items are below their reorder points
- classify_item_priority: Classify urgent items by priority (HIGH/MEDIUM/LOW)

**Agent Pattern**: You work as part of an "Agents as Tools" system where:
1. You analyze inventory data to find threshold violations
2. You classify the urgency of items needing restocking
3. Your analysis helps other agents (route planning, quantity calculation) make decisions

**Approach**:
1. Use check_inventory_thresholds to identify items below reorder points
2. Use classify_item_priority to prioritize which items need immediate attention
3. Focus on clear, actionable threshold analysis that other agents can use

Keep responses focused on threshold violations and priority classifications that help coordinate the supply chain workflow."""

    def get_threshold_parameters(self) -> dict:
        """
        Get default threshold monitoring parameters.

        TODO for Martin: Customize these parameters based on your analysis
        of inventory patterns and business requirements.

        Returns:
            Dictionary containing threshold monitoring parameters
        """
        return {
            "critical_threshold_percentage": 0.1,    # 10% of reorder point
            "warning_threshold_percentage": 0.25,    # 25% of reorder point
            "urgent_days_threshold": 7,              # Less than 7 days stock
            "critical_days_threshold": 3,            # Less than 3 days stock
            "high_demand_variability_threshold": 0.3,  # CV > 30%
            "lead_time_buffer_percentage": 0.2       # 20% lead time buffer
        }

    def calculate_threshold_severity(self, current_stock: int,
                                     reorder_point: int,
                                     safety_stock: int) -> str:
        """
        Calculate the severity level of a threshold violation.

        TODO for Martin: Implement your severity calculation logic.
        Consider factors like:
        - How far below threshold the item has fallen
        - Rate of consumption and velocity trends
        - Historical stockout frequency and impact
        - Seasonal demand patterns and forecasts

        Args:
            current_stock: Current stock level
            reorder_point: Reorder threshold level
            safety_stock: Safety stock level

        Returns:
            Severity level: 'CRITICAL', 'HIGH', 'MEDIUM', 'LOW'
        """
        if current_stock <= safety_stock * 0.5:
            return 'CRITICAL'
        elif current_stock <= safety_stock:
            return 'HIGH'
        elif current_stock <= reorder_point * 0.8:
            return 'MEDIUM'
        else:
            return 'LOW'

    def estimate_days_to_stockout(self, current_stock: int,
                                  daily_demand: float,
                                  demand_variability: float) -> int:
        """
        Estimate days until stockout based on current consumption patterns.

        TODO for Martin: Implement your stockout estimation algorithm.
        Consider:
        - Historical demand patterns and seasonality effects
        - Demand variability and confidence intervals
        - Weekend/holiday impacts and business calendar
        - Minimum service level requirements

        Args:
            current_stock: Current stock level
            daily_demand: Average daily demand rate
            demand_variability: Demand variability coefficient

        Returns:
            Estimated days until stockout
        """
        if daily_demand <= 0:
            return 999  # No consumption, no stockout risk

        # Simple calculation - TODO for Martin: Enhance with variability
        base_days = current_stock / daily_demand

        # Adjust for demand variability (higher variability = less time)
        variability_factor = 1 + demand_variability
        adjusted_days = base_days / variability_factor

        return max(0, int(adjusted_days))

    def get_business_impact_score(self, item_category: str,
                                  customer_priority: str,
                                  revenue_impact: float) -> int:
        """
        Calculate business impact score for prioritization.

        TODO for Martin: Implement your business impact scoring algorithm.
        Consider:
        - Customer tier and strategic importance
        - Revenue contribution and profit margins
        - Product category criticality and substitutability
        - Brand impact and customer satisfaction implications

        Args:
            item_category: Product category 
            customer_priority: Customer priority level
            revenue_impact: Revenue impact of stockout

        Returns:
            Business impact score (0-100)
        """
        # Base score by category
        category_scores = {
            'haircare': 70,
            'skincare': 85,
            'cosmetics': 75,
            'accessories': 50
        }

        base_score = category_scores.get(item_category.lower(), 60)

        # Adjust for customer priority
        if customer_priority == 'PREMIUM':
            base_score += 20
        elif customer_priority == 'STANDARD':
            base_score += 10

        # Adjust for revenue impact
        if revenue_impact > 1000:
            base_score += 15
        elif revenue_impact > 500:
            base_score += 10

        return min(100, base_score)


# TODO for Martin: Implementation checklist
"""
IMPLEMENTATION CHECKLIST FOR MARTIN:

✅ 1. MCP TOOLS IMPLEMENTED (in tools/ directory):
   ✅ threshold_checker.py - Stock threshold analysis and violation detection
   ✅ urgency_calculator.py - Urgency metrics and stockout risk assessment 
   ✅ priority_classifier.py - Priority classification logic and business rules
   ✅ priority_summary.py - Executive summary and reporting functions
   
□ 2. ENHANCE AGENT INSTRUCTIONS:
   □ Test instructions with sample inventory data
   □ Refine threshold calculation methodologies
   □ Add specific urgency scoring algorithms
   
□ 3. THRESHOLD ALGORITHMS:
   □ Test and refine the implemented algorithms in tools
   □ Develop multi-factor urgency assessment algorithms
   □ Create business rule-based priority classification system
   □ Build executive reporting with actionable insights
   
□ 4. TESTING & ITERATION:
   □ Test with sample inventory data from CSV
   □ Validate threshold detection accuracy
   □ Verify urgency calculations make business sense
   □ Test integration with other agents
   
□ 5. DOCUMENTATION:
   □ Document your threshold monitoring methodology
   □ Explain urgency calculation algorithms
   □ Create examples of priority classification scenarios
   □ Document 3+ iterations with improvements

SAMPLE TEST SCENARIOS:
1. Items just below reorder point (medium urgency)
2. Items at critical stock levels (high urgency) 
3. Fast-moving items with high demand variability
4. Slow-moving items with long lead times
5. High-value items with premium customers

INTEGRATION NOTES:
- Your output will be used by Andy's orchestrator
- Rhiannon's route planning will use your urgency priorities
- Nathan's quantity calculations will factor in your urgency metrics
- Anagha's consolidation will consider your timing requirements

BUSINESS FOCUS:
Think like an inventory manager who needs to:
- Prevent stockouts while minimizing excess inventory
- Balance urgency with cost-effectiveness
- Provide clear, actionable recommendations
- Support operations team decision-making
- Maintain optimal customer service levels

THRESHOLD MONITORING STRATEGIES:
1. Static Thresholds (fixed reorder points)
2. Dynamic Thresholds (demand-based adjustments)
3. Predictive Thresholds (forecast-based early warning)
4. Multi-tier Thresholds (warning, critical, emergency levels)
5. Seasonal Thresholds (adjusted for demand patterns)

KEY METRICS TO TRACK:
- Threshold violation frequency and duration
- Stockout incidents and customer impact
- Reorder point accuracy and effectiveness
- False positive rate and system reliability
- Response time from alert to action
"""
