# The Oxford Artificial Intelligence Summit 2025: Autonomous AI Agents

Full Code Assignment

## Prerequisites

- **OpenAI API Access**: An OpenAI account with an API key is required for calling language models and using OpenAI-hosted tools.
- **Python Basics**: Familiarity with Python programming, as the SDK uses async calls.
- **LLM and Function-Calling Knowledge**: Understanding of prompt design and how large language models can call functions/tools.
- **Google Account**: Necessary for using Google Colab to run the code, eliminating the need for local installation.

## Assignment Task

Each group will:

1. Choose one Pattern to implement: Deterministic, Agents as Tools, or Parallel Execution.
2. Choose a Scenario from the list of use cases.
3. Build a Baseline Solution: Configure one or more agents to solve the task, even if the initial output is imperfect.
4. Use Tools: Integrate at least one prebuilt function/tool (e.g., web search, MCP) into the agent flow to extend capabilities.
5. Iterate Improvements: Refine prompts and configurations to enhance results.
6. Justify & Analyze: Explain why the chosen pattern was appropriate and how each iteration improved the agent’s performance.

## Use Cases

1. **Healthcare – Patient Journey Optimization**

    - **Use Case**: Analyzing patient flow from admission to discharge.
    - **Goal**: Identify bottlenecks (e.g., long wait times), unnecessary steps, or re-admissions to improve service delivery and reduce costs.

2. **Manufacturing – Production Line Efficiency**

    - **Use Case**: Tracking production workflows from raw materials to finished goods.
    - **Goal**: Detect deviations, delays, or inefficiencies in assembly lines to enhance throughput and reduce waste.

3. **Financial Services – Loan Application Processing**

    - **Use Case**: Monitoring the steps from loan application to approval or rejection.
    - **Goal**: Ensure compliance, reduce delays, and spot fraudulent patterns or unnecessary rework.

4. **E-commerce – Order-to-Cash (O2C) Process**

    - **Use Case**: Mapping customer order fulfillment from purchase to payment.
    - **Goal**: Reduce order delays, improve customer satisfaction, and optimize cash flow.

5. **Logistics – Shipment and Delivery Tracking**

    - **Use Case**: Analyzing logistics operations including warehouse handling, dispatch, and delivery.
    - **Goal**: Minimize delivery delays, improve routing efficiency, and manage supply chain risks.

6. **Public Sector – Permit and License Approvals**

    - **Use Case**: Monitoring application processes for building permits, business licenses, etc.
    - **Goal**: Streamline public services, reduce citizen wait times, and increase transparency.

7. **IT Service Management – Incident Resolution**

    - **Use Case**: Mapping IT incident management (e.g., ticket creation → triage → resolution).
    - **Goal**: Reduce Mean Time to Resolution (MTTR), identify recurring issues, and optimize service desk workflows.

8. **Telecommunications – Customer Onboarding**

    - **Use Case**: Tracking steps for onboarding new subscribers or activating services.
    - **Goal**: Ensure timely activations, reduce churn, and uncover causes of failed onboarding attempts.

9. **Insurance – Claims Processing**

    - **Use Case**: Analyzing the end-to-end claims handling process.
    - **Goal**: Detect fraud, accelerate payouts, and ensure regulatory compliance.

10. **Education – Student Enrollment and Course Progression**

    - **Use Case**: Mapping student actions from enrollment, registration, to course completion.
    - **Goal**: Identify drop-out risks, improve academic advising, and optimize program structure.

## Google Colab Setup

1. **Open a Colab Notebook**: Go to [colab.research.google.com](colab.research.google.com) and create a new Python 3 notebook. Ensure GPU/TPU acceleration is not needed (CPU is sufficient for API calls).
2. **Install the OpenAI Agents SDK**: In a Colab code cell, install the SDK from PyPI using the `pip` command:

    ```bash
    !pip install openai-agents
    ```

    This will install the Agents SDK and its dependencies.
3. **Set Up OpenAI API Key**: You can store your API key securely in Colab. For example:

    ```python
    import os
    os.environ["OPENAI_API_KEY"] = "sk-..." # replace with your actual key
    ```

    Alternatively, use Colab's secret feature or input form to avoid hardcoding the key. The OpenAI Agents SDK will pick up the `OPENAI_API_KEY` environment variable for authentication.
