# Agent 01 - Inventory Threshold Monitor

**Team Member**: Martin  
**Purpose**: Monitor inventory levels and identify items needing restocking

## 📁 What's in This Folder

- `agent.py` - Your main agent (monitors thresholds, classifies priorities)
- `tools/` - Your function tools:
  - `threshold_checker.py` - Finds items below reorder points
  - `priority_classifier.py` - Classifies items as HIGH/MEDIUM/LOW priority
- `tests/` - Test your agent quickly with `python -m pytest -m agent01`

## 🎯 What Your Agent Does

**Your agent monitors 100+ real inventory items and:**

1. **Identifies threshold violations** - Which items are below reorder points
2. **Classifies urgency** - Prioritizes which items need immediate attention
3. **Provides recommendations** - Clear actions for operations team

**Data**: Your agent already has access to real inventory data (no setup needed!)

## 🔧 Your Tools Explained

**`threshold_checker`**: Scans all inventory items and finds those below reorder thresholds

- Shows item ID, current stock, threshold level, and category
- Gives you a clear list of items needing attention

**`priority_classifier`**: Takes items below threshold and sorts by urgency

- **HIGH**: Critical stock levels (immediate action needed)
- **MEDIUM**: Important categories like skincare (plan restocking)  
- **LOW**: Other items (monitor but not urgent)

## 🚀 Quick Start

1. **First, read the main project README** to understand the setup
2. **Test your agent**: `python -m pytest -m agent01`
3. **Try the sample notebook** (copy from `notebooks/samples/`)

## 💡 Ideas for Iterations

**Enhance your priority logic:**

- Consider item value/revenue impact
- Factor in lead times and supplier reliability
- Add seasonal demand patterns
- Include customer tier importance

**Improve threshold detection:**

- Add "days until stockout" calculations  
- Consider demand variability
- Create different severity levels
- Add trend analysis (stock declining fast?)

**Make it more business-focused:**

- Add cost of stockout calculations
- Consider supplier minimum order quantities
- Factor in storage capacity constraints
- Include promotional event impacts

## 🔗 Integration

Your agent will be used by:

- **Agent 05 (Orchestrator)** - Coordinates your priorities with other agents
- **Agent 02 (Route Computer)** - Plans delivery routes based on your urgency
- **Agent 03 (Restock Calculator)** - Calculates quantities for your flagged items

Start simple, test frequently, document your improvements! 🎯
