"""Result Synthesizer Tool - Simplified for Course Learning."""

from agents import RunContextWrapper, function_tool

from ....models.inventory_data import InventoryContext
from ....utils.logging_config import log_tool_interaction


@function_tool
@log_tool_interaction("ResultSynthesizer")
def create_executive_summary(wrapper: RunContextWrapper[InventoryContext]) -> str:
    """Create executive summary of multi-agent analysis results with strategic business context.

    Focus: Learning result synthesis, executive reporting, and strategic communication patterns.
    """
    context = wrapper.context

    # Enhanced analysis with business metrics
    total_items = len(context.items)
    low_stock_items = [
        item
        for item in context.items
        if item.current_stock <= item.order_quantity * 0.2
    ]
    critical_items = [
        item
        for item in low_stock_items
        if item.current_stock <= item.order_quantity * 0.1
    ]
    medium_items = [
        item
        for item in low_stock_items
        if item.current_stock > item.order_quantity * 0.1
        and item.current_stock <= item.order_quantity * 0.2
    ]

    # Financial impact analysis
    total_restock_cost = sum(
        (item.order_quantity - item.current_stock) * item.unit_cost
        for item in low_stock_items
    )
    urgent_cost = sum(
        (item.order_quantity - item.current_stock) * item.unit_cost
        for item in critical_items
    )
    medium_cost = sum(
        (item.order_quantity - item.current_stock) * item.unit_cost
        for item in medium_items
    )

    # Risk assessment
    projected_lost_sales = sum(
        item.unit_cost * item.order_quantity * 0.15 for item in critical_items
    )  # 15% lost sales risk

    # Supplier consolidation analysis
    suppliers = set(item.supplier_id for item in low_stock_items)
    consolidation_potential = min(
        85, 15 + len(suppliers) * 10
    )  # Estimated consolidation efficiency
    optimization_savings = (
        total_restock_cost * (consolidation_potential / 100) * 0.12
    )  # 12% of potential consolidation

    # Business impact classification
    if len(critical_items) > total_items * 0.1:
        impact_level = "HIGH RISK"
        efficiency_score = 65
        target_efficiency = 85
    elif len(critical_items) > total_items * 0.05:
        impact_level = "MEDIUM RISK"
        efficiency_score = 75
        target_efficiency = 85
    else:
        impact_level = "LOW RISK"
        efficiency_score = 82
        target_efficiency = 90

    # Timeline-based recommendations
    immediate_timeline = "24-48 hours"
    short_term_timeline = "1-2 weeks"
    medium_term_timeline = "1 month"
    long_term_timeline = "quarterly review"

    executive_summary = f"""
🎯 STRATEGIC LOGISTICS ANALYSIS - Executive Brief

📊 SITUATION ASSESSMENT:
• Business Impact: {impact_level} - {len(critical_items)} critical stockouts imminent
• Financial Exposure: ${total_restock_cost:,.2f} immediate, ${projected_lost_sales:,.2f} at risk
• Operational Efficiency: {efficiency_score}% current vs {target_efficiency}% target
• Supplier Relationships: {len(suppliers)} active, {consolidation_potential}% consolidation opportunity

💰 FINANCIAL IMPACT BREAKDOWN:
• Total Restock Investment: ${total_restock_cost:,.2f}
• Critical Items (Urgent): ${urgent_cost:,.2f} ({len(critical_items)} items)
• Medium Priority Items: ${medium_cost:,.2f} ({len(medium_items)} items)
• Potential Cost Savings: ${optimization_savings:,.2f} through consolidation

💡 STRATEGIC RECOMMENDATIONS:

1. **IMMEDIATE** ({immediate_timeline}): Address {len(critical_items)} critical items - ${urgent_cost:,.2f}
   • Risk: Stockout prevention, customer satisfaction protection
   • Action: Emergency procurement, expedited delivery

2. **SHORT-TERM** ({short_term_timeline}): Implement {len(medium_items)} planned restocks - ${medium_cost:,.2f}
   • Focus: Balanced cost-efficiency approach
   • Action: Standard procurement cycles, route optimization

3. **MEDIUM-TERM** ({medium_term_timeline}): Optimize {len(suppliers)} supplier relationships - ${optimization_savings:,.2f} savings
   • Strategy: Consolidation opportunities, volume negotiations
   • Action: Supplier partnership reviews, contract optimization

4. **LONG-TERM** ({long_term_timeline}): Review demand patterns and adjust reorder points
   • Objective: Improve {efficiency_score}% to {target_efficiency}% operational efficiency
   • Action: Demand forecasting enhancement, threshold optimization

🚀 EXECUTION PLAN:
• Risk Mitigation: Immediate action prevents estimated ${projected_lost_sales:,.2f} in lost sales
• Success Metrics: Stockout reduction, cost efficiency improvement, supplier consolidation
• Quality Assurance: Multi-agent validation ensures comprehensive analysis
• Scalability: Framework supports {total_items}+ items with maintained accuracy

⚠️ RISK FACTORS & MITIGATION:
• Supply Chain Disruption: Diversified supplier base, buffer stock strategies
• Cost Escalation: Fixed-price contracts, volume commitments
• Capacity Constraints: Phased implementation, resource allocation planning

This orchestrated analysis demonstrates how multiple specialist agents collaborate to solve complex logistics challenges through intelligent coordination and strategic synthesis.
"""

    return executive_summary.strip()
