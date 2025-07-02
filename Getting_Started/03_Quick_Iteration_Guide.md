# Quick Iteration Guide - Agent Development

Super succinct workflow to develop your agent using the sample notebook template.

> **📝 Next Step**: Copy the sample notebook template for your assigned agent.

## 🚀 VSCode Setup (Recommended)

### Initial Setup

```bash
./install.sh
cp .env.example .env
# Add: OPENAI_API_KEY=your-key-here to .env
source .venv/Scripts/activate  # Windows
source .venv/bin/activate      # Mac/Linux
```

### Verify Setup

```bash
python -m pytest -m agent01 -v
```

## 📓 Notebook Iteration Workflow

### 1. Copy Template

```bash
cp notebooks/samples/agent01_sample_demo.ipynb notebooks/agent0X_yourname_demo.ipynb
```

### 2. Update for Your Agent

**Cell 2** - Change imports:

```python
# Agent 02: from ...agent_02_route_computer.agent import RouteComputer
# Agent 03: from ...agent_03_restock_calculator.agent import RestockCalculator
# Agent 04: from ...agent_04_order_consolidator.agent import OrderConsolidator
# Agent 05: from ...agent_05_orchestrator.agent import Orchestrator
```

**All cells** - Update agent creation:

```python
agent = RouteComputer()  # or your agent class
```

### 3. Iteration Pattern

1. **Baseline**: Run notebook as-is → See current performance
2. **Edit**: Modify your agent files in VSCode:
   - `src/logistics_agents/agents/agent_XX_*/agent.py`
   - `src/logistics_agents/agents/agent_XX_*/tools/*.py`
3. **Reload**: Run iteration cell → `importlib.reload()` picks up changes
4. **Compare**: See tool inputs/outputs and improvements
5. **Document**: Add your observations in text cells

### 4. Key Features

- **Real data**: 100 inventory items from CSV (no fallbacks)
- **Tool logging**: See exact inputs/outputs for each tool call
- **Agent prompts**: Captured before/after each iteration
- **Clean comparison**: Side-by-side results across iterations

## 🔧 Quick Commands

**Test your specific agent:**

```bash
python -m pytest -m agent02 -v  # or agent03, agent04, agent05
```

**Run full system:**

```bash
python run.py
```

## 🐛 Troubleshooting

**"Import errors"**

- Ensure Python interpreter is `.venv/bin/python`
- **Restart VSCode** to load workspace settings

**"Changes not reflected"**

- Always run the reload cell: `importlib.reload(agent_module)`

**"Tool inputs/outputs not showing"**

- Use `display_logs("detailed")` to see full agent/tool interactions
- Logs capture the same detail as log files but display in notebook

## 📋 Team Assignments

- **Agent 01** = Martin (Sample provided)
- **Agent 02** = Rhiannon (Route Computer)
- **Agent 03** = Nathan (Restock Calculator)
- **Agent 04** = Anagha (Order Consolidator)
- **Agent 05** = Andy (Orchestrator)

## 🎯 Submission Ready

Your notebook should show:

- ✅ Baseline agent performance
- ✅ 2-3 iterations with clear improvements
- ✅ Tool inputs/outputs captured for each iteration
- ✅ Integration pattern (agent becomes tool for orchestrator)
- ✅ Lessons learned and performance improvements documented
