"""Analysis result data models for all logistics agents."""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Any, Union

from pydantic import BaseModel, Field, ConfigDict


@dataclass
class ThresholdMonitorResult:
    """
    Results from Agent 01 - Inventory Threshold Monitor (Martin).

    Contains analysis of inventory levels and identification of items
    requiring restocking based on threshold violations.

    Attributes:
        items_below_threshold: List of SKUs that are below reorder thresholds
        critical_items: List of SKUs with critically low stock levels
        priority_classifications: Mapping of item_id to priority level (HIGH/MEDIUM/LOW)
        reorder_urgency: Mapping of item_id to estimated days until stockout
        recommendations: List of actionable business recommendations
        summary: Executive summary of threshold analysis findings
        analysis_metadata: Additional metadata about the analysis
    """

    items_below_threshold: List[str]
    critical_items: List[str]
    priority_classifications: Dict[str, str]  # item_id -> priority
    reorder_urgency: Dict[str, int]  # item_id -> days until stockout
    recommendations: List[str]
    summary: str
    analysis_metadata: Dict[str, Any] = None

    def __post_init__(self):
        """Initialize metadata if not provided."""
        if self.analysis_metadata is None:
            self.analysis_metadata = {
                "total_analyzed": len(self.priority_classifications),
                "below_threshold_count": len(self.items_below_threshold),
                "critical_count": len(self.critical_items),
                "analysis_timestamp": datetime.now().isoformat()
            }

    @property
    def urgent_action_required(self) -> bool:
        """Check if any urgent actions are required."""
        return len(self.critical_items) > 0

    @property
    def high_priority_items(self) -> List[str]:
        """Get list of high priority items."""
        return [item_id for item_id, priority in self.priority_classifications.items()
                if priority == "HIGH"]


@dataclass
class RouteComputationResult:
    """
    Results from Agent 02 - Route Computer (Rhiannon).

    Contains optimal routing analysis for delivery and restocking operations.

    Attributes:
        optimal_routes: Mapping of route_id to list of locations in optimal order
        delivery_schedules: Mapping of route_id to delivery schedule information
        efficiency_metrics: Mapping of route_id to efficiency score (0-100)
        cost_estimates: Mapping of route_id to estimated transportation costs
        consolidation_opportunities: Routes that can be consolidated for savings
        recommendations: List of actionable routing recommendations
        summary: Executive summary of route optimization findings
    """

    optimal_routes: Dict[str, List[str]]  # route_id -> [locations]
    delivery_schedules: Dict[str, str]    # route_id -> schedule description
    # route_id -> efficiency_score (0-100)
    efficiency_metrics: Dict[str, float]
    cost_estimates: Dict[str, float]      # route_id -> estimated_cost
    # route_id -> [consolidatable_routes]
    consolidation_opportunities: Dict[str, List[str]] = None
    recommendations: List[str] = None
    summary: str = ""

    def __post_init__(self):
        """Initialize optional fields."""
        if self.consolidation_opportunities is None:
            self.consolidation_opportunities = {}
        if self.recommendations is None:
            self.recommendations = []

    @property
    def total_estimated_cost(self) -> float:
        """Calculate total estimated transportation costs."""
        return sum(self.cost_estimates.values())

    @property
    def average_efficiency(self) -> float:
        """Calculate average route efficiency."""
        if not self.efficiency_metrics:
            return 0.0
        return sum(self.efficiency_metrics.values()) / len(self.efficiency_metrics)

    @property
    def most_efficient_route(self) -> Optional[str]:
        """Get the most efficient route ID."""
        if not self.efficiency_metrics:
            return None
        return max(self.efficiency_metrics.keys(), key=lambda k: self.efficiency_metrics[k])


@dataclass
class RestockCalculationResult:
    """
    Results from Agent 03 - Restocking Calculator (Nathan).

    Contains optimal quantity calculations and demand forecasting analysis.

    Attributes:
        recommended_orders: Mapping of item_id to recommended order quantity
        quantity_optimizations: Detailed optimization data for each item
        demand_forecasts: Demand prediction data for each item
        cost_estimates: Estimated costs for recommended orders
        abc_classifications: ABC analysis classification for each item
        recommendations: List of actionable inventory management recommendations
        summary: Executive summary of restocking analysis
    """

    # item_id -> recommended_quantity
    recommended_orders: Dict[str, int]
    # item_id -> optimization_details
    quantity_optimizations: Dict[str, Dict[str, Any]]
    demand_forecasts: Dict[str, Dict[str, Any]]  # item_id -> forecast_data
    # item_id -> estimated_order_cost
    cost_estimates: Dict[str, float]
    abc_classifications: Dict[str, str]          # item_id -> ABC_class
    recommendations: List[str] = None
    summary: str = ""

    def __post_init__(self):
        """Initialize optional fields."""
        if self.recommendations is None:
            self.recommendations = []

    @property
    def total_order_value(self) -> float:
        """Calculate total value of all recommended orders."""
        return sum(self.cost_estimates.values())

    @property
    def items_requiring_orders(self) -> List[str]:
        """Get list of items that require orders (quantity > 0)."""
        return [item_id for item_id, qty in self.recommended_orders.items() if qty > 0]

    @property
    def high_value_items(self) -> List[str]:
        """Get list of high-value items (A classification)."""
        return [item_id for item_id, classification in self.abc_classifications.items()
                if classification == "A"]