4. **Import the SDK Modules**: At minimum, you'll need:

    ```python
    from agents import Agent, Runner, ModelSettings, trace, gen_trace_id
    from agents import WebSearchTool, CodeInterpreterTool # (optional tools, as needed)
    ```

    - `Agent` is the core class to define an agent.
    - `Runner` executes agents.
    - `ModelSettings` allows configuration like parallelism or reasoning mode.
    - `trace` and `gen_trace_id` help capture and group execution traces (discussed later).
    - Tool classes like `WebSearchTool` (for web queries) or `CodeInterpreterTool` (to run code) can be imported when you plan to use them.
5. **Verify the Installation**: Run a quick test to ensure everything is set. For example:

    ```python
    print("OpenAI Agents SDK version:", __import__('agents').__version__)
    ```

    This should output the SDK version, confirming that the library is ready.

## Agents - Basic Configuration

The most common properties of an agent you'll configure are:

- `instructions`: Also known as a developer message or system prompt.
- `model`: Which LLM to use, and optional `model_settings` to configure model tuning parameters like temperature, top_p, etc.
- `tools`: Tools that the agent can use to achieve its tasks.

Example:

```python
from agents import Agent, ModelSettings, function_tool

@function_tool
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny"

agent = Agent(
    name="Haiku agent",
    instructions="Always respond in haiku form",
    model="o3-mini",
    tools=[get_weather],
)
```

## Agents - Context

Agents are generic on their context type. Context is a dependency-injection tool: it's an object you create and pass to `Runner.run()`, which is then passed to every agent, tool, handoff, etc. It serves as a collection of dependencies and state for the agent run. You can provide any Python object as the context.

Example:

```python
@dataclass
class UserContext:
    uid: str
    is_pro_user: bool

    async def fetch_purchases(self) -> list[Purchase]:
        return ...

agent = Agent[UserContext](
    ...,
)
```

## Agents - Output Types

By default, agents produce plain text (`str`) outputs. If you want the agent to produce a particular type of output, you can use the `output_type` parameter. A common choice is to use Pydantic objects, but any type that can be wrapped in a Pydantic `TypeAdapter` (dataclasses, lists, TypedDict, etc.) is supported.

Example:

```python
from pydantic import BaseModel
from agents import Agent

class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]

agent = Agent(
    name="Calendar extractor",
    instructions="Extract calendar events from text",
    output_type=CalendarEvent,
)
```

**Note**: When you pass an `output_type`, it tells the model to use structured outputs instead of regular plain text responses.

## Agents - Handoffs

Handoffs are sub-agents that the agent can delegate to. You provide a list of handoffs, and the agent can choose to delegate to them if relevant. This powerful pattern allows orchestrating modular, specialized agents that excel at a single task.

Example:

```python
from agents import Agent

booking_agent = Agent(...)
refund_agent = Agent(...)

triage_agent = Agent(
    name="Triage agent",
    instructions=(
        "Help the user with their questions."
        "If they ask about booking, handoff to the booking agent."
        "If they ask about refunds, handoff to the refund agent."
    ),
    handoffs=[booking_agent, refund_agent],
)
```

## Agents - Cloning

By using the `clone()` method on an agent, you can duplicate an `Agent` and optionally change any properties you like.

Example:

```python
pirate_agent = Agent(
    name="Pirate",
    instructions="Write like a pirate",
    model="o3-mini",
)

robot_agent = pirate_agent.clone(
    name="Robot",
    instructions="Write like a robot",
)
```

## Agents - Forcing Tool Use

Supplying a list of tools doesn't always mean the LLM will use a tool. You can force tool use by setting `ModelSettings.tool_choice`. Valid values are:

- `auto`: Allows the LLM to decide whether or not to use a tool.
- `required`: Requires the LLM to use a tool (but it can intelligently decide which tool).
- `none`: Requires the LLM to not use a tool.
- Setting a specific string (e.g., `"my_tool"`): Requires the LLM to use that specific tool.

