"""
Sidebar Component with Filters
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from datetime import datetime

from config import COLORS, MONTH_NAMES_SHORT


def create_sidebar(
    min_date=None,
    max_date=None,
    opd_list=None,
    payment_types=None,
    years=None,
    weeks=None
):
    """Create the sidebar with filter controls"""

    # Default values
    min_date = min_date or datetime.now().date()
    max_date = max_date or datetime.now().date()
    opd_list = opd_list or []
    payment_types = payment_types or ['Tunai', 'E-Samsat/Giro/Transfer', 'EDC', 'Virtual Account', 'QRIS']
    years = years or [datetime.now().year]
    weeks = weeks or list(range(1, 53))

    return html.Div([
        # Logo
        html.Div([
            html.Img(
                src='/assets/bapendajatim_logo.png',
                style={
                    'width': '100%',
                    'maxWidth': '200px',
                    'marginBottom': '1rem'
                }
            )
        ], style={'textAlign': 'center', 'padding': '1rem'}),

        html.Hr(style={'margin': '0 1rem 1rem 1rem', 'opacity': '0.2'}),

        # Filter header
        html.Div([
            html.H5([
                html.I(className='fas fa-filter me-2'),
                "Filter Data"
            ], style={
                'color': COLORS['primary'],
                'fontWeight': '700',
                'marginBottom': '1.5rem'
            })
        ], style={'padding': '0 1rem'}),

        # Period filter
        html.Div([
            dbc.Label([
                html.I(className='fas fa-calendar-alt me-2', style={'color': COLORS['primary']}),
                "Periode Waktu"
            ], style={
                'fontWeight': '600',
                'color': COLORS['text_primary'],
                'marginBottom': '0.5rem'
            }),
            dcc.Dropdown(
                id='period-type-dropdown',
                options=[
                    {'label': 'Semua Data', 'value': 'Semua Data'},
                    {'label': 'Harian', 'value': 'Harian'},
                    {'label': 'Mingguan', 'value': 'Mingguan'},
                    {'label': 'Bulanan', 'value': 'Bulanan'},
                    {'label': 'Tahunan', 'value': 'Tahunan'},
                    {'label': 'Rentang Tanggal', 'value': 'Rentang Tanggal'},
                ],
                value='Semua Data',
                clearable=False,
                style={'marginBottom': '1rem'}
            ),

            # Dynamic period selector container
            html.Div(id='period-selector-container'),

        ], style={'padding': '0 1rem', 'marginBottom': '1.5rem'}),

        html.Hr(style={'margin': '0 1rem 1rem 1rem', 'opacity': '0.2'}),

        # OPD filter
        html.Div([
            dbc.Label([
                html.I(className='fas fa-building me-2', style={'color': COLORS['secondary']}),
                "Perangkat Daerah"
            ], style={
                'fontWeight': '600',
                'color': COLORS['text_primary'],
                'marginBottom': '0.5rem'
            }),
            dcc.Dropdown(
                id='opd-dropdown',
                options=[{'label': 'Semua OPD', 'value': 'Semua OPD'}] +
                        [{'label': opd, 'value': opd} for opd in opd_list],
                value=['Semua OPD'],
                multi=True,
                placeholder='Pilih OPD...',
                style={'marginBottom': '1rem'}
            ),
        ], style={'padding': '0 1rem', 'marginBottom': '1.5rem'}),

        html.Hr(style={'margin': '0 1rem 1rem 1rem', 'opacity': '0.2'}),

        # Payment type filter
        html.Div([
            dbc.Label([
                html.I(className='fas fa-credit-card me-2', style={'color': COLORS['gold']}),
                "Jenis Pembayaran"
            ], style={
                'fontWeight': '600',
                'color': COLORS['text_primary'],
                'marginBottom': '0.5rem'
            }),
            dcc.Dropdown(
                id='payment-dropdown',
                options=[{'label': 'Semua', 'value': 'Semua'}] +
                        [{'label': pt, 'value': pt} for pt in payment_types],
                value='Semua',
                clearable=False,
                style={'marginBottom': '1rem'}
            ),
        ], style={'padding': '0 1rem', 'marginBottom': '1.5rem'}),

        html.Hr(style={'margin': '0 1rem 1rem 1rem', 'opacity': '0.2'}),

        # Refresh controls
        html.Div([
            dbc.Label([
                html.I(className='fas fa-sync-alt me-2', style={'color': COLORS['accent']}),
                "Auto Refresh"
            ], style={
                'fontWeight': '600',
                'color': COLORS['text_primary'],
                'marginBottom': '0.5rem'
            }),
            dbc.Switch(
                id='auto-refresh-switch',
                label='Aktif (30 detik)',
                value=True,
                style={'marginBottom': '1rem'}
            ),
            dbc.Button([
                html.I(className='fas fa-sync me-2'),
                "Refresh Sekarang"
            ],
                id='manual-refresh-button',
                color='primary',
                outline=True,
                size='sm',
                className='w-100',
                style={'borderRadius': '8px'}
            ),
        ], style={'padding': '0 1rem', 'marginBottom': '1.5rem'}),

        # Data info
        html.Div([
            html.Hr(style={'margin': '1rem 0', 'opacity': '0.2'}),
            html.Div([
                html.I(className='fas fa-info-circle me-2', style={'color': COLORS['accent']}),
                html.Span("Data Info", style={'fontWeight': '600'})
            ], style={'marginBottom': '0.5rem'}),
            html.P(id='data-info-text', style={
                'fontSize': '0.85rem',
                'color': COLORS['text_secondary'],
                'marginBottom': '0'
            }),
            html.P(id='last-update-text', style={
                'fontSize': '0.8rem',
                'color': COLORS['text_secondary'],
                'marginBottom': '0'
            }),
        ], style={'padding': '0 1rem', 'marginBottom': '1rem'}),

    ], style={
        'background': f'linear-gradient(180deg, {COLORS["light_bg"]} 0%, {COLORS["white"]} 100%)',
        'minHeight': '100vh',
        'borderRight': f'1px solid {COLORS["border"]}',
        'paddingTop': '0.5rem'
    })


def create_period_selector(
    period_type,
    min_date,
    max_date,
    years,
    weeks
):
    """Create dynamic period selector based on period type"""

    if period_type == 'Harian':
        return html.Div([
            dbc.Label("Pilih Tanggal", style={'fontSize': '0.9rem'}),
            dcc.DatePickerSingle(
                id='date-picker-single',
                min_date_allowed=min_date,
                max_date_allowed=max_date,
                date=max_date,
                display_format='DD/MM/YYYY',
                style={'width': '100%'}
            )
        ])

    elif period_type == 'Mingguan':
        return html.Div([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Minggu", style={'fontSize': '0.9rem'}),
                    dcc.Dropdown(
                        id='week-dropdown',
                        options=[{'label': f'Minggu {w}', 'value': w} for w in weeks],
                        value=weeks[-1] if weeks else 1,
                        clearable=False
                    )
                ], width=6),
                dbc.Col([
                    dbc.Label("Tahun", style={'fontSize': '0.9rem'}),
                    dcc.Dropdown(
                        id='year-dropdown-week',
                        options=[{'label': str(y), 'value': y} for y in years],
                        value=years[0] if years else datetime.now().year,
                        clearable=False
                    )
                ], width=6)
            ])
        ])

    elif period_type == 'Bulanan':
        return html.Div([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Bulan", style={'fontSize': '0.9rem'}),
                    dcc.Dropdown(
                        id='month-dropdown',
                        options=[{'label': v, 'value': k} for k, v in MONTH_NAMES_SHORT.items()],
                        value=datetime.now().month,
                        clearable=False
                    )
                ], width=6),
                dbc.Col([
                    dbc.Label("Tahun", style={'fontSize': '0.9rem'}),
                    dcc.Dropdown(
                        id='year-dropdown-month',
                        options=[{'label': str(y), 'value': y} for y in years],
                        value=years[0] if years else datetime.now().year,
                        clearable=False
                    )
                ], width=6)
            ])
        ])

    elif period_type == 'Tahunan':
        return html.Div([
            dbc.Label("Pilih Tahun", style={'fontSize': '0.9rem'}),
            dcc.Dropdown(
                id='year-dropdown',
                options=[{'label': str(y), 'value': y} for y in years],
                value=years[0] if years else datetime.now().year,
                clearable=False
            )
        ])

    elif period_type == 'Rentang Tanggal':
        return html.Div([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Dari", style={'fontSize': '0.9rem'}),
                    dcc.DatePickerSingle(
                        id='date-picker-start',
                        min_date_allowed=min_date,
                        max_date_allowed=max_date,
                        date=min_date,
                        display_format='DD/MM/YYYY'
                    )
                ], width=6),
                dbc.Col([
                    dbc.Label("Sampai", style={'fontSize': '0.9rem'}),
                    dcc.DatePickerSingle(
                        id='date-picker-end',
                        min_date_allowed=min_date,
                        max_date_allowed=max_date,
                        date=max_date,
                        display_format='DD/MM/YYYY'
                    )
                ], width=6)
            ])
        ])

    else:
        return html.Div()
