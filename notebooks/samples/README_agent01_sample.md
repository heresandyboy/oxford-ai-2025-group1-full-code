# Agent 01 Sample Demo - Quick Start Guide

Simple guide for developing your agent using the **"Lab Notebook"** approach - edit your code, test in notebook, document results.

## 🚀 **Quick Start**

### **Option 1: VSCode (Recommended)**

1. Open the project in VSCode (install recommended extensions when prompted)
2. Open `agent01_sample_demo.ipynb` directly in VSCode
3. Add API key to `.env` file: `OPENAI_API_KEY=your-key-here`
4. Select the project's Python interpreter (`.venv/bin/python`)
5. Run notebook cells directly in VSCode - done!

### **Option 2: Google Colab**

1. Click the **"Open in Colab"** badge in the notebook
2. Add your OpenAI API key to Colab secrets:
   - Click 🔑 icon in left sidebar → Add `OPENAI_API_KEY`
3. Run all cells - done!

## 🔄 **Development Workflow**

**Simple 4-step cycle:**

1. **Document** what you're going to change in the notebook
2. **Edit** your `agent.py` and `tools/` files in your IDE
3. **Reload** in notebook: `importlib.reload(agent_module)`
4. **Test & document** the results

**Key benefit**: No code duplication - notebook imports from your actual project files.

## 📋 **What the Notebook Does**

1. **Auto-setup** - Detects Colab vs local, handles API keys
2. **Import your agent** - From real project structure (no copying code)
3. **Load real data** - 100+ inventory items from CSV
4. **Run baseline** - Test your agent works
5. **Iterate** - Make changes, reload, test, document
6. **Show integration** - How orchestrator will use your agent

## ❓ **Common Issues**

**"API key not found"**

- Colab: Add to secrets with exact name `OPENAI_API_KEY`
- Local: Check `.env` file exists with correct format

**"Import errors" in Colab**

- Make sure git clone completed successfully

**"Changes not reflected"**

- Always run `importlib.reload(agent_module)` after editing files

## 📝 **For Team Members**

1. **Copy this notebook** as your template
2. **Update imports** to point to your agent folder:

   ```python
   from src.logistics_agents.agents.agent_02_route_computer.agent import RouteComputer
   ```

3. **Follow same pattern** - document iterations and learning
4. **Focus on your domain** (routing, restocking, consolidation, orchestration)

---

**That's it!** Simple workflow: Edit code → Reload → Test → Document → Repeat