**Note**: To prevent infinite loops, the framework automatically resets `tool_choice` to `"auto"` after a tool call. This behavior is configurable via `agent.reset_tool_choice`. The infinite loop occurs because tool results are sent to the LLM, which then generates another tool call due to `tool_choice`, leading to an infinite cycle.

If you want the Agent to completely stop after a tool call (rather than continuing with `auto` mode), you can set `Agent.tool_use_behavior="stop_on_first_tool"`, which will directly use the tool output as the final response without further LLM processing.

## Agents - Running Agents

You can run agents via the `Runner` class, with three options:

- `Runner.run()`: Runs asynchronously and returns a `RunResult`.
- `Runner.run_sync()`: A synchronous method that runs `.run()` under the hood.
- `Runner.run_streamed()`: Runs asynchronously and returns a `RunResultStreaming`. It calls the LLM in streaming mode and streams those events to you as they are received.

Example:

```python
from agents import Agent, Runner

async def main():
    agent = Agent(name="Assistant", instructions="You are a helpful assistant")

    result = await Runner.run(agent, "Write a haiku about recursion in programming.")
    print(result.final_output)
    # Code within the code,
    # Functions calling themselves,
    # Infinite loop's dance.
```

## Agents - Agent Loop

When you use the `run` method in `Runner`, you pass in a starting agent and input. The input can be a string (considered a user message) or a list of input items (items in the OpenAI Responses API).

The runner then runs a loop:

1. The LLM for the current agent is called with the current input.
2. The LLM produces its output.
3. If the LLM returns a `final_output`, the loop ends and the result is returned.
4. If the LLM does a handoff, the current agent and input are updated, and the loop re-runs.
5. If the LLM produces tool calls, those tool calls are run, the results are appended, and the loop re-runs.
6. If `max_turns` is exceeded, a `MaxTurnsExceeded` exception is raised.

## Agents - Run Config

The `run_config` parameter allows you to configure some global settings for the agent run:

- `model`: Allows setting a global LLM model to use, irrespective of what `model` each Agent has.
- `model_provider`: A model provider for looking up model names, which defaults to OpenAI.
- `model_settings`: Overrides agent-specific settings. For example, you can set a global `temperature` or `top_p`.
- `input_guardrails`, `output_guardrails`: A list of input or output guardrails to include on all runs.
- `handoff_input_filter`: A global input filter to apply to all handoffs if the handoff doesn't already have one. The input filter allows you to edit the inputs that are sent to the new agent.
- `tracing_disabled`: Allows you to disable tracing for the entire run.
- `trace_include_sensitive_data`: Configures whether traces will include potentially sensitive data, such as LLM and tool call inputs/outputs.
- `workflow_name`, `trace_id`, `group_id`: Sets the tracing workflow name, trace ID, and trace group ID for the run. It is recommended to at least set `workflow_name`. The `group_id` is an optional field that lets you link traces across multiple runs.
- `trace_metadata`: Metadata to include on all traces.

## Agents - Tracing

By default, the SDK traces the following:

- The entire `Runner.{run, run_sync, run_streamed}()` is wrapped in a `trace()`.
- Each time an agent runs, it is wrapped in `agent_span()`.
- LLM generations are wrapped in `generation_span()`.
- Function tool calls are each wrapped in `function_span()`.
- Guardrails are wrapped in `guardrail_span()`.
- Handoffs are wrapped in `handoff_span()`.
- Audio inputs (speech-to-text) are wrapped in a `transcription_span()`.
- Audio outputs (text-to-speech) are wrapped in a `speech_span()`.
- Related audio spans may be parented under a `speech_group_span()`.

By default, the trace is named "Agent trace". You can set this name if you use `trace`, or you can configure the name and other properties with the `RunConfig`.

In addition, you can set up custom trace processors to push traces to other destinations (as a replacement, or secondary destination).

## Agents - Higher Level Traces

Sometimes, you might want multiple calls to `run()` to be part of a single trace. You can do this by wrapping the entire code in a `trace()`.

Example:

