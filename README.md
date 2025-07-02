# Oxford AI Summit 2025 - Logistics Multi-Agent System

**Supply Chain Optimization using "Agents as Tools" Pattern**

## 🚀 Quick Start

**VSCode Users**: This project includes optimized VSCode settings and extension recommendations in `.vscode/`. Simply open the project in VSCode and install the recommended extensions when prompted.

First copy the `.env.example` file to a new file called `.env` in the same directory and enter your `OPENAI_API_KEY`

1. **Install & Setup**:

   ```bash
   ./install.sh
   cp .env.example .env
   # Add your OpenAI API key to .env
   ```

2. **Activate Environment** (once per session *IMPORTANT!*):

   ```bash
   source .venv/Scripts/activate  # Windows
   source .venv/bin/activate      # Mac/Linux
   ```

   **Why?** Virtual environment isolates project dependencies from your system Python.

   **Check you're in venv**: Command prompt shows `(oxford-ai-2025-group1-full-code)` prefix

   **To exit venv**: `deactivate` (when done working)

   ⚠️ **Always ensure you're in the venv before running any Python commands or tests!**

3. **Test Installation**:

   ```bash
   python -m pytest -m agent01    # Test your agent
   python run.py                  # Run full system
   ```

## 📝 Comprehensive Logging System

**All agent and tool interactions are automatically logged!**

👉 **Full Logging Guide**: [`Getting_Started/02_Logging_Guide.md`](Getting_Started/02_Logging_Guide.md)

- Complete logging configuration instructions
- Test execution with full visibility
- Log analysis and debugging commands
- Development workflow with logging

## 📚 Course Requirements & Guidelines

👉 **Read the Course Guide**: [`Getting_Started/01_Course_Guide.md`](Getting_Started/01_Course_Guide.md)

- Assignment requirements & evaluation criteria
- Step-by-step implementation approach
- Submission guidelines & deadlines

## 🔬 Development Workflow

