"""Data loading utilities for logistics agents.

This module provides functions to load and process CSV data files for
inventory management and supply chain analysis.

Functions:
- load_inventory_from_csv: Load inventory items from CSV data
- create_inventory_context: Create InventoryContext from loaded data
- validate_csv_structure: Validate CSV file structure
"""

import pandas as pd
from typing import List, Dict, Optional
from pathlib import Path
from datetime import datetime

from ..models.inventory_data import (
    InventoryItem,
    Supplier,
    InventoryContext,
    ProductCategory,
    TransportationMode,
    InspectionResult
)
from ..config.settings import settings
from .logging_config import setup_logging
import logging

logger = logging.getLogger(__name__)


def load_inventory_from_csv(csv_path: str) -> List[InventoryItem]:
    """
    Load inventory items from the CSV file.

    This function reads the final_customer_location_aligned.csv file and
    converts each row into an InventoryItem object with proper type conversions
    and calculated fields.

    Args:
        csv_path: Path to the CSV file

    Returns:
        List of InventoryItem objects

    Raises:
        FileNotFoundError: If CSV file doesn't exist
        ValueError: If CSV structure is invalid
    """
    csv_file = Path(csv_path)
    if not csv_file.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    logger.info(f"Loading inventory data from {csv_path}")

    try:
        # Read CSV file
        df = pd.read_csv(csv_path)
        logger.info(f"Loaded {len(df)} records from CSV")

        # Validate CSV structure
        validate_csv_structure(df)

        items = []
        for index, row in df.iterrows():
            try:
                # Create InventoryItem from CSV row
                item = _create_inventory_item_from_row(row)
                items.append(item)
            except Exception as e:
                logger.warning(f"Skipping row {index} due to error: {e}")
                continue

        logger.info(f"Successfully created {len(items)} inventory items")
        return items

    except Exception as e:
        logger.error(f"Error loading CSV data: {e}")
        raise ValueError(f"Failed to load CSV data: {e}")


def create_inventory_context(csv_path: str, region: str = "Multi-region") -> InventoryContext:
    """
    Create an InventoryContext from CSV data.

    This function loads the CSV data and creates a complete InventoryContext
    with items, suppliers, and metadata that can be used by the agents.

    Args:
        csv_path: Path to the CSV file
        region: Geographic region for the analysis

    Returns:
        InventoryContext object ready for agent analysis
    """
    logger.info(f"Creating inventory context from {csv_path}")

    # Load inventory items
    items = load_inventory_from_csv(csv_path)

    # Extract suppliers from the data
    suppliers = _extract_suppliers_from_items(items)

    # Create context
    context = InventoryContext(
        items=items,
        suppliers=suppliers,
        analysis_date=datetime.now(),
        region=region,
        total_locations=len(set(item.location for item in items)),
        urgent_items=[
            item.item_id for item in items if item.is_below_threshold]
    )

    logger.info(
        f"Created inventory context with {len(items)} items and {len(suppliers)} suppliers")
    logger.info(f"Items below threshold: {len(context.items_below_threshold)}")
    logger.info(f"Critical items: {len(context.critical_items)}")

    return context