```python
from agents import Agent, Runner, trace

async def main():
    agent = Agent(name="Joke generator", instructions="Tell funny jokes.")

    with trace("Joke workflow"):
        first_result = await Runner.run(agent, "Tell me a joke")
        second_result = await Runner.run(agent, f'Rate this joke: {first_result.final_output}')
        print(f'Joke: {first_result.final_output}')
        print(f'Rating: {second_result.final_output}')
```

## Understanding Agent Design Patterns

The OpenAI Agents SDK supports multiple agent orchestration patterns. Each pattern defines how tasks are broken down and how multiple agents might interact. Here are the three official patterns you can choose from, along with when to use each:

- Deterministic Workflows
- Agents as Tools
- Parallel Agent Execution

### Deterministic Workflows Design Pattern

Deterministic workflows are straightforward, fixed sequences of steps to accomplish a task. In this pattern, the flow of execution is predetermined by code, not by the LLM's reasoning. One agent’s output feeds directly into the next agent, and so on, in a linear pipeline.

- **Characteristics**: A fixed sequence of operations; each step is well-defined and does not vary. There is no branching logic based on content – it's always "do X, then Y, then Z".
- **When to Use**: Ideal when the problem can be broken into clear sub-tasks and the path to the goal is known in advance. If the end goal and method are certain, a deterministic chain is both simpler and more predictable in terms of cost, speed, and outcome.
- **Example Use-Case**: Shopping scenario – first generate a winter shopping list, then have another agent calculate the total cost. The steps and their order do not change.

Example:

```python
from pydantic import BaseModel
from agents import Agent, Runner

# Define structured output models for clarity
class ShoppingItem(BaseModel):
    name: str
    price: float
    url: str

class ShoppingList(BaseModel):
    items: list[ShoppingItem]

class TotalCostSummary(BaseModel):
    total: float
    item_count: int
    details: str

# Define agents
winter_agent = Agent(
    name="Winter Shopping List Agent",
    instructions="""
    You are an agent that generates a random shopping list for a complete winter outfit.
    Include various items like a jacket, scarf, gloves, hat, boots, etc.
    For each item, provide a name, a realistic price, and a placeholder URL.
    Return the list as a ShoppingList.
    """,
    output_type=ShoppingList,
)

cost_agent = Agent(
    name="Total Cost Agent",
    instructions="""
    You are a deterministic agent. Given a ShoppingList, calculate the total cost and item count,
    and return a TotalCostSummary with a details string in the format: 'Total for X items: $Y'.
    """,
    output_type=TotalCostSummary,
)

# Execute sequentially (deterministic flow)
async def main():
    shopping_list_result = await Runner.run(winter_agent, input="")
    shopping_list = shopping_list_result.final_output

    cost_result = await Runner.run(cost_agent, input=shopping_list.model_dump_json())
    summary = cost_result.final_output

    print(f"Summary: {summary.details}")
```

### Agents as Tool Design Pattern

The Agents-as-Tools pattern uses a central orchestrator agent that can invoke other specialist agents as tools to complete sub-tasks, without handing over full control. Unlike deterministic pipelines, the orchestrator decides at runtime which agent/tool to call next based on intermediate results or the problem’s needs.

- **Characteristics**: The orchestrator agent never relinquishes control; it uses other agents like function calls. The sequence of calls can vary: which sub-agent is invoked, how many times, and in what order can depend on the content of the task and partial results. This often involves the main agent doing some reasoning/planning step (sometimes called a "planner" agent).
- **When to Use**: Use this when you have a complex, open-ended task requiring multiple skills or tools, and the exact steps aren’t a straight line. The LLM can plan and select the appropriate tools/agents dynamically. It’s great for scenarios where different inputs may require different workflows, or iterative refinement is needed.
- **Example Use-Case**: Research & Synthesis Agent – an agent that, given a query, decides to use a Web Search tool if needed, then perhaps an Answer Composer agent as a tool, etc., to produce an answer.

Example:

