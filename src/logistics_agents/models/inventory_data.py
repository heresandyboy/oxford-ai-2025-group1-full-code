"""Core inventory and supply chain data models."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProductCategory(str, Enum):
    """Product categories for inventory classification."""

    HAIRCARE = "haircare"
    SKINCARE = "skincare"
    COSMETICS = "cosmetics"


class TransportationMode(str, Enum):
    """Available transportation modes for shipping."""

    ROAD = "Road"
    AIR = "Air"
    SEA = "Sea"
    RAIL = "Rail"


class InspectionResult(str, Enum):
    """Quality inspection results."""

    PASS = "Pass"
    FAIL = "Fail"
    PENDING = "Pending"


class Priority(str, Enum):
    """Priority levels for restocking orders."""

    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


@dataclass
class InventoryItem:
    """
    Represents a single inventory item from the CSV data.

    This model maps directly to the CSV structure and provides
    type safety and validation for inventory operations.

    Attributes:
        item_id: Unique identifier (SKU) for the inventory item
        name: Descriptive name derived from product type
        category: Product category (haircare, skincare, cosmetics)
        current_stock: Current stock level in inventory
        availability: Availability percentage (0-100)
        order_quantity: Typical order quantity for restocking
        unit_cost: Cost per unit (Price from CSV)
        supplier_id: Identifier of the supplier
        location: Supplier location
        units_sold: Number of products sold (historical data)
        revenue: Revenue generated from sales
        customer_location: Primary customer destination
        shipping_time: Shipping time in days
        shipping_carrier: Carrier used for shipping
        shipping_cost: Cost of shipping
        transportation_mode: Mode of transportation
        manufacturing_lead_time: Lead time for manufacturing
        inspection_result: Quality inspection status
        defect_rate: Defect rate percentage
    """

    # Core identification
    item_id: str  # SKU
    name: str  # Product type + "_product"
    category: ProductCategory

    # Inventory levels
    current_stock: int
    availability: int  # 0-100 percentage
    order_quantity: int

    # Cost information
    unit_cost: float  # Price from CSV

    # Supplier information
    supplier_id: str
    location: str  # Supplier location

    # Sales data
    units_sold: int = 0  # Number of products sold
    revenue: float = 0.0  # Revenue generated

    # Shipping information
    customer_location: str = ""  # Customer location
    shipping_time: int = 0  # Shipping times
    shipping_carrier: str = ""  # Shipping carriers
    shipping_cost: float = 0.0  # Shipping costs
    transportation_mode: TransportationMode = TransportationMode.ROAD

    # Manufacturing information
    manufacturing_lead_time: int = 0  # Manufacturing lead time
    inspection_result: InspectionResult = InspectionResult.PENDING
    defect_rate: float = 0.0  # Defect rates

    # Calculated fields
    reorder_threshold: Optional[int] = None  # Will be calculated
    last_restocked: Optional[datetime] = None

    def __post_init__(self) -> None:
        """Post-initialization validation and calculations."""
        # Calculate reorder threshold if not provided (20% of order quantity)
        if self.reorder_threshold is None:
            self.reorder_threshold = max(10, int(self.order_quantity * 0.2))

    @property
    def is_below_threshold(self) -> bool:
        """Check if current stock is below reorder threshold."""
        return self.current_stock <= (self.reorder_threshold or 0)

    @property
    def is_critical(self) -> bool:
        """Check if stock level is critically low (below 50% of threshold)."""
        threshold = self.reorder_threshold or 0
        return self.current_stock <= (threshold * 0.5)

    @property
    def stock_turnover_rate(self) -> float:
        """Calculate inventory turnover rate."""
        if self.current_stock <= 0:
            return 0.0
        return self.units_sold / self.current_stock

    @property
    def daily_demand(self) -> float:
        """Estimate daily demand based on monthly sales."""
        return self.units_sold / 30 if self.units_sold > 0 else 0.0

    @property
    def days_of_stock(self) -> float:
        """Calculate how many days of stock remain at current demand."""
        if self.daily_demand <= 0:
            return float("inf")
        return self.current_stock / self.daily_demand


@dataclass
class Supplier:
    """
    Represents a supplier in the supply chain.

    Attributes:
        supplier_id: Unique identifier for the supplier
        name: Supplier name
        location: Primary supplier location
        delivery_routes: List of locations this supplier can deliver to
        lead_time_days: Average lead time in days
        minimum_order_value: Minimum order value required
        reliability_score: Reliability rating (0.0-1.0)
        cost_competitiveness: Cost competitiveness rating (0.0-1.0)
    """

    supplier_id: str
    name: str
    location: str
    delivery_routes: List[str]
    lead_time_days: int
    minimum_order_value: float = 0.0
    reliability_score: float = 1.0  # 0.0-1.0
    cost_competitiveness: float = 1.0  # 0.0-1.0

    @property
    def performance_score(self) -> float:
        """Calculate overall supplier performance score."""
        # Weighted score: reliability 60%, cost 40%
        return (self.reliability_score * 0.6) + (self.cost_competitiveness * 0.4)


@dataclass
class RestockOrder:
    """
    Represents a restocking order recommendation.

    Attributes:
        order_id: Unique identifier for the order
        item_id: SKU of the item to restock
        quantity: Recommended quantity to order
        supplier_id: Recommended supplier
        estimated_cost: Estimated total cost
        delivery_route: Recommended delivery route
        priority: Order priority level
        estimated_delivery_date: When the order should arrive
        consolidation_group: Group ID for order consolidation
    """

    order_id: str
    item_id: str
    quantity: int
    supplier_id: str
    estimated_cost: float
    delivery_route: str
    priority: Priority
    estimated_delivery_date: Optional[datetime] = None
    consolidation_group: Optional[str] = None

    @property
    def cost_per_unit(self) -> float:
        """Calculate cost per unit for this order."""
        return self.estimated_cost / self.quantity if self.quantity > 0 else 0.0


class InventoryContext(BaseModel):
    """
    Context for inventory analysis containing all relevant data.

    This model serves as the input context for all agents and provides
    a complete view of the inventory system state.

    Attributes:
        items: List of all inventory items
        suppliers: List of all suppliers
        analysis_date: Date of the analysis
        region: Geographic region for the analysis
        total_locations: Total number of locations in the system
        budget_constraints: Optional budget limitations
        urgent_items: List of items requiring urgent attention
    """

    items: List[InventoryItem] = Field(
        ..., description="List of all inventory items to analyze"
    )
    suppliers: List[Supplier] = Field(
        default_factory=list, description="List of all available suppliers"
    )
    analysis_date: datetime = Field(
        default_factory=datetime.now, description="Date and time of the analysis"
    )
    region: str = Field(
        default="Multi-region", description="Geographic region for the analysis"
    )
    total_locations: int = Field(
        default=1, description="Total number of locations in the supply chain"
    )
    budget_constraints: Optional[float] = Field(
        None, description="Optional budget constraints for restocking"
    )
    urgent_items: List[str] = Field(
        default_factory=list, description="List of item IDs requiring urgent attention"
    )

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @field_validator("items")
    @classmethod
    def validate_items(cls, v: List[InventoryItem]) -> List[InventoryItem]:
        """Validate that items list is not empty."""
        if not v:
            raise ValueError("Items list cannot be empty")
        return v

    @property
    def total_items(self) -> int:
        """Get total number of items."""
        return len(self.items)

    @property
    def items_below_threshold(self) -> List[InventoryItem]:
        """Get all items below reorder threshold."""
        return [item for item in self.items if item.is_below_threshold]

    @property
    def critical_items(self) -> List[InventoryItem]:
        """Get all critically low stock items."""
        return [item for item in self.items if item.is_critical]

    @property
    def items_by_category(self) -> Dict[ProductCategory, List[InventoryItem]]:
        """Group items by product category."""
        categories: Dict[ProductCategory, List[InventoryItem]] = {}
        for item in self.items:
            if item.category not in categories:
                categories[item.category] = []
            categories[item.category].append(item)
        return categories

    @property
    def items_by_supplier(self) -> Dict[str, List[InventoryItem]]:
        """Group items by supplier."""
        suppliers: Dict[str, List[InventoryItem]] = {}
        for item in self.items:
            if item.supplier_id not in suppliers:
                suppliers[item.supplier_id] = []
            suppliers[item.supplier_id].append(item)
        return suppliers

    def get_summary_stats(self) -> Dict[str, Union[int, float]]:
        """
        Get summary statistics for the inventory context.

        Returns:
            Dictionary containing key metrics about the inventory
        """
        return {
            "total_items": self.total_items,
            "items_below_threshold": len(self.items_below_threshold),
            "critical_items": len(self.critical_items),
            "total_suppliers": len(set(item.supplier_id for item in self.items)),
            "total_stock_value": sum(
                item.current_stock * item.unit_cost for item in self.items
            ),
            "average_stock_level": (
                sum(item.current_stock for item in self.items) / self.total_items
                if self.total_items > 0
                else 0
            ),
            "categories": len(set(item.category for item in self.items)),
        }
