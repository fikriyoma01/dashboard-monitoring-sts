"""
Card Components - Metric Cards and Info Boxes
"""

from dash import html
import dash_bootstrap_components as dbc

from config import COLORS
from utils.formatters import format_rupiah_short, format_number


def create_metric_card(
    title: str,
    value: str,
    icon: str,
    color: str = 'primary',
    subtitle: str = None
):
    """
    Create a single metric card

    Args:
        title: Card title
        value: Main value to display
        icon: FontAwesome icon class
        color: Color key from COLORS dict
        subtitle: Optional subtitle text
    """
    color_map = {
        'primary': COLORS['primary'],
        'secondary': COLORS['secondary'],
        'gold': COLORS['gold'],
        'accent': COLORS['accent'],
        'success': COLORS['success'],
        'warning': COLORS['warning'],
        'danger': COLORS['danger'],
    }

    border_color = color_map.get(color, COLORS['primary'])

    return dbc.Card([
        dbc.CardBody([
            html.Div([
                # Icon
                html.Div([
                    html.I(className=f'fas {icon}', style={
                        'fontSize': '2rem',
                        'color': border_color,
                        'opacity': '0.8'
                    })
                ], style={'marginBottom': '0.75rem'}),

                # Value
                html.H3(
                    value,
                    style={
                        'color': COLORS['dark'],
                        'fontWeight': '700',
                        'fontSize': '1.75rem',
                        'marginBottom': '0.25rem',
                        'letterSpacing': '-0.5px'
                    }
                ),

                # Title
                html.P(
                    title,
                    style={
                        'color': COLORS['text_secondary'],
                        'fontSize': '0.95rem',
                        'fontWeight': '500',
                        'marginBottom': '0'
                    }
                ),

                # Subtitle (optional)
                html.P(
                    subtitle,
                    style={
                        'color': COLORS['text_secondary'],
                        'fontSize': '0.8rem',
                        'marginBottom': '0',
                        'marginTop': '0.25rem'
                    }
                ) if subtitle else None,
            ])
        ], style={'padding': '1.25rem'})
    ], style={
        'background': f'linear-gradient(145deg, {COLORS["white"]} 0%, {COLORS["light_bg"]} 100%)',
        'borderRadius': '12px',
        'boxShadow': '0 3px 12px rgba(0,0,0,0.08)',
        'borderLeft': f'5px solid {border_color}',
        'transition': 'transform 0.2s, box-shadow 0.2s',
        'border': 'none'
    }, className='metric-card h-100')


def create_metric_cards(metrics: dict):
    """
    Create all metric cards

    Args:
        metrics: Dictionary with metric values
            - total_penerimaan
            - jumlah_sts
            - rata_rata
            - jumlah_opd
    """
    return dbc.Row([
        dbc.Col([
            create_metric_card(
                title='Total Penerimaan',
                value=format_rupiah_short(metrics.get('total_penerimaan', 0)),
                icon='fa-money-bill-wave',
                color='primary'
            )
        ], width=12, md=6, lg=3, className='mb-3'),

        dbc.Col([
            create_metric_card(
                title='Jumlah STS',
                value=format_number(metrics.get('jumlah_sts', 0)),
                icon='fa-file-invoice',
                color='secondary'
            )
        ], width=12, md=6, lg=3, className='mb-3'),

        dbc.Col([
            create_metric_card(
                title='Rata-rata per STS',
                value=format_rupiah_short(metrics.get('rata_rata', 0)),
                icon='fa-chart-bar',
                color='gold'
            )
        ], width=12, md=6, lg=3, className='mb-3'),

        dbc.Col([
            create_metric_card(
                title='Perangkat Daerah',
                value=format_number(metrics.get('jumlah_opd', 0)),
                icon='fa-landmark',
                color='accent'
            )
        ], width=12, md=6, lg=3, className='mb-3'),
    ], className='mb-2')


