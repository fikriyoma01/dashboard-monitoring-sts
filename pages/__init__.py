"""
Pages package
"""

from .dashboard import create_dashboard_layout, register_callbacks
from .data_detail import create_detail_layout

__all__ = [
    'create_dashboard_layout', 'register_callbacks',
    'create_detail_layout'
]
