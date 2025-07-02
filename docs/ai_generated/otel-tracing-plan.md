# Local OpenTelemetry Trace Visualization for Python Development

When working with OpenTelemetry (OTEL) in your Python application, especially with tools like the OpenAI Agents SDK, you often need a quick and easy way to visualize trace data directly within your development environment. This allows for efficient debugging and a better understanding of your application's flow without the overhead of a full-fledged observability backend.

While OpenTelemetry is a specification, not a visualization tool, there are excellent options for local development.

---

## 1. `otel-desktop-viewer`: The Top Pick for Local Visualization

For a simple, standalone, and visually appealing way to see your traces, **`otel-desktop-viewer`** is highly recommended. It's designed specifically for local OpenTelemetry trace visualization.

* **What it is:** A lightweight command-line interface (CLI) tool that functions as a minimal OpenTelemetry Collector and a web-based user interface (UI) for viewing traces. It's perfect for running alongside your application during development.
* **Why it's great:**
  * **Easy to install:** Often a single command or Docker run.
  * **Minimal dependencies:** No need for databases or complex backend setups.
  * **Local UI:** Provides a web interface (typically at `http://localhost:8000`) that displays your traces as intuitive Gantt charts or flame graphs.
  * **Direct OTLP Receiver:** It can receive OpenTelemetry Protocol (OTLP) data directly from your application.

* **How to Use It:**

    1. **Run `otel-desktop-viewer`:** The simplest way is often with Docker:

        ```bash
        docker pull davetron5000/otel-desktop-viewer:alpine-3
        docker run -p 8000:8000 -p 4317:4317 -p 4318:4318 davetron5000/otel-desktop-viewer:alpine-3
        ```

        This command pulls the Docker image and exposes the necessary ports: `8000` for the UI, `4317` for OTLP/gRPC, and `4318` for OTLP/HTTP.

    2. **Configure Your Python App:** Set your OpenTelemetry exporter endpoint to point to the viewer. This is typically done via environment variables before running your Python script:

        ```bash
        export OTEL_EXPORTER_OTLP_ENDPOINT="http://localhost:4317" # Use 4318 for HTTP
        export OTEL_EXPORTER_OTLP_PROTOCOL="grpc" # Use "http/protobuf" for HTTP
        ```

    3. **Run Your Python Application.**

    4. **Open Your Browser:** Navigate to `http://localhost:8000` to see your traces visualized in real-time.

---

## 2. OpenTelemetry Collector with Console Exporter

While not a visual tool, the OpenTelemetry Collector can be configured to simply print formatted trace data to your console. This is useful for quick, raw inspection of trace details.

* **What it is:** The OpenTelemetry Collector is a powerful, vendor-agnostic proxy for receiving, processing, and exporting telemetry data.
* **Why it's useful for local dev:**
  * **Local output:** You can configure a `logging` or `debug` exporter to print traces directly to your terminal.
  * **Basic filtering/processing:** Even locally, you can use the collector to filter or process traces before they are displayed in the console.

* **How to Use It:**

    1. **Download/Run OpenTelemetry Collector:**

        ```bash
        # Example for Linux/macOS (check for the latest release URL)
        wget [https://github.com/open-telemetry/opentelemetry-collector-releases/releases/latest/download/otelcol-contrib_linux_amd64](https://github.com/open-telemetry/opentelemetry-collector-releases/releases/latest/download/otelcol-contrib_linux_amd64)
        chmod +x otelcol-contrib_linux_amd64
        ```

    2. **Create a Minimal Collector Configuration (`collector-config.yaml`):**

        ```yaml
        receivers:
          otlp:
            protocols:
              grpc:
              http:
        exporters:
          # This will print traces to the console
          logging:
            loglevel: debug
        service:
          pipelines:
            traces:
              receivers: [otlp]
              exporters: [logging]
        ```

    3. **Run the Collector:**

        ```bash
        ./otelcol-contrib_linux_amd64 --config collector-config.yaml
        ```

    4. **Configure Your Python App:** Set your OpenTelemetry exporter endpoint to point to the collector:

        ```bash
        export OTEL_EXPORTER_OTLP_ENDPOINT="http://localhost:4317"
        export OTEL_EXPORTER_OTLP_PROTOCOL="grpc"
        ```

    5. **Run Your Python Application.** You will see the trace details printed in the terminal where the collector is running.

---

## 3. Jupyter Notebook / Python Environment (Custom Scripting)

For quick, ad-hoc analysis directly within a Jupyter Notebook or Python script, you can perform custom parsing and basic visualization. This requires more effort than a dedicated tool but offers maximum flexibility for specific analyses.

* **Approach:**
    1. **Export Spans to Console/File:** Configure your OpenTelemetry setup to export spans to the console using `ConsoleSpanExporter` or to a file.
    2. **Parse and Visualize:** Write Python code within your notebook to parse these outputs. You can then use libraries like `matplotlib` or `plotly` to create simple visualizations, such as Gantt charts for span durations or time series.

* **Example (Console Export for parsing):**

    ```python
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleExportSpanProcessor

    # Set up a tracer provider that exports to the console
    provider = TracerProvider()
    processor = SimpleExportSpanProcessor(ConsoleSpanExporter())
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)

    tracer = trace.get_tracer(__name__)

    def my_function_to_trace():
        with tracer.start_as_current_span("parent_operation"):
            print("Starting parent operation...")
            with tracer.start_as_current_span("child_task_1"):
                print("Executing child task 1...")
                import time
                time.sleep(0.05)
            with tracer.start_as_current_span("child_task_2"):
                print("Executing child task 2...")
                time.sleep(0.03)
            print("Parent operation completed.")

    my_function_to_trace()
    ```

    The output from `ConsoleSpanExporter` can then be programmatically parsed and visualized within your notebook.

---

## Which Option Should You Choose?

* For the **simplest standalone runnable tool that provides nice visual graphs** with minimal setup, **`otel-desktop-viewer`** is your best bet. It offers a dedicated UI for trace visualization.
* If you primarily need to inspect the **raw OpenTelemetry data flow in your terminal** without a graphical interface, the **OpenTelemetry Collector with a `logging` exporter** is very quick and efficient.
* For **deep, custom analysis or unique visualizations** directly within a data science or Python development workflow, consider **parsing exported data programmatically** in a Jupyter Notebook.