@dataclass
class OrderConsolidationResult:
    """
    Results from Agent 04 - Order Consolidation (Anagha).

    Contains order consolidation opportunities and supplier optimization analysis.

    Attributes:
        consolidation_opportunities: Available consolidation groups and their details
        supplier_optimizations: Supplier-specific optimization recommendations
        estimated_savings: Projected cost savings from consolidation
        consolidation_schedule: Timing and coordination for consolidated orders
        coordination_requirements: Requirements for implementing consolidation
        recommendations: List of actionable consolidation recommendations
        summary: Executive summary of consolidation analysis
    """

    # consolidation_type -> opportunity_details
    consolidation_opportunities: Dict[str, Any]
    # supplier_id -> optimization_data
    supplier_optimizations: Dict[str, Dict[str, Any]]
    estimated_savings: Dict[str, float]          # savings_type -> amount
    consolidation_schedule: Dict[str, Any]       # schedule_info
    coordination_requirements: List[str] = None
    recommendations: List[str] = None
    summary: str = ""

    def __post_init__(self):
        """Initialize optional fields."""
        if self.coordination_requirements is None:
            self.coordination_requirements = []
        if self.recommendations is None:
            self.recommendations = []

    @property
    def total_estimated_savings(self) -> float:
        """Calculate total estimated savings from all consolidation opportunities."""
        return sum(self.estimated_savings.values())

    @property
    def high_impact_consolidations(self) -> Dict[str, Any]:
        """Get consolidation opportunities with savings > $500."""
        return {
            cons_type: details for cons_type, details in self.consolidation_opportunities.items()
            if self.estimated_savings.get(cons_type, 0) > 500
        }

    @property
    def preferred_suppliers(self) -> List[str]:
        """Get list of suppliers recommended for preferred status."""
        return [
            supplier_id for supplier_id, opt_data in self.supplier_optimizations.items()
            if opt_data.get("strategy") == "PREFERRED_SUPPLIER"
        ]


