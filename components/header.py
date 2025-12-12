"""
Header Component
"""

from dash import html
import dash_bootstrap_components as dbc

from config import COLORS


def create_header(user_info: dict = None):
    """Create the dashboard header"""
    username = user_info.get('nama_lengkap', 'User') if user_info else 'User'

    return html.Div([
        dbc.Row([
            # Logo and title
            dbc.Col([
                html.Div([
                    # Logo
                    html.Img(
                        src='/assets/logo_jawa-timur.svg',
                        style={
                            'height': '60px',
                            'width': 'auto',
                            'marginRight': '1rem'
                        }
                    ),
                    # Title text
                    html.Div([
                        html.H1([
                            html.I(className='fas fa-chart-line me-2'),
                            "MONITORING PENERIMAAN RETRIBUSI & PAD"
                        ], style={
                            'color': COLORS['white'],
                            'fontSize': '1.5rem',
                            'fontWeight': '700',
                            'marginBottom': '0.25rem',
                            'letterSpacing': '-0.3px'
                        }),
                        html.P(
                            "Surat Tanda Setoran (STS)",
                            style={
                                'color': COLORS['accent'],
                                'fontSize': '1rem',
                                'marginBottom': '0.15rem',
                                'fontWeight': '500'
                            }
                        ),
                        html.P(
                            "BADAN PENDAPATAN DAERAH PROVINSI JAWA TIMUR",
                            style={
                                'color': COLORS['gold'],
                                'fontSize': '0.85rem',
                                'fontWeight': '600',
                                'letterSpacing': '0.5px',
                                'marginBottom': '0'
                            }
                        ),
                    ])
                ], style={
                    'display': 'flex',
                    'alignItems': 'center'
                })
            ], width=9),

            # User info and logout
            dbc.Col([
                html.Div([
                    html.Div([
                        html.I(className='fas fa-user-circle', style={
                            'fontSize': '2rem',
                            'color': COLORS['accent'],
                            'marginRight': '0.75rem'
                        }),
                        html.Div([
                            html.P(username, style={
                                'color': COLORS['white'],
                                'fontWeight': '600',
                                'fontSize': '0.95rem',
                                'marginBottom': '0'
                            }),
                            html.P('Administrator', style={
                                'color': COLORS['accent'],
                                'fontSize': '0.8rem',
                                'marginBottom': '0'
                            }),
                        ])
                    ], style={
                        'display': 'flex',
                        'alignItems': 'center',
                        'marginBottom': '0.5rem'
                    }),
                    dbc.Button([
                        html.I(className='fas fa-sign-out-alt me-2'),
                        "Logout"
                    ],
                        id='logout-button',
                        color='light',
                        size='sm',
                        outline=True,
                        style={
                            'borderRadius': '20px',
                            'padding': '0.4rem 1rem',
                            'fontSize': '0.85rem'
                        }
                    )
                ], style={
                    'textAlign': 'right',
                    'display': 'flex',
                    'flexDirection': 'column',
                    'alignItems': 'flex-end'
                })
            ], width=3)
        ], className='align-items-center')
    ], style={
        'background': f'linear-gradient(135deg, {COLORS["primary"]} 0%, {COLORS["dark"]} 100%)',
        'padding': '1.25rem 1.5rem',
        'borderRadius': '12px',
        'marginBottom': '1.25rem',
        'boxShadow': f'0 4px 15px {COLORS["primary"]}40'
    })
