# Agent 04 - Order Consolidator

**Team Member**: Anagha  
**Purpose**: Group orders by supplier and optimize consolidation for cost savings

## 📁 What's in This Folder

- `agent.py` - Your main agent (groups orders, calculates savings)
- `tools/` - Your function tools:
  - `supplier_matcher.py` - Groups items needing restock by supplier
  - `order_optimizer.py` - Calculates consolidation cost savings
- `tests/` - Test your agent quickly with `python -m pytest -m agent04`

## 🎯 What Your Agent Does

**Your agent analyzes restocking needs and:**

1. **Groups orders by supplier** - Identifies consolidation opportunities
2. **Calculates savings** - Shows financial benefits of consolidated orders
3. **Provides recommendations** - Clear cost optimization strategies

**Data**: Your agent gets real inventory data with supplier IDs, costs, and locations!

**Bonus**: You also have **WebSearchTool** for researching supplier information, shipping rates, and market conditions

## 🔧 Your Tools Explained

**`supplier_matcher`**: Groups items by supplier for consolidation

- Identifies which items can be ordered together
- Shows total cost and item count per supplier
- Maps supplier locations for shipping optimization
- Highlights multi-item consolidation opportunities

**`order_optimizer`**: Calculates financial benefits of consolidation  

- Compares individual vs consolidated shipping costs
- Applies volume discounts for large orders
- Shows per-supplier and total savings
- Identifies most profitable consolidation opportunities

**`WebSearchTool`**: For real-time supplier research

- Current shipping rates and policies
- Supplier reliability and performance data
- Market conditions and pricing trends
- Alternative supplier options

## 🚀 Quick Start

1. **First, read the main project README** to understand the setup
2. **Test your agent**: `python -m pytest -m agent04`
3. **Try the sample notebook** (copy from `notebooks/samples/`)

## 💡 Ideas for Iterations

**Enhance supplier grouping:**

- Add geographic clustering for shipping efficiency  
- Consider supplier lead times and reliability scores
- Factor in minimum order quantities and discounts
- Group by product categories or compatibility

**Improve savings calculations:**

- Add different shipping cost models (weight, distance, urgency)
- Consider bulk purchase discounts and tier pricing
- Factor in inventory holding costs vs ordering frequency
- Include supplier payment terms and cash flow benefits

**Use WebSearchTool for market intelligence:**

- Research current shipping rates and fuel costs
- Find alternative suppliers for better pricing
- Check supplier capacity and availability
- Monitor market trends affecting costs

**Make it more sophisticated:**

- Add supplier risk assessment and diversification
- Consider seasonal demand and bulk ordering strategies
- Optimize for multiple constraints (cost, time, quality)
- Include sustainability factors (carbon footprint, green suppliers)

## 🔗 Integration

Your agent works with:

- **Agent 01 (Threshold Monitor)** - Gets urgency levels for consolidation prioritization
- **Agent 02 (Route Computer)** - Coordinates consolidated deliveries with routing
- **Agent 03 (Restock Calculator)** - Gets quantities to optimize order sizes  
- **Agent 05 (Orchestrator)** - Provides consolidation recommendations for cost optimization

Focus on finding real cost savings through smart ordering! 💰
