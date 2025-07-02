"""Shared utility functions and helpers for logistics agents."""

import uuid
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import pandas as pd


def format_currency(amount: float, currency: str = "USD") -> str:
    """
    Format a monetary amount as a currency string.

    Args:
        amount: The monetary amount to format
        currency: Currency code (default: USD)

    Returns:
        Formatted currency string

    Examples:
        >>> format_currency(1234.56)
        '$1,234.56'
        >>> format_currency(1000, "GBP")
        '£1,000.00'
    """

    # Currency symbols mapping
    currency_symbols = {
        "USD": "$",
        "GBP": "£",
        "EUR": "€",
        "INR": "₹"
    }

    symbol = currency_symbols.get(currency.upper(), currency)

    # Format with thousands separator and 2 decimal places
    if amount >= 0:
        return f"{symbol}{amount:,.2f}"
    else:
        return f"-{symbol}{abs(amount):,.2f}"


def calculate_percentage_change(old_value: float, new_value: float) -> float:
    """
    Calculate percentage change between two values.

    Args:
        old_value: Original value
        new_value: New value

    Returns:
        Percentage change (positive for increase, negative for decrease)

    Examples:
        >>> calculate_percentage_change(100, 120)
        20.0
        >>> calculate_percentage_change(200, 150)
        -25.0
    """

    if old_value == 0:
        return 0.0 if new_value == 0 else float('inf')

    return ((new_value - old_value) / old_value) * 100


def validate_csv_structure(
    csv_path: Path,
    required_columns: List[str]
) -> Dict[str, Any]:
    """
    Validate that a CSV file has the required structure and columns.

    Args:
        csv_path: Path to the CSV file
        required_columns: List of column names that must be present

    Returns:
        Dictionary with validation results containing:
        - is_valid: Boolean indicating if validation passed
        - missing_columns: List of missing required columns
        - extra_columns: List of columns not in required list
        - row_count: Number of data rows in the file
        - error_message: Error message if validation failed

    Examples:
        >>> result = validate_csv_structure(
        ...     Path("data.csv"), 
        ...     ["SKU", "Price", "Stock levels"]
        ... )
        >>> result["is_valid"]
        True
    """

    result = {
        "is_valid": False,
        "missing_columns": [],
        "extra_columns": [],
        "row_count": 0,
        "error_message": ""
    }

    try:
        # Check if file exists
        if not csv_path.exists():
            result["error_message"] = f"CSV file not found: {csv_path}"
            return result

        # Read CSV header
        df = pd.read_csv(csv_path, nrows=0)  # Read only header
        actual_columns = df.columns.tolist()

        # Check for missing columns
        missing = [col for col in required_columns if col not in actual_columns]
        result["missing_columns"] = missing

        # Check for extra columns
        extra = [col for col in actual_columns if col not in required_columns]
        result["extra_columns"] = extra

        # Count rows (excluding header)
        df_full = pd.read_csv(csv_path)
        result["row_count"] = len(df_full)

        # Validation passes if no missing columns
        if not missing:
            result["is_valid"] = True
        else:
            result["error_message"] = f"Missing required columns: {missing}"

    except Exception as e:
        result["error_message"] = f"Error reading CSV file: {str(e)}"

    return result


