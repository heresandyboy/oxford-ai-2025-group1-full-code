# Oxford AI Summit 2025: Logistics Use Case Implementation Guide

## Course Overview

**Event**: Oxford Artificial Intelligence Summit 2025 (June 27-28, 2025)  
**Theme**: "Autonomous AI Agents: Learning from deployments (low-code & full-code)"  
**Deadline**: July 6, 2025  
**Track**: Full-code implementation  

## Your Use Case: Logistics - Shipment and Delivery Tracking

**Use Case**: Analyzing logistics operations including warehouse handling, dispatch, and delivery  
**Goal**: Minimize delivery delays, improve routing efficiency, and manage supply chain risks

## Prerequisites (Must Have)

1. **OpenAI API Access**: Active OpenAI account with API key
2. **Google Account**: For Google Colab (no local installation needed)
3. **Basic Python Knowledge**: Understanding of async/await, basic programming
4. **LLM Understanding**: Basic knowledge of prompts and function calling

## Assignment Requirements

You must complete ALL of the following:

1. **Choose ONE Agent Pattern**: Select from Deterministic Workflows, Agents as Tools, or Parallel Execution
2. **Build Baseline Solution**: Create working agents that solve logistics challenges
3. **Use Tools**: Integrate at least one prebuilt OpenAI tool (WebSearch, CodeInterpreter, etc.)
4. **Iterate & Improve**: Refine prompts and configurations through multiple iterations
5. **Justify & Analyze**: Document why you chose your pattern and how each iteration improved performance

## 🚀 **Recommended Approach: Use the Sample Notebook Template**

**Instead of building from scratch, follow the proven workflow:**

1. **Use the sample notebook**: `notebooks/agent01_sample_demo.ipynb` as your template
2. **Follow the README guide**: `notebooks/README_agent01_sample.md` for step-by-step instructions
3. **Adapt for your agent**: Copy the template and modify for your specific logistics domain

**This approach gives you:**

- ✅ Pre-configured Colab compatibility with automatic API key handling
- ✅ Real project structure integration (no code duplication)
- ✅ Proven iteration workflow: Edit code → Reload → Test → Document
- ✅ Course requirement alignment built-in
- ✅ Professional development practices

## Step-by-Step Implementation

### Step 1: Quick Start (5 minutes)

**Option A: Google Colab (Recommended)**

1. Open the sample notebook: `notebooks/agent01_sample_demo.ipynb`
2. Click "Open in Colab" badge
3. Add your OpenAI API key to Colab secrets (🔑 icon)
4. Run all cells to verify setup

**Option B: Local Development**

1. Copy the sample notebook as your template
2. Follow instructions in `notebooks/README_agent01_sample.md`
3. Add API key to `.env` file and start Jupyter

### Step 2: Choose Your Agent Pattern & Domain

**For Logistics, we recommend "Agents as Tools" pattern because:**

- Dynamic decision-making fits logistics complexity
- Specialist agents can handle different logistics domains  
- Orchestrator can coordinate based on real-time conditions

**Choose your logistics domain:**

1. **Inventory Management** (Agent 01): Stock threshold monitoring (sample provided)
2. **Route Optimization** (Agent 02): Delivery route planning and optimization
3. **Demand Forecasting** (Agent 03): Predicting restocking needs and quantities
4. **Order Consolidation** (Agent 04): Supplier grouping and order optimization
5. **Orchestration** (Agent 05): Coordinating all logistics specialists

### Step 3: Follow the Sample Notebook Structure

The sample notebook already includes the course-required structure:

1. **Setup & Installation** ✅ (Auto-handles Colab vs local)
2. **Pattern Justification** ✅ (Why "Agents as Tools" for logistics)
3. **Real Data Loading** ✅ (100+ inventory items from CSV)
4. **Baseline Implementation** ✅ (Working agent with tools)
5. **Iteration Testing** ✅ (Edit code → reload → test workflow)
6. **Integration Preview** ✅ (How orchestrator uses your agent)

### Step 4: Develop Using the "Lab Notebook" Workflow

**Simple 4-step cycle** (as detailed in `README_agent01_sample.md`):

1. **Document** what you're going to change in the notebook
2. **Edit** your `agent.py` and `tools/` files in your IDE
3. **Reload** in notebook: `importlib.reload(agent_module)`
4. **Test & document** the results

**Key benefit**: No code duplication - notebook imports from your actual project files.

