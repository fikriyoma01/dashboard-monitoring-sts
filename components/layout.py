"""
Main Layout Component
"""

from dash import html, dcc
import dash_bootstrap_components as dbc

from config import COLORS


def create_main_layout():
    """Create the main dashboard layout"""
    from pages.dashboard import create_dashboard_layout
    return create_dashboard_layout()


def create_content_wrapper(children):
    """Wrap content with standard styling"""
    return html.Div(
        children,
        style={
            'padding': '1.5rem',
            'backgroundColor': COLORS['light_bg'],
            'minHeight': '100vh'
        }
    )
