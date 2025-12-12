"""
Formatting utilities for the dashboard
"""

import pandas as pd
from config import MONTH_NAMES, MONTH_NAMES_SHORT, DAY_NAMES


def format_rupiah(value, prefix: str = "Rp ") -> str:
    """
    Format number as Indonesian Rupiah (full format)

    Args:
        value: Number to format
        prefix: Currency prefix (default: "Rp ")

    Returns:
        Formatted string like "Rp 1.234.567"
    """
    if pd.isna(value) or value is None:
        return f"{prefix}0"

    try:
        value = float(value)
        formatted = f"{value:,.0f}".replace(",", ".")
        return f"{prefix}{formatted}"
    except (ValueError, TypeError):
        return f"{prefix}0"


def format_rupiah_short(value, prefix: str = "Rp ") -> str:
    """
    Format number as shortened Rupiah

    Args:
        value: Number to format
        prefix: Currency prefix (default: "Rp ")

    Returns:
        Formatted string like "Rp 1.23 T" or "Rp 456 M" or "Rp 789 Jt"
    """
    if pd.isna(value) or value is None:
        return f"{prefix}0"

    try:
        value = float(value)

        if abs(value) >= 1e12:
            return f"{prefix}{value/1e12:.2f} T"
        elif abs(value) >= 1e9:
            return f"{prefix}{value/1e9:.2f} M"
        elif abs(value) >= 1e6:
            return f"{prefix}{value/1e6:.1f} Jt"
        elif abs(value) >= 1e3:
            return f"{prefix}{value/1e3:.1f} Rb"
        else:
            return f"{prefix}{value:,.0f}".replace(",", ".")

    except (ValueError, TypeError):
        return f"{prefix}0"


def format_number(value, decimal_places: int = 0) -> str:
    """
    Format number with thousand separators (Indonesian style)

    Args:
        value: Number to format
        decimal_places: Number of decimal places

    Returns:
        Formatted string like "1.234.567"
    """
    if pd.isna(value) or value is None:
        return "0"

    try:
        value = float(value)
        if decimal_places > 0:
            formatted = f"{value:,.{decimal_places}f}"
        else:
            formatted = f"{value:,.0f}"
        return formatted.replace(",", ".")
    except (ValueError, TypeError):
        return "0"


def format_percentage(value, decimal_places: int = 1) -> str:
    """
    Format number as percentage

    Args:
        value: Number to format (0-100)
        decimal_places: Number of decimal places

    Returns:
        Formatted string like "12.5%"
    """
    if pd.isna(value) or value is None:
        return "0%"

    try:
        value = float(value)
        return f"{value:.{decimal_places}f}%"
    except (ValueError, TypeError):
        return "0%"


def format_date(date, format_str: str = "%d/%m/%Y") -> str:
    """
    Format date to Indonesian format

    Args:
        date: Date object or string
        format_str: Date format string

    Returns:
        Formatted date string
    """
    if pd.isna(date) or date is None:
        return "-"

    try:
        if isinstance(date, str):
            date = pd.to_datetime(date)
        return date.strftime(format_str)
    except Exception:
        return "-"


def format_date_long(date) -> str:
    """
    Format date to long Indonesian format (e.g., "12 Januari 2025")

    Args:
        date: Date object

    Returns:
        Formatted date string
    """
    if pd.isna(date) or date is None:
        return "-"

    try:
        if isinstance(date, str):
            date = pd.to_datetime(date)

        day = date.day
        month = MONTH_NAMES.get(date.month, date.strftime("%B"))
        year = date.year

        return f"{day} {month} {year}"
    except Exception:
        return "-"


def format_datetime(dt, format_str: str = "%d/%m/%Y %H:%M") -> str:
    """
    Format datetime to Indonesian format

    Args:
        dt: Datetime object
        format_str: Datetime format string

    Returns:
        Formatted datetime string
    """
    if pd.isna(dt) or dt is None:
        return "-"

    try:
        if isinstance(dt, str):
            dt = pd.to_datetime(dt)
        return dt.strftime(format_str)
    except Exception:
        return "-"


def get_month_name(month_number: int, short: bool = False) -> str:
    """
    Get Indonesian month name from month number

    Args:
        month_number: Month number (1-12)
        short: Use short form (default: False)

    Returns:
        Month name in Indonesian
    """
    if short:
        return MONTH_NAMES_SHORT.get(month_number, str(month_number))
    return MONTH_NAMES.get(month_number, str(month_number))


def get_day_name(day_name_en: str) -> str:
    """
    Get Indonesian day name from English day name

    Args:
        day_name_en: English day name

    Returns:
        Day name in Indonesian
    """
    return DAY_NAMES.get(day_name_en, day_name_en)


def truncate_text(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """
    Truncate text to specified length

    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated

    Returns:
        Truncated text
    """
    if pd.isna(text) or text is None:
        return ""

    text = str(text).strip()
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def scale_value(value):
    """
    Determine appropriate scale for value display

    Args:
        value: Numeric value

    Returns:
        Tuple of (scale_factor, suffix, label)
    """
    if pd.isna(value) or value is None:
        value = 0

    try:
        value = float(value)

        if value >= 1e12:
            return (1e12, ' T', '(Rp dalam Triliun)')
        elif value >= 1e9:
            return (1e9, ' M', '(Rp dalam Milyar)')
        elif value >= 1e6:
            return (1e6, ' Jt', '(Rp dalam Juta)')
        else:
            return (1, '', '(Rp)')
    except (ValueError, TypeError):
        return (1, '', '(Rp)')