def generate_unique_id(prefix: str = "", length: int = 8) -> str:
    """
    Generate a unique identifier string.

    Args:
        prefix: Optional prefix for the ID
        length: Length of the random part (default: 8)

    Returns:
        Unique identifier string

    Examples:
        >>> generate_unique_id("ORDER")
        'ORDER_a1b2c3d4'
        >>> generate_unique_id()
        'a1b2c3d4'
    """

    # Generate random part using UUID
    random_part = str(uuid.uuid4()).replace("-", "")[:length]

    if prefix:
        return f"{prefix}_{random_part}"
    else:
        return random_part


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    Safely divide two numbers, returning a default value if division by zero.

    Args:
        numerator: Number to divide
        denominator: Number to divide by
        default: Value to return if denominator is zero

    Returns:
        Result of division or default value

    Examples:
        >>> safe_divide(10, 2)
        5.0
        >>> safe_divide(10, 0)
        0.0
        >>> safe_divide(10, 0, -1)
        -1.0
    """

    if denominator == 0:
        return default
    return numerator / denominator


def clean_string(text: str) -> str:
    """
    Clean and normalize a string for consistent processing.

    Args:
        text: String to clean

    Returns:
        Cleaned string with normalized whitespace and special characters

    Examples:
        >>> clean_string("  Hello   World!  ")
        'Hello World!'
        >>> clean_string("Product/Name (Special)")
        'Product Name Special'
    """

    if not isinstance(text, str):
        return str(text)

    # Remove extra whitespace
    cleaned = re.sub(r'\s+', ' ', text.strip())

    # Remove special characters but keep spaces, letters, numbers
    cleaned = re.sub(r'[^\w\s-]', ' ', cleaned)

    # Remove extra spaces again
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()

    return cleaned


def parse_numeric_string(value: str, default: float = 0.0) -> float:
    """
    Parse a string that might contain numeric data with various formats.

    Args:
        value: String to parse
        default: Default value if parsing fails

    Returns:
        Parsed numeric value or default

    Examples:
        >>> parse_numeric_string("$1,234.56")
        1234.56
        >>> parse_numeric_string("10.5%")
        10.5
        >>> parse_numeric_string("invalid")
        0.0
    """

    if not isinstance(value, str):
        try:
            return float(value)
        except (ValueError, TypeError):
            return default

    # Remove common non-numeric characters
    cleaned = re.sub(r'[$£€₹,\s%]', '', value)

    try:
        return float(cleaned)
    except ValueError:
        return default


def validate_date_string(date_string: str, format_string: str = "%Y-%m-%d") -> bool:
    """
    Validate if a string represents a valid date in the given format.

    Args:
        date_string: String to validate
        format_string: Expected date format (default: ISO format)

    Returns:
        True if valid date, False otherwise

    Examples:
        >>> validate_date_string("2025-01-15")
        True
        >>> validate_date_string("2025-13-45")
        False
        >>> validate_date_string("15/01/2025", "%d/%m/%Y")
        True
    """

    try:
        datetime.strptime(date_string, format_string)
        return True
    except ValueError:
        return False


def chunk_list(data: List[Any], chunk_size: int) -> List[List[Any]]:
    """
    Split a list into smaller chunks of specified size.

    Args:
        data: List to chunk
        chunk_size: Maximum size of each chunk

    Returns:
        List of chunks (sublists)

    Examples:
        >>> chunk_list([1, 2, 3, 4, 5], 2)
        [[1, 2], [3, 4], [5]]
        >>> chunk_list(['a', 'b', 'c', 'd'], 3)
        [['a', 'b', 'c'], ['d']]
    """

    if chunk_size <= 0:
        raise ValueError("Chunk size must be positive")

    return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]


def flatten_dict(
    nested_dict: Dict[str, Any],
    separator: str = ".",
    prefix: str = ""
) -> Dict[str, Any]:
    """
    Flatten a nested dictionary into a single-level dictionary.

    Args:
        nested_dict: Dictionary to flatten
        separator: String to use between nested keys
        prefix: Optional prefix for all keys

    Returns:
        Flattened dictionary

    Examples:
        >>> flatten_dict({"a": {"b": 1, "c": 2}, "d": 3})
        {'a.b': 1, 'a.c': 2, 'd': 3}
        >>> flatten_dict({"x": {"y": 4}}, separator="_", prefix="data")
        {'data_x_y': 4}
    """

    flattened = {}

    for key, value in nested_dict.items():
        new_key = f"{prefix}{separator}{key}" if prefix else key

        if isinstance(value, dict):
            # Recursively flatten nested dictionaries
            flattened.update(flatten_dict(value, separator, new_key))
        else:
            flattened[new_key] = value

    return flattened


def calculate_business_days(start_date: datetime, end_date: datetime) -> int:
    """
    Calculate the number of business days between two dates.

    Args:
        start_date: Starting date
        end_date: Ending date

    Returns:
        Number of business days (excluding weekends)

    Examples:
        >>> from datetime import datetime
        >>> start = datetime(2025, 1, 13)  # Monday
        >>> end = datetime(2025, 1, 17)    # Friday
        >>> calculate_business_days(start, end)
        4
    """

    if start_date > end_date:
        return 0

    # Use pandas for business day calculation
    business_days = pd.bdate_range(start_date, end_date)
    return len(business_days) - 1  # Exclude the start date


def format_file_size(size_bytes: int) -> str:
    """
    Format a file size in bytes as a human-readable string.

    Args:
        size_bytes: File size in bytes

    Returns:
        Formatted file size string

    Examples:
        >>> format_file_size(1024)
        '1.0 KB'
        >>> format_file_size(1536000)
        '1.5 MB'
        >>> format_file_size(2048576512)
        '1.9 GB'
    """

    if size_bytes == 0:
        return "0 B"

    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0

    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1

    return f"{size_bytes:.1f} {size_names[i]}"


def get_timestamp_string(
    include_microseconds: bool = False,
    use_utc: bool = False
) -> str:
    """
    Get a formatted timestamp string for logging or file naming.

    Args:
        include_microseconds: Whether to include microseconds in the timestamp
        use_utc: Whether to use UTC time instead of local time

    Returns:
        Formatted timestamp string

    Examples:
        >>> get_timestamp_string()
        '2025-01-16_14-30-45'
        >>> get_timestamp_string(include_microseconds=True)
        '2025-01-16_14-30-45-123456'
    """

    if use_utc:
        now = datetime.utcnow()
    else:
        now = datetime.now()

    if include_microseconds:
        return now.strftime("%Y-%m-%d_%H-%M-%S-%f")
    else:
        return now.strftime("%Y-%m-%d_%H-%M-%S")


class Timer:
    """
    Simple context manager for timing code execution.

    Usage:
        with Timer() as timer:
            # Some code to time
            pass
        print(f"Execution took {timer.elapsed:.2f} seconds")
    """

    def __init__(self):
        self.start_time = None
        self.end_time = None

    def __enter__(self):
        import time
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        import time
        self.end_time = time.time()

    @property
    def elapsed(self) -> float:
        """Get elapsed time in seconds."""
        if self.start_time is None:
            return 0.0

        end = self.end_time or time.time()
        return end - self.start_time


def retry_operation(
    operation,
    max_attempts: int = 3,
    delay_seconds: float = 1.0,
    exceptions: tuple = (Exception,)
) -> Any:
    """
    Retry an operation with exponential backoff.

    Args:
        operation: Function to retry
        max_attempts: Maximum number of attempts
        delay_seconds: Initial delay between attempts
        exceptions: Tuple of exceptions to catch and retry

    Returns:
        Result of the operation

    Raises:
        Last exception if all attempts fail
    """

    import time

    last_exception = None

    for attempt in range(max_attempts):
        try:
            return operation()
        except exceptions as e:
            last_exception = e

            if attempt < max_attempts - 1:
                # Exponential backoff
                wait_time = delay_seconds * (2 ** attempt)
                time.sleep(wait_time)
            else:
                # Last attempt failed
                raise last_exception

    # Should never reach here, but just in case
    raise last_exception or Exception("Operation failed after all retries")
