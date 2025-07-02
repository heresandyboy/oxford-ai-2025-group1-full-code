# Agent 02 - Route Computer

**Team Member**: Rhiannon  
**Purpose**: Calculate delivery routes and schedules for restocking operations

## 📁 What's in This Folder

- `agent.py` - Your main agent (computes routes, schedules deliveries)
- `tools/` - Your function tools:
  - `route_calculator.py` - Calculates routes between suppliers and customers
  - `delivery_scheduler.py` - Creates delivery schedules for urgent items
- `tests/` - Test your agent quickly with `python -m pytest -m agent02`

## 🎯 What Your Agent Does

**Your agent analyzes inventory data and:**

1. **Calculates routes** - Finds optimal paths between suppliers and customers
2. **Schedules deliveries** - Prioritizes deliveries based on urgency
3. **Provides logistics plans** - Clear routing and timing recommendations

**Data**: Your agent gets real inventory data including supplier/customer locations!

**Bonus**: You also have **CodeInterpreter** tool for mathematical calculations (distances, costs, etc.)

## 🔧 Your Tools Explained

**`route_calculator`**: Calculates delivery routes for items needing restocking

- Maps supplier locations to customer locations
- Estimates distances between major Indian cities
- Shows item ID and delivery path

**`delivery_scheduler`**: Creates schedules based on urgency

- Prioritizes HIGH vs MEDIUM priority items
- Assigns delivery dates based on stock levels
- Shows supplier → customer delivery plan

**`CodeInterpreter`**: For complex calculations

- Distance optimization algorithms
- Cost calculations
- Route efficiency analysis

## 🚀 Quick Start

1. **First, read the main project README** to understand the setup
2. **Test your agent**: `python -m pytest -m agent02`
3. **Try the sample notebook** (copy from `notebooks/samples/`)

## 💡 Ideas for Iterations

**Enhance route calculation:**

- Add real distance APIs (Google Maps, MapBox)
- Consider traffic patterns and delivery windows
- Optimize for fuel costs and vehicle capacity
- Add multi-stop route optimization

**Improve scheduling logic:**

- Factor in supplier lead times
- Consider delivery vehicle availability
- Add time-based priority adjustments
- Include seasonal demand patterns

**Use CodeInterpreter for advanced math:**

- Implement traveling salesman problem solver
- Calculate route efficiency metrics
- Optimize delivery batch sizes
- Analyze cost vs time trade-offs

**Make it more realistic:**

- Add delivery time windows
- Consider vehicle capacity constraints
- Factor in driver working hours
- Include weather/traffic delays

## 🔗 Integration

Your agent works with:

- **Agent 01 (Threshold Monitor)** - Gets urgency priorities for routing
- **Agent 03 (Restock Calculator)** - Gets quantities to optimize vehicle loads
- **Agent 04 (Order Consolidator)** - Coordinates with consolidated orders
- **Agent 05 (Orchestrator)** - Provides routing plans for overall logistics

Focus on practical routing that saves time and money! 🚛