```python
from agents import Agent, Runner, WebSearchTool, ModelSettings

# Define a simple information-fetching agent as a tool (e.g., uses web search)
search_tool_agent = Agent(
    name="WebSearchAgent",
    instructions="You are an agent that can search the web for information on a query and will integrate OpenAI's hosted web search tool.",
    tools=[WebSearchTool()],
    output_type=str, # assume it returns a text with search results summary
)

# Define an answer composing agent
answer_agent = Agent(
    name="AnswerComposerAgent",
    instructions="You take search findings and craft a concise answer for the user query.",
    output_type=str,
)

# Orchestrator agent that decides when to search and when to answer
orchestrator = Agent(
    name="OrchestratorAgent",
    instructions="""
    You are a knowledgeable assistant who can use tools to answer questions.
    1. If the user question needs external information, use the Search tool to find relevant data.
    2. Once you have enough information, use the AnswerComposer tool to formulate the final answer.
    Always return the final answer to the user when done.
    """,
    model_settings=ModelSettings(reasoning={"summary": "auto"}), # enable reasoning steps
    tools=[
        search_tool_agent.as_tool(tool_name="Search", tool_description="Find information on a query"),
        answer_agent.as_tool(tool_name="AnswerComposer", tool_description="Compose the final answer"),
    ],
)

async def main():
    result = await Runner.run(orchestrator, input="What are the latest Mars rover findings?")
    print(result.final_output)
```

### Parallel Agent Execution Design Pattern

The Parallel Execution pattern involves running multiple agents simultaneously (concurrently) to speed up processing or generate diverse results that can later be merged. Instead of sequential or orchestrated calls, parallel agents work independently on subtasks, and then their outputs are combined by a final step.

- **Characteristics**: Independent agents address different aspects of a task (or the same task in different ways) at the same time, often using Python concurrency (e.g., `asyncio.gather`) to run them in parallel threads or async tasks. There is typically an aggregator agent or code that waits for all results and then composes a final result.
- **When to Use**: Best when sub-tasks do not depend on each other’s immediate results (no need to wait for one agent before starting another). This pattern shines for speeding up multi-part problems (reducing latency by concurrent execution) or for exploring variations (having multiple agents attempt the same task in different ways and then picking the best result).
- **Example Use-Case**: Summarizing different aspects of a product review (features, pros/cons, sentiment, etc.) in parallel, then merging them.

Example:

```python
import asyncio
from agents import Agent, Runner

# Define multiple specialized agents (for brevity, instructions are abstracted)
features_agent = Agent(name="FeaturesAgent", instructions="Extract key features...", output_type=str)
pros_cons_agent = Agent(name="ProsConsAgent", instructions="List pros and cons...", output_type=str)
sentiment_agent = Agent(name="SentimentAgent", instructions="Analyze overall sentiment...", output_type=str)
recommend_agent = Agent(name="RecommendAgent", instructions="Give a recommendation with stars...", output_type=str)

# Input text to summarize (e.g., a product review)
review_text = "<LONG REVIEW TEXT>"

# Run all four agents in parallel on the same review text
async def main():
    results = await asyncio.gather(
        Runner.run(features_agent, input=review_text),
        Runner.run(pros_cons_agent, input=review_text),
        Runner.run(sentiment_agent, input=review_text),
        Runner.run(recommend_agent, input=review_text),
    )

    # Each result is a RunnerResult; get final outputs
    features_summary = results[0].final_output
    pros_cons_summary = results[1].final_output
    sentiment_summary = results[2].final_output
    recommendation = results[3].final_output

    # Aggregate the summaries (could use another agent or just format them)
    combined_summary = f"***Features:*** {features_summary}\n\n***Pros & Cons:*** {pros_cons_summary}\n\n***Sentiment:*** {sentiment_summary}\n\n***Recommendation:*** {recommendation}"
    print(combined_summary)
```

## Submission Process

- **Deadline**: 6 July 2025 – ensure your notebook is ready by then.
- **Submission Method**: Upload your Colab notebook (export as .ipynb or share the link with edit access) and email to <ayse.mutlu@conted.ox.ac.uk>.
- **What to Include**: The notebook should contain:
  1. All source code for agents and any support functions.
  2. Sample runs demonstrating the agent working.
  3. Written explanations/justifications for your pattern choice and iterations.
  4. Ensure outputs are visible (run all cells before saving, so evaluators can see results without rerunning).
- **Evaluation**: Completion will consider correctness (does it solve the task?), use of pattern and tools, clarity of code, and depth of analysis/improvement.