class ComprehensiveSupplyChainAnalysis(BaseModel):
    """
    Combined results from Agent 05 - Orchestrator (Andy).

    This is the final output that synthesizes all individual agent analyses
    into a comprehensive supply chain optimization plan.

    Attributes:
        threshold_analysis: Results from threshold monitoring
        route_computation: Results from route optimization
        restock_calculation: Results from quantity calculations
        order_consolidation: Results from consolidation analysis
        agent_contributions: Summary of each agent's key contributions
        priority_actions: Ranked list of recommended actions
        estimated_annual_savings: Total projected annual savings
        implementation_timeline: Phased implementation plan
        risk_assessment: Identified risks and mitigation strategies
        success_metrics: KPIs for measuring implementation success
        executive_summary: High-level business summary
        next_steps: Specific actions for immediate implementation
    """

    # Individual agent results
    threshold_analysis: Optional[ThresholdMonitorResult] = None
    route_computation: Optional[RouteComputationResult] = None
    restock_calculation: Optional[RestockCalculationResult] = None
    order_consolidation: Optional[OrderConsolidationResult] = None

    # Synthesized analysis
    agent_contributions: Dict[str, str] = Field(
        default_factory=dict,
        description="Summary of each agent's key contributions"
    )
    priority_actions: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Ranked list of recommended actions with priorities and timelines"
    )
    estimated_annual_savings: float = Field(
        default=0.0,
        description="Total projected annual cost savings"
    )
    implementation_timeline: Dict[str, List[str]] = Field(
        default_factory=dict,
        description="Phased implementation plan with timelines"
    )
    risk_assessment: Dict[str, Any] = Field(
        default_factory=dict,
        description="Identified risks and mitigation strategies"
    )
    success_metrics: List[str] = Field(
        default_factory=list,
        description="KPIs for measuring implementation success"
    )
    executive_summary: str = Field(
        default="",
        description="High-level business summary of findings and recommendations"
    )
    next_steps: List[str] = Field(
        default_factory=list,
        description="Specific actions for immediate implementation"
    )

    # Metadata
    analysis_timestamp: datetime = Field(
        default_factory=datetime.now,
        description="When this comprehensive analysis was completed"
    )
    total_items_analyzed: int = Field(
        default=0,
        description="Total number of inventory items analyzed"
    )

    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )

    @property
    def urgent_actions(self) -> List[Dict[str, Any]]:
        """Get list of urgent actions (HIGH priority)."""
        return [action for action in self.priority_actions
                if action.get("priority") == "HIGH"]

    @property
    def total_potential_savings(self) -> float:
        """Calculate total potential savings from all sources."""
        savings = self.estimated_annual_savings

        # Add savings from consolidation if available
        if self.order_consolidation:
            savings += self.order_consolidation.total_estimated_savings

        return savings

    @property
    def implementation_complexity(self) -> str:
        """Assess overall implementation complexity."""
        action_count = len(self.priority_actions)
        urgent_count = len(self.urgent_actions)

        if urgent_count > 5 or action_count > 20:
            return "HIGH"
        elif urgent_count > 2 or action_count > 10:
            return "MEDIUM"
        else:
            return "LOW"

    @property
    def roi_projection(self) -> Optional[float]:
        """Calculate rough ROI projection if cost data is available."""
        if self.restock_calculation and self.total_potential_savings > 0:
            total_investment = self.restock_calculation.total_order_value
            if total_investment > 0:
                return (self.total_potential_savings / total_investment) * 100
        return None

    def get_agent_summary(self) -> Dict[str, Dict[str, Any]]:
        """
        Get summary of all agent results.

        Returns:
            Dictionary with summary statistics from each agent
        """
        summary = {}

        if self.threshold_analysis:
            summary["threshold_monitor"] = {
                "items_below_threshold": len(self.threshold_analysis.items_below_threshold),
                "critical_items": len(self.threshold_analysis.critical_items),
                "urgent_action_required": self.threshold_analysis.urgent_action_required
            }

        if self.route_computation:
            summary["route_computer"] = {
                "total_routes": len(self.route_computation.optimal_routes),
                "average_efficiency": self.route_computation.average_efficiency,
                "total_cost": self.route_computation.total_estimated_cost
            }

        if self.restock_calculation:
            summary["restock_calculator"] = {
                "items_requiring_orders": len(self.restock_calculation.items_requiring_orders),
                "total_order_value": self.restock_calculation.total_order_value,
                "high_value_items": len(self.restock_calculation.high_value_items)
            }

        if self.order_consolidation:
            summary["order_consolidation"] = {
                "total_savings": self.order_consolidation.total_estimated_savings,
                "consolidation_opportunities": len(self.order_consolidation.consolidation_opportunities),
                "preferred_suppliers": len(self.order_consolidation.preferred_suppliers)
            }

        return summary


# Additional helper models for complex data structures

@dataclass
class ActionItem:
    """
    Represents a specific action item in the implementation plan.

    Attributes:
        action_id: Unique identifier for the action
        description: Detailed description of the action
        priority: Priority level (HIGH, MEDIUM, LOW)
        timeline: Expected timeline for completion
        responsible_party: Who should execute this action
        dependencies: Other actions this depends on
        success_criteria: How to measure success
        estimated_impact: Expected business impact
    """

    action_id: str
    description: str
    priority: str
    timeline: str
    responsible_party: str
    dependencies: List[str] = None
    success_criteria: List[str] = None
    estimated_impact: str = ""

    def __post_init__(self):
        """Initialize optional fields."""
        if self.dependencies is None:
            self.dependencies = []
        if self.success_criteria is None:
            self.success_criteria = []


@dataclass
class RiskAssessment:
    """
    Represents a risk assessment for the supply chain optimization plan.

    Attributes:
        risk_id: Unique identifier for the risk
        description: Description of the risk
        probability: Probability of occurrence (LOW, MEDIUM, HIGH)
        impact: Potential impact if risk occurs (LOW, MEDIUM, HIGH)
        mitigation_strategies: List of mitigation approaches
        contingency_plans: Backup plans if risk materializes
    """

    risk_id: str
    description: str
    probability: str  # LOW, MEDIUM, HIGH
    impact: str       # LOW, MEDIUM, HIGH
    mitigation_strategies: List[str]
    contingency_plans: List[str] = None

    def __post_init__(self):
        """Initialize optional fields."""
        if self.contingency_plans is None:
            self.contingency_plans = []

    @property
    def risk_level(self) -> str:
        """Calculate overall risk level based on probability and impact."""
        risk_matrix = {
            ("LOW", "LOW"): "LOW",
            ("LOW", "MEDIUM"): "LOW",
            ("LOW", "HIGH"): "MEDIUM",
            ("MEDIUM", "LOW"): "LOW",
            ("MEDIUM", "MEDIUM"): "MEDIUM",
            ("MEDIUM", "HIGH"): "HIGH",
            ("HIGH", "LOW"): "MEDIUM",
            ("HIGH", "MEDIUM"): "HIGH",
            ("HIGH", "HIGH"): "HIGH"
        }
        return risk_matrix.get((self.probability, self.impact), "MEDIUM")