def validate_csv_structure(df: pd.DataFrame) -> None:
    """
    Validate that the CSV file has the expected structure.

    Args:
        df: DataFrame to validate

    Raises:
        ValueError: If required columns are missing
    """
    required_columns = [
        'Product type', 'SKU', 'Price', 'Availability', 'Number of products sold',
        'Revenue generated', 'Stock levels', 'Order quantities', 'Shipping times',
        'Shipping costs', 'Supplier name', 'Location', 'Manufacturing lead time'
    ]

    missing_columns = [
        col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    logger.info("CSV structure validation passed")


def _create_inventory_item_from_row(row: pd.Series) -> InventoryItem:
    """
    Create an InventoryItem from a CSV row.

    Args:
        row: Pandas Series representing a CSV row

    Returns:
        InventoryItem object
    """
    # Map product category
    product_type = str(row['Product type']).lower().strip()
    if product_type in ['haircare', 'hair care']:
        category = ProductCategory.HAIRCARE
    elif product_type in ['skincare', 'skin care']:
        category = ProductCategory.SKINCARE
    elif product_type == 'cosmetics':
        category = ProductCategory.COSMETICS
    else:
        category = ProductCategory.SKINCARE  # Default fallback

    # Map transportation mode
    transport_mode = TransportationMode.ROAD  # Default
    if 'Transportation modes' in row and pd.notna(row['Transportation modes']):
        transport_str = str(row['Transportation modes']).lower()
        if 'air' in transport_str:
            transport_mode = TransportationMode.AIR
        elif 'sea' in transport_str:
            transport_mode = TransportationMode.SEA
        elif 'rail' in transport_str:
            transport_mode = TransportationMode.RAIL

    # Map inspection result
    inspection_result = InspectionResult.PENDING  # Default
    if 'Inspection results' in row and pd.notna(row['Inspection results']):
        inspection_str = str(row['Inspection results']).lower()
        if 'pass' in inspection_str:
            inspection_result = InspectionResult.PASS
        elif 'fail' in inspection_str:
            inspection_result = InspectionResult.FAIL

    # Create the inventory item
    item = InventoryItem(
        # Core identification
        item_id=str(row['SKU']),
        name=f"{product_type}_product",
        category=category,

        # Inventory levels
        current_stock=int(row['Stock levels']),
        availability=int(row['Availability']),
        order_quantity=int(row['Order quantities']),

        # Cost information
        unit_cost=float(row['Price']),

        # Supplier information
        supplier_id=str(row['Supplier name']),
        location=str(row['Location']),

        # Sales data
        units_sold=int(row['Number of products sold']) if pd.notna(
            row['Number of products sold']) else 0,
        revenue=float(row['Revenue generated']) if pd.notna(
            row['Revenue generated']) else 0.0,

        # Shipping information
        customer_location=str(row.get('Customer location', '')),
        shipping_time=int(row['Shipping times']) if pd.notna(
            row['Shipping times']) else 0,
        shipping_carrier=str(row.get('Shipping carriers', '')),
        shipping_cost=float(row['Shipping costs']) if pd.notna(
            row['Shipping costs']) else 0.0,
        transportation_mode=transport_mode,

        # Manufacturing information
        manufacturing_lead_time=int(row['Manufacturing lead time']) if pd.notna(
            row['Manufacturing lead time']) else 0,
        inspection_result=inspection_result,
        defect_rate=float(row.get('Defect rates', 0.0)) if pd.notna(
            row.get('Defect rates', 0.0)) else 0.0,
    )

    return item


def _extract_suppliers_from_items(items: List[InventoryItem]) -> List[Supplier]:
    """
    Extract unique suppliers from inventory items.

    Args:
        items: List of inventory items

    Returns:
        List of unique suppliers
    """
    suppliers_dict = {}

    for item in items:
        if item.supplier_id not in suppliers_dict:
            # Create supplier from item data
            supplier = Supplier(
                supplier_id=item.supplier_id,
                name=item.supplier_id,  # Using supplier_id as name
                location=item.location,
                delivery_routes=[item.customer_location] if item.customer_location else [
                    item.location],
                lead_time_days=item.manufacturing_lead_time,
                minimum_order_value=0.0,  # Default value
                reliability_score=0.9,  # Default high reliability
                cost_competitiveness=0.8  # Default competitive score
            )
            suppliers_dict[item.supplier_id] = supplier
        else:
            # Update delivery routes if new customer location found
            existing_supplier = suppliers_dict[item.supplier_id]
            if item.customer_location and item.customer_location not in existing_supplier.delivery_routes:
                existing_supplier.delivery_routes.append(
                    item.customer_location)

    return list(suppliers_dict.values())


def get_sample_csv_path() -> str:
    """
    Get the path to the CSV file from settings.

    Returns:
        Path to the configured CSV file
    """
    # Use the configured data path from settings
    if settings.data_path.exists():
        return str(settings.data_path)

    raise FileNotFoundError(
        f"CSV file not found at configured path: {settings.data_path}. "
        f"Please ensure DATA_PATH in .env points to the correct file.")


def load_sample_inventory_context() -> InventoryContext:
    """
    Load a sample inventory context for testing using configured data path.

    Returns:
        InventoryContext with sample data
    """
    try:
        csv_path = get_sample_csv_path()
        logger.info(f"Loading inventory data from configured path: {csv_path}")
        return create_inventory_context(csv_path)
    except FileNotFoundError as e:
        logger.warning(f"Could not load sample data: {e}")
        logger.info("Creating minimal sample context for testing")

        # Create minimal sample data if CSV not found
        sample_items = [
            InventoryItem(
                item_id="SKU_SAMPLE_01",
                name="skincare_product",
                category=ProductCategory.SKINCARE,
                current_stock=5,  # Low stock for testing
                availability=25,
                order_quantity=50,
                unit_cost=25.99,
                supplier_id="Sample Supplier 1",
                location="Test Location",
                units_sold=100,
                revenue=2599.0,
                manufacturing_lead_time=7
            )
        ]

        sample_suppliers = [
            Supplier(
                supplier_id="Sample Supplier 1",
                name="Sample Supplier 1",
                location="Test Location",
                delivery_routes=["Test Location"],
                lead_time_days=7,
                minimum_order_value=100.0,
                reliability_score=0.9,
                cost_competitiveness=0.8
            )
        ]

        return InventoryContext(
            items=sample_items,
            suppliers=sample_suppliers,
            analysis_date=datetime.now(),
            region="Test Region",
            total_locations=1,
            urgent_items=["SKU_SAMPLE_01"]
        )