👉 **Copy the Sample Notebook** (don't use the original!):

- **Template to copy**: [`notebooks/samples/agent01_sample_demo.ipynb`](notebooks/samples/agent01_sample_demo.ipynb)
- **Guide**: [`notebooks/samples/README_agent01_sample.md`](notebooks/samples/README_agent01_sample.md)

**Two-level development approach**:

1. **Quick testing** → Use your `tests/` folder for rapid development and small changes
2. **Document iterations** → Use your copied notebook to capture significant improvements

**Daily workflow**: Edit code → Run tests with logging → Review logs → When happy → Document in notebook

## 👥 Team Agent Assignments

| Agent | Team Member | Purpose | Location | Quick Guide |
|-------|-------------|---------|----------|-------------|
| **01** | **Martin** | Inventory Threshold Monitor | `src/logistics_agents/agents/agent_01_threshold_monitor/` | [README.md](src/logistics_agents/agents/agent_01_threshold_monitor/README.md) |
| **02** | **Rhiannon** | Route Computer | `src/logistics_agents/agents/agent_02_route_computer/` | [README.md](src/logistics_agents/agents/agent_02_route_computer/README.md) |
| **03** | **Nathan** | Restocking Calculator | `src/logistics_agents/agents/agent_03_restock_calculator/` | [README.md](src/logistics_agents/agents/agent_03_restock_calculator/README.md) |
| **04** | **Anagha** | Order Consolidator | `src/logistics_agents/agents/agent_04_order_consolidator/` | [README.md](src/logistics_agents/agents/agent_04_order_consolidator/README.md) |
| **05** | **Andy** | Orchestrator | `src/logistics_agents/agents/agent_05_orchestrator/` | [README.md](src/logistics_agents/agents/agent_05_orchestrator/README.md) |

## 📁 Project Structure

```
oxford-ai-2025-group1-full-code/
├── Getting_Started/
│   └── 01_Course_Guide.md              # Course requirements & guidelines
├── notebooks/
│   └── samples/
│       ├── agent01_sample_demo.ipynb   # Notebook template (copy this!)
│       └── README_agent01_sample.md    # Iteration workflow guide
├── logs/                               # 🆕 AUTO-GENERATED LOG FILES
│   └── logistics_agents_YYYYMMDD_HHMMSS_username.log
├── data/
│   ├── final_customer_location_aligned.csv  # Real inventory data (100+ items)
│   └── outputs/                        # Analysis results
├── src/
│   └── logistics_agents/
│       ├── main.py                     # Application entry point
│       ├── config/                     # Configuration management
│       ├── models/                     # Data models & schemas
│       ├── utils/                      # Shared utilities & data loading
│       │   ├── logging_config.py       # 🆕 ENHANCED LOGGING SYSTEM
│       │   └── agent_runner.py         # 🆕 LOGGED AGENT EXECUTION
│       └── agents/                     # Individual agent implementations
│           ├── conftest.py             # Shared test fixtures
│           ├── agent_01_threshold_monitor/     # Martin's agent
│           │   ├── agent.py            # Main agent implementation
│           │   ├── tools/              # Function tools (@function_tool)
│           │   │   ├── threshold_checker.py    # 🆕 WITH LOGGING
│           │   │   └── priority_classifier.py  # 🆕 WITH LOGGING
│           │   ├── tests/              # Unit tests
│           │   └── README.md           # Agent-specific docs
│           ├── agent_02_route_computer/        # Rhiannon's agent
│           ├── agent_03_restock_calculator/    # Nathan's agent
│           ├── agent_04_order_consolidator/    # Anagha's agent
│           └── agent_05_orchestrator/          # Andy's agent
├── install.sh                         # Setup script
├── run.py                             # Run application
└── pyproject.toml                     # Dependencies
```

## 🛠️ Development Commands

**Quick Testing with Logging** (use for rapid development):

```bash
# Basic testing with logging output
python -m pytest -m agent01 -v -s --log-cli-level=INFO
python -m pytest -m agent02 -v -s --log-cli-level=INFO
python -m pytest -m agent03 -v -s --log-cli-level=INFO
python -m pytest -m agent04 -v -s --log-cli-level=INFO
python -m pytest -m agent05 -v -s --log-cli-level=INFO

# Detailed testing with full input/output logging
python -m pytest -m agent01 -v -s --log-cli-level=DEBUG --tb=short

# All tests with logging
python -m pytest -v -s --log-cli-level=INFO
python -m pytest -m integration -v -s --log-cli-level=INFO
```

**Cost-Aware Testing** (manage OpenAI API usage):

```bash
# Run cheap tests only (skip expensive orchestration)
python -m pytest -m "agent05 and not expensive" -v -s --log-cli-level=INFO

# Run the full end-to-end orchestration test (expensive!)
python -m pytest -m "agent05 and expensive" -v -s --log-cli-level=INFO

# Run all agents except expensive tests
python -m pytest -m "not expensive" -v -s --log-cli-level=INFO
```

👉 **For detailed logging commands**: See [`Getting_Started/02_Logging_Guide.md`](Getting_Started/02_Logging_Guide.md)

**Course Documentation** (use for iteration capture):

```bash
python -m jupyterlab                # Start notebooks for iteration documentation
python run.py                       # Test full system integration (creates log file)
```

## 🎯 Your Next Steps

1. **Read the Course Guide** to understand requirements
2. **Copy the sample notebook** and rename for your agent (e.g., `agent02_rhiannon_demo.ipynb`)
3. **Work in your agent folder** (`src/logistics_agents/agents/agent_XX_*/`)
4. **Use tests for quick development** (`python -m pytest -m agentXX -v -s --log-cli-level=INFO`)
5. **Review logs** to understand agent/tool interactions (`logs/` folder)
6. **Use notebook for documented iterations** (significant improvements only)

**Remember**:

- Tests + Logs = quick development with full visibility
- Notebook = course iteration documentation
- Check `/logs/` folder after every run for detailed execution traces

## 📊 Course Pattern: "Agents as Tools"

Each specialist agent implements domain expertise and can be used as a tool by the orchestrator agent, enabling dynamic coordination based on real-time logistics conditions.

**All interactions are automatically logged for learning and debugging!**

---

**Ready to start?** → [`Getting_Started/01_Course_Guide.md`](Getting_Started/01_Course_Guide.md)

---

## 📊 System Architecture Diagrams

### Overall System Architecture - "Agents as Tools" Pattern

```mermaid
%% =============================================================================
%% LOGISTICS AGENTS SYSTEM ARCHITECTURE - "Agents as Tools" Pattern
%% =============================================================================

%% Overall System Architecture
graph TB
    subgraph "🏢 Logistics Multi-Agent System"
        Main["🚀 main.py<br/>Entry Point"] --> Orchestrator["🎯 Agent 05<br/>Orchestrator<br/>(Andy)"]

        subgraph "🎛️ Orchestrator Tools"
            OT1["📋 agent_coordinator"]
            OT2["📊 result_synthesizer"]
        end

        subgraph "🔧 Specialist Agents (as Tools)"
            Agent01["🚨 Agent 01<br/>Threshold Monitor<br/>(Martin)"]
            Agent02["🗺️ Agent 02<br/>Route Computer<br/>(Rhiannon)"]
            Agent03["📈 Agent 03<br/>Restock Calculator<br/>(Nathan)"]
            Agent04["📦 Agent 04<br/>Order Consolidator<br/>(Anagha)"]
        end

        Orchestrator --> OT1
        Orchestrator --> OT2
        Orchestrator -.->|"as_tool()"| Agent01
        Orchestrator -.->|"as_tool()"| Agent02
        Orchestrator -.->|"as_tool()"| Agent03
        Orchestrator -.->|"as_tool()"| Agent04
    end

    subgraph "📊 Data Flow"
        CSV["📄 Inventory CSV"] --> Context["🏗️ InventoryContext"]
        Context --> Orchestrator
    end

    style Orchestrator fill:#e1f5fe,stroke:#0277bd,stroke-width:3px
    style Agent01 fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    style Agent02 fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    style Agent03 fill:#e8f5e8,stroke:#388e3c,stroke-width:2px
    style Agent04 fill:#fce4ec,stroke:#c2185b,stroke-width:2px
```

### Agent 05 - Orchestrator Workflow

```mermaid
graph TD
    subgraph "🎯 Agent 05 - Orchestrator Workflow (Andy)"
        Start["🚀 Start Analysis"] --> Coord["📋 coordinate_workflow_steps<br/>Plan execution sequence"]

        Coord --> Step1["1️⃣ Call InventoryThresholdMonitor<br/>Identify urgent items"]
        Step1 --> Step2["2️⃣ Call RestockingCalculator<br/>Calculate optimal quantities"]
        Step2 --> Step3["3️⃣ Call RouteComputer<br/>Plan delivery routes"]
        Step3 --> Step4["4️⃣ Call OrderConsolidator<br/>Optimize order grouping"]
        Step4 --> Synth["📊 create_executive_summary<br/>Synthesize all results"]

        Synth --> Final["📋 Final Recommendations<br/>Comprehensive logistics plan"]
    end

    subgraph "🔄 Agents as Tools Pattern"
        AgentTools["🔧 Specialist Agents Available as Tools"]
        AgentTools --> T1["🚨 InventoryThresholdMonitor.as_tool()"]
        AgentTools --> T2["🗺️ RouteComputer.as_tool()"]
        AgentTools --> T3["📈 RestockingCalculator.as_tool()"]
        AgentTools --> T4["📦 OrderConsolidator.as_tool()"]
    end

    Step1 -.-> T1
    Step2 -.-> T3
    Step3 -.-> T2
    Step4 -.-> T4

    style Start fill:#e1f5fe,stroke:#0277bd,stroke-width:3px
    style Final fill:#e8f5e8,stroke:#388e3c,stroke-width:3px
    style Coord fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    style Synth fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
```

### Data Flow Sequence

```mermaid
sequenceDiagram
    participant CSV as 📄 CSV Data
    participant Main as 🚀 main.py
    participant Orch as 🎯 Orchestrator
    participant A01 as 🚨 Agent 01<br/>Threshold
    participant A03 as 📈 Agent 03<br/>Restock Calc
    participant A02 as 🗺️ Agent 02<br/>Route Comp
    participant A04 as 📦 Agent 04<br/>Consolidator

    CSV->>Main: Load inventory data
    Main->>Orch: InventoryContext

    Note over Orch: 📋 coordinate_workflow_steps

    Orch->>A01: Analyze thresholds
    A01->>A01: threshold_checker
    A01->>A01: priority_classifier
    A01->>Orch: Priority items + urgency

    Orch->>A03: Calculate quantities
    A03->>A03: demand_forecaster
    A03->>A03: quantity_optimizer
    A03->>Orch: Optimal quantities + costs

    Orch->>A02: Plan routes
    A02->>A02: route_calculator
    A02->>A02: delivery_scheduler
    A02->>Orch: Routes + schedules

    Orch->>A04: Consolidate orders
    A04->>A04: supplier_matcher
    A04->>A04: order_optimizer
    A04->>Orch: Consolidated orders + savings

    Note over Orch: 📊 create_executive_summary

    Orch->>Main: Final recommendations
    Main->>Main: 📋 Display results
```