def create_info_box(
    period_label: str,
    total_transactions: int,
    total_opd: int,
    date_range: str
):
    """
    Create the info box showing current filter info

    Args:
        period_label: Current period label
        total_transactions: Total number of transactions
        total_opd: Total number of OPD
        date_range: Date range string
    """
    return html.Div([
        dbc.Row([
            # Period
            dbc.Col([
                html.Div([
                    html.I(className='fas fa-calendar-alt', style={
                        'fontSize': '1.5rem',
                        'color': COLORS['primary'],
                        'marginRight': '0.75rem'
                    }),
                    html.Div([
                        html.Span('Periode', style={
                            'fontSize': '0.85rem',
                            'color': COLORS['text_secondary'],
                            'display': 'block'
                        }),
                        html.Span(period_label, style={
                            'fontSize': '1rem',
                            'fontWeight': '700',
                            'color': COLORS['primary']
                        })
                    ])
                ], style={'display': 'flex', 'alignItems': 'center'})
            ], width=12, md=3, className='mb-2 mb-md-0'),

            # Total Transactions
            dbc.Col([
                html.Div([
                    html.I(className='fas fa-receipt', style={
                        'fontSize': '1.5rem',
                        'color': COLORS['secondary'],
                        'marginRight': '0.75rem'
                    }),
                    html.Div([
                        html.Span('Total Transaksi', style={
                            'fontSize': '0.85rem',
                            'color': COLORS['text_secondary'],
                            'display': 'block'
                        }),
                        html.Span(format_number(total_transactions), style={
                            'fontSize': '1rem',
                            'fontWeight': '700',
                            'color': COLORS['primary']
                        })
                    ])
                ], style={'display': 'flex', 'alignItems': 'center'})
            ], width=12, md=3, className='mb-2 mb-md-0'),

            # Total OPD
            dbc.Col([
                html.Div([
                    html.I(className='fas fa-building', style={
                        'fontSize': '1.5rem',
                        'color': COLORS['gold'],
                        'marginRight': '0.75rem'
                    }),
                    html.Div([
                        html.Span('Jumlah OPD', style={
                            'fontSize': '0.85rem',
                            'color': COLORS['text_secondary'],
                            'display': 'block'
                        }),
                        html.Span(str(total_opd), style={
                            'fontSize': '1rem',
                            'fontWeight': '700',
                            'color': COLORS['primary']
                        })
                    ])
                ], style={'display': 'flex', 'alignItems': 'center'})
            ], width=12, md=3, className='mb-2 mb-md-0'),

            # Date Range
            dbc.Col([
                html.Div([
                    html.I(className='fas fa-clock', style={
                        'fontSize': '1.5rem',
                        'color': COLORS['accent'],
                        'marginRight': '0.75rem'
                    }),
                    html.Div([
                        html.Span('Rentang Data', style={
                            'fontSize': '0.85rem',
                            'color': COLORS['text_secondary'],
                            'display': 'block'
                        }),
                        html.Span(date_range, style={
                            'fontSize': '1rem',
                            'fontWeight': '700',
                            'color': COLORS['primary']
                        })
                    ])
                ], style={'display': 'flex', 'alignItems': 'center'})
            ], width=12, md=3),
        ], className='align-items-center')
    ], style={
        'background': f'linear-gradient(135deg, {COLORS["light_bg"]} 0%, #E6F3FF 100%)',
        'border': f'1px solid rgba(0, 181, 239, 0.3)',
        'borderRadius': '10px',
        'padding': '1rem 1.5rem',
        'marginBottom': '1.25rem'
    })


def create_section_header(title: str, icon: str = None):
    """
    Create a section header

    Args:
        title: Section title
        icon: Optional FontAwesome icon class
    """
    return html.Div([
        html.I(className=f'fas {icon} me-2') if icon else None,
        title
    ], style={
        'background': f'linear-gradient(90deg, {COLORS["primary"]} 0%, {COLORS["accent"]} 100%)',
        'color': COLORS['white'],
        'padding': '0.875rem 1.25rem',
        'borderRadius': '8px',
        'fontWeight': '600',
        'fontSize': '1.1rem',
        'marginBottom': '1rem',
        'display': 'flex',
        'alignItems': 'center'
    })


def create_chart_container(children, title: str = None):
    """
    Create a container for charts

    Args:
        children: Chart component(s)
        title: Optional title
    """
    content = []

    if title:
        content.append(create_section_header(title))

    content.append(
        html.Div(
            children,
            style={
                'background': COLORS['white'],
                'borderRadius': '12px',
                'padding': '1.25rem',
                'boxShadow': '0 3px 10px rgba(0,0,0,0.06)'
            }
        )
    )

    return html.Div(content, className='mb-4')
