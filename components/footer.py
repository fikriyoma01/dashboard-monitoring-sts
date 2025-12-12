"""
Footer Component
"""

from dash import html
import dash_bootstrap_components as dbc
from datetime import datetime

from config import COLORS


def create_footer():
    """Create the dashboard footer"""
    return html.Footer([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.I(className='fas fa-chart-line me-2'),
                    html.Span(
                        "Aplikasi Monitoring STS - Retribusi & PAD",
                        style={'fontWeight': '600', 'fontSize': '1.1rem'}
                    )
                ], style={
                    'color': COLORS['gold'],
                    'marginBottom': '0.5rem'
                }),
                html.P(
                    "Badan Pendapatan Daerah Provinsi Jawa Timur",
                    style={
                        'color': '#ccc',
                        'marginBottom': '0.25rem',
                        'fontSize': '0.95rem'
                    }
                ),
                html.P([
                    html.I(className='far fa-copyright me-1'),
                    f" {datetime.now().year} BAPENDA Jatim. All Rights Reserved."
                ], style={
                    'color': '#999',
                    'marginBottom': '0',
                    'fontSize': '0.85rem'
                })
            ], width=12, md=6, className='text-center text-md-start mb-3 mb-md-0'),

            dbc.Col([
                html.Div([
                    html.Span(
                        "Powered by",
                        style={'color': '#999', 'fontSize': '0.8rem', 'marginRight': '0.5rem'}
                    ),
                    html.Span(
                        "Dash + Plotly",
                        style={'color': COLORS['accent'], 'fontWeight': '600', 'fontSize': '0.9rem'}
                    )
                ], style={'marginBottom': '0.5rem'}),
                html.Div([
                    html.A([
                        html.I(className='fas fa-globe me-1'),
                        "bapenda.jatimprov.go.id"
                    ],
                        href='https://bapenda.jatimprov.go.id',
                        target='_blank',
                        style={
                            'color': COLORS['accent'],
                            'textDecoration': 'none',
                            'fontSize': '0.85rem'
                        }
                    )
                ])
            ], width=12, md=6, className='text-center text-md-end'),
        ], className='align-items-center')
    ], style={
        'background': f'linear-gradient(135deg, {COLORS["dark"]} 0%, {COLORS["primary"]} 100%)',
        'color': COLORS['white'],
        'padding': '1.5rem 2rem',
        'borderRadius': '12px',
        'marginTop': '2rem'
    })


def create_mini_footer():
    """Create a minimal footer for smaller screens or modals"""
    return html.Div([
        html.Small([
            html.I(className='far fa-copyright me-1'),
            f" {datetime.now().year} BAPENDA Jatim"
        ], style={'color': COLORS['text_secondary']})
    ], style={'textAlign': 'center', 'padding': '1rem'})
