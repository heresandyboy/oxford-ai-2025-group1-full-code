"""Agent Coordinator Tool - Simplified for Course Learning."""

from agents import RunContextWrapper, function_tool

from ....models.inventory_data import InventoryContext
from ....utils.logging_config import log_tool_interaction


@function_tool
@log_tool_interaction("AgentCoordinator")
def coordinate_workflow_steps(wrapper: RunContextWrapper[InventoryContext]) -> str:
    """Coordinate the logical workflow steps for multi-agent analysis with urgency-based strategy selection.

    Focus: Learning orchestration patterns, workflow coordination, and conditional logic.
    """
    context = wrapper.context
    total_items = len(context.items)

    # Advanced urgency analysis
    critical_items = len(
        [
            item
            for item in context.items
            if item.current_stock <= item.order_quantity * 0.1
        ]
    )
    urgent_items = len(
        [
            item
            for item in context.items
            if item.current_stock <= item.order_quantity * 0.3
        ]
    )
    low_stock_items = len(
        [
            item
            for item in context.items
            if item.current_stock <= item.order_quantity * 0.5
        ]
    )

    # Determine workflow strategy based on urgency
    if critical_items > total_items * 0.1:  # More than 10% critical
        workflow_type = "🚨 URGENT RESPONSE"
        sequence = ["threshold", "routes", "consolidation"]
        priority = "Speed over optimization"
        rationale = f"With {critical_items} critical items ({critical_items/total_items*100:.1f}%), immediate action required"
    elif urgent_items > total_items * 0.3:  # More than 30% urgent
        workflow_type = "⚡ BALANCED APPROACH"
        sequence = ["threshold", "quantity", "routes", "consolidation"]
        priority = "Balance speed and cost"
        rationale = f"With {urgent_items} urgent items ({urgent_items/total_items*100:.1f}%), balanced approach optimal"
    else:
        workflow_type = "💰 COST OPTIMIZATION"
        sequence = ["threshold", "quantity", "consolidation", "routes"]
        priority = "Cost optimization focus"
        rationale = f"With {low_stock_items} low-stock items ({low_stock_items/total_items*100:.1f}%), cost optimization prioritized"

    # Enhanced workflow steps with conditional logic
    workflow_steps = [
        "1. THRESHOLD CHECK: Identify items below reorder thresholds with urgency classification",
        "2. URGENCY ANALYSIS: Assess business impact and risk levels",
        "3. STRATEGY SELECTION: Choose optimal workflow sequence based on urgency",
        "4. AGENT COORDINATION: Execute specialists in optimal order",
        "5. RESULT INTEGRATION: Synthesize outputs with business context",
        "6. EXECUTIVE SYNTHESIS: Create strategic recommendations with risk assessment",
    ]

    # Risk assessment
    financial_exposure = sum(
        item.unit_cost * item.order_quantity
        for item in context.items
        if item.current_stock <= item.order_quantity * 0.2
    )

    risks = []
    if critical_items > 0:
        risks.append(f"Stockout risk for {critical_items} critical items")
    if financial_exposure > 10000:
        risks.append(f"High financial exposure: ${financial_exposure:,.2f}")
    if urgent_items > total_items * 0.4:
        risks.append("Supply chain stress indicators detected")

    status_summary = (
        f"📋 ENHANCED ORCHESTRATION STRATEGY for {total_items} total items:\n\n"
        + f"🎯 STRATEGY SELECTED: {workflow_type}\n"
        + f"📊 URGENCY ANALYSIS:\n"
        + f"  • Critical items: {critical_items} ({critical_items/total_items*100:.1f}%)\n"
        + f"  • Urgent items: {urgent_items} ({urgent_items/total_items*100:.1f}%)\n"
        + f"  • Low stock items: {low_stock_items} ({low_stock_items/total_items*100:.1f}%)\n\n"
        + f"🔄 WORKFLOW SEQUENCE: {' → '.join(sequence)}\n"
        + f"⭐ PRIORITY: {priority}\n"
        + f"💡 RATIONALE: {rationale}\n\n"
        + "📋 ORCHESTRATION STEPS:\n"
        + "\n".join(workflow_steps)
        + (
            f"\n\n⚠️ RISK FACTORS:\n" + "\n".join(f"  • {risk}" for risk in risks)
            if risks
            else "\n\n✅ LOW RISK SCENARIO"
        )
    )

    return status_summary
