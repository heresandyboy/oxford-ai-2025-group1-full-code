"""Main entry point for the logistics agents application."""

import click
from src.logistics_agents.main import main


@click.command()
@click.option("--debug", is_flag=True, help="Enable debug mode")
@click.option("--data-path", type=click.Path(exists=True), help="Path to logistics data file")
def cli(debug: bool, data_path: str) -> None:
    """Run the Logistics Agents analysis."""
    
    if debug:
        import os
        os.environ["DEBUG"] = "true"
        os.environ["LOG_LEVEL"] = "DEBUG"
    
    if data_path:
        import os
        os.environ["DATA_PATH"] = data_path
    
    main()


if __name__ == "__main__":
    cli() 