### Step 5: Required Iterations (Critical for Evaluation)

Document at least 3 iterations following the sample pattern:

**Example iteration format:**

```markdown
## Iteration 1: Enhanced Tool Instructions

**What I observed**: Agent's tool instructions could be more specific about business priorities.

**Changes made in codebase**:
- Enhanced `threshold_checker.py` to include more context about stockout risk
- Improved `priority_classifier.py` to consider business impact

**Results**: More business-relevant priorities and clearer action items
```

### Step 6: Test with Logistics Scenarios

Test your agents with realistic logistics scenarios:

1. **Inventory scenarios**: Low stock alerts, critical item prioritization
2. **Route scenarios**: Multi-stop optimization, traffic considerations  
3. **Demand scenarios**: Seasonal patterns, demand forecasting
4. **Integration scenarios**: Multiple agents working together

## Submission Requirements

### Deadline: July 6, 2025

### Submission Method

**Email to**: <ayse.mutlu@conted.ox.ac.uk>  
**Subject**: "Oxford AI Summit - Logistics Use Case Submission - [Your Name]"

### Required Deliverables

Your notebook (based on the sample template) must contain:

1. **Complete Working Implementation**:
   - All agent code (in project structure)
   - Notebook demonstrating functionality
   - Clear imports from project files (no code duplication)

2. **Visible Sample Runs**:
   - Run all cells before saving
   - Include output examples for each iteration
   - Show improvement progression

3. **Written Analysis** (Following sample structure):
   - Pattern choice justification
   - Iteration explanations with evidence
   - Performance analysis and improvements
   - Integration preview showing orchestration

4. **Course Requirements Met**:
   - ✅ Agent pattern implemented and justified
   - ✅ Function tools (`@function_tool`) used
   - ✅ Prebuilt tools integrated (CodeInterpreter, WebSearch)
   - ✅ Structured output with Pydantic models
   - ✅ 3+ documented iterations with reasoning

## Evaluation Criteria

Your submission will be evaluated on:

1. **Correctness**: Does it solve logistics problems effectively?
2. **Pattern Usage**: Proper implementation of chosen agent pattern
3. **Tool Integration**: Effective use of function tools and prebuilt tools
4. **Code Quality**: Clean project structure, well-commented code
5. **Analysis Depth**: Quality of iteration documentation and improvements
6. **Logistics Relevance**: How well it addresses real supply chain challenges

## Success Checklist

Before submission, verify you have:

- [ ] Used the sample notebook template approach (`agent01_sample_demo.ipynb`)
- [ ] Followed the README guide instructions (`README_agent01_sample.md`)
- [ ] Chosen and justified your agent pattern ("Agents as Tools" recommended)
- [ ] Built working baseline with function tools and prebuilt tools
- [ ] Completed 3+ documented iterations using the lab notebook workflow
- [ ] Tested with realistic logistics scenarios
- [ ] All code runs without errors in notebook
- [ ] All outputs visible in notebook
- [ ] Written analysis for each iteration
- [ ] Integration preview showing orchestration pattern

## Support Resources

- **Sample Notebook**: `notebooks/agent01_sample_demo.ipynb` (Your template)
- **Quick Start Guide**: `notebooks/README_agent01_sample.md` (Step-by-step workflow)
- **Canvas**: [https://canvas.ox.ac.uk/courses/275912](https://canvas.ox.ac.uk/courses/275912)
- **Mentors**: Available during the event + WhatsApp support
- **OpenAI Tracing**: [https://platform.openai.com](https://platform.openai.com)

## Quick Reference: Key Code Patterns

```python
# Import from project structure (no code duplication)
from src.logistics_agents.agents.agent_01_threshold_monitor.agent import InventoryThresholdMonitor

# Reload after making changes
importlib.reload(agent_module)
agent_v2 = agent_module.InventoryThresholdMonitor()

# Integration pattern (for orchestrator)
threshold_tool = agent.as_tool(
    tool_name="InventoryThresholdMonitor",
    tool_description="Monitor inventory thresholds and prioritize urgent restocking"
)
```

## Final Notes

- **Start with the sample notebook** (`agent01_sample_demo.ipynb`) - don't build from scratch
- **Follow the README guide** (`README_agent01_sample.md`) for smooth workflow
- **Keep logistics focus** throughout all implementations
- **Document every iteration** with business justification using the lab notebook approach
- **Test with realistic scenarios** from your specific logistics domain
- **Ask mentors** if you need clarification
