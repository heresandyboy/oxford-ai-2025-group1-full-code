# Agent 03 - Restocking Calculator

**Team Member**: Nathan  
**Purpose**: Analyze demand patterns and calculate optimal reorder quantities

## 📁 What's in This Folder

- `agent.py` - Your main agent (forecasts demand, calculates quantities)
- `tools/` - Your function tools:
  - `demand_forecaster.py` - Estimates demand patterns for low-stock items
  - `quantity_optimizer.py` - Calculates reorder quantities using EOQ principles
- `tests/` - Test your agent quickly with `python -m pytest -m agent03`

## 🎯 What Your Agent Does

**Your agent analyzes inventory data and:**

1. **Forecasts demand** - Estimates consumption patterns for urgent items
2. **Calculates quantities** - Determines optimal reorder amounts using EOQ
3. **Provides cost analysis** - Shows total costs and recommendations

**Data**: Your agent gets real inventory data with costs, stock levels, and order quantities!

**Bonus**: You also have **CodeInterpreter** tool for advanced mathematical analysis (EOQ optimization, statistical forecasting, etc.)

## 🔧 Your Tools Explained

**`demand_forecaster`**: Analyzes consumption patterns

- Calculates consumption rates from stock data
- Classifies demand as HIGH/MEDIUM/LOW
- Estimates monthly demand with safety buffer
- Identifies fast-moving vs slow-moving items

**`quantity_optimizer`**: Calculates optimal reorder quantities

- Uses EOQ (Economic Order Quantity) formula
- Factors in holding costs and ordering costs
- Shows recommended order quantity and total cost
- Compares current stock vs optimal levels

**`CodeInterpreter`**: For complex calculations

- Advanced EOQ variations and optimizations
- Statistical demand forecasting models
- Cost-benefit analysis and scenarios
- Inventory optimization algorithms

## 🚀 Quick Start

1. **First, read the main project README** to understand the setup
2. **Test your agent**: `python -m pytest -m agent03`  
3. **Try the sample notebook** (copy from `notebooks/samples/`)

## 💡 Ideas for Iterations

**Enhance demand forecasting:**

- Add seasonal demand patterns
- Consider trend analysis (growing/declining demand)
- Factor in promotional events and campaigns
- Use moving averages for smoother forecasts

**Improve quantity optimization:**

- Add different EOQ variations (quantity discounts, shortage costs)
- Consider supplier minimum order quantities
- Factor in storage capacity constraints
- Add multi-period optimization

**Use CodeInterpreter for advanced math:**

- Implement advanced forecasting models (ARIMA, exponential smoothing)
- Optimize safety stock calculations
- Analyze demand uncertainty and risk
- Create inventory cost optimization models

**Make it more business-focused:**

- Add lead time variability considerations
- Factor in supplier reliability scores
- Consider cash flow and working capital impacts
- Include service level requirements

## 🔗 Integration

Your agent works with:

- **Agent 01 (Threshold Monitor)** - Gets urgent items needing quantity analysis
- **Agent 02 (Route Computer)** - Provides quantities for vehicle load optimization
- **Agent 04 (Order Consolidator)** - Supplies quantities for order grouping
- **Agent 05 (Orchestrator)** - Provides quantity recommendations for restocking plans

Focus on mathematical accuracy and cost optimization! 📊
