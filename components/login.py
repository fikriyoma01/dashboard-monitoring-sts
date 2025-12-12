"""
Login Page Component
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from datetime import datetime
import os

from config import COLORS, ASSETS_DIR


def create_login_layout():
    """Create the login page layout"""
    return html.Div([
        # Background
        html.Div(
            style={
                'position': 'fixed',
                'top': 0,
                'left': 0,
                'right': 0,
                'bottom': 0,
                'background': f'linear-gradient(135deg, {COLORS["primary"]} 0%, {COLORS["dark"]} 50%, {COLORS["primary_dark"]} 100%)',
                'zIndex': -1
            }
        ),

        # Floating shapes for visual interest
        html.Div([
            html.Div(style={
                'position': 'absolute',
                'width': '300px',
                'height': '300px',
                'borderRadius': '50%',
                'background': f'rgba(255,255,255,0.05)',
                'top': '10%',
                'left': '5%',
            }),
            html.Div(style={
                'position': 'absolute',
                'width': '200px',
                'height': '200px',
                'borderRadius': '50%',
                'background': f'rgba(255,255,255,0.03)',
                'bottom': '15%',
                'right': '10%',
            }),
            html.Div(style={
                'position': 'absolute',
                'width': '150px',
                'height': '150px',
                'borderRadius': '50%',
                'background': f'rgba(212, 175, 55, 0.1)',
                'top': '60%',
                'left': '15%',
            }),
        ], style={'position': 'fixed', 'top': 0, 'left': 0, 'right': 0, 'bottom': 0, 'overflow': 'hidden', 'zIndex': -1}),

        # Login card container
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    # Login card
                    dbc.Card([
                        dbc.CardBody([
                            # Logo
                            html.Div([
                                html.Img(
                                    src='/assets/logo_jawa-timur.svg',
                                    style={
                                        'width': '100px',
                                        'height': 'auto',
                                        'marginBottom': '1rem'
                                    }
                                ),
                            ], style={'textAlign': 'center'}),

                            # Title
                            html.Div([
                                html.H2([
                                    html.I(className='fas fa-lock me-2'),
                                    "Login Sistem"
                                ], style={
                                    'color': COLORS['primary'],
                                    'fontWeight': '700',
                                    'marginBottom': '0.5rem',
                                    'fontSize': '1.75rem'
                                }),
                                html.P(
                                    "Monitoring STS - Retribusi & PAD",
                                    style={
                                        'color': COLORS['text_secondary'],
                                        'fontSize': '1rem',
                                        'marginBottom': '0.25rem'
                                    }
                                ),
                                html.P(
                                    "BAPENDA JAWA TIMUR",
                                    style={
                                        'color': COLORS['gold'],
                                        'fontSize': '0.9rem',
                                        'fontWeight': '600',
                                        'letterSpacing': '0.5px'
                                    }
                                ),
                            ], style={'textAlign': 'center', 'marginBottom': '2rem'}),

                            # Error message
                            dbc.Alert(
                                id='login-error',
                                color='danger',
                                style={'display': 'none'},
                                className='mb-3'
                            ),

                            # Login form
                            html.Div([
                                # Username
                                dbc.Label([
                                    html.I(className='fas fa-user me-2'),
                                    "Username"
                                ], style={
                                    'fontWeight': '600',
                                    'color': COLORS['text_primary'],
                                    'marginBottom': '0.5rem'
                                }),
                                dbc.Input(
                                    id='username-input',
                                    type='text',
                                    placeholder='Masukkan username',
                                    className='mb-3',
                                    style={
                                        'padding': '0.75rem 1rem',
                                        'borderRadius': '8px',
                                        'border': f'1px solid {COLORS["border"]}',
                                        'fontSize': '1rem'
                                    }
                                ),

                                # Password
                                dbc.Label([
                                    html.I(className='fas fa-key me-2'),
                                    "Password"
                                ], style={
                                    'fontWeight': '600',
                                    'color': COLORS['text_primary'],
                                    'marginBottom': '0.5rem'
                                }),
                                dbc.Input(
                                    id='password-input',
                                    type='password',
                                    placeholder='Masukkan password',
                                    className='mb-4',
                                    style={
                                        'padding': '0.75rem 1rem',
                                        'borderRadius': '8px',
                                        'border': f'1px solid {COLORS["border"]}',
                                        'fontSize': '1rem'
                                    }
                                ),

                                # Login button
                                dbc.Button([
                                    html.I(className='fas fa-sign-in-alt me-2'),
                                    "Masuk"
                                ],
                                    id='login-button',
                                    color='primary',
                                    className='w-100',
                                    size='lg',
                                    style={
                                        'padding': '0.875rem',
                                        'fontWeight': '600',
                                        'borderRadius': '8px',
                                        'background': f'linear-gradient(135deg, {COLORS["primary"]} 0%, {COLORS["primary_dark"]} 100%)',
                                        'border': 'none',
                                        'boxShadow': f'0 4px 15px {COLORS["primary"]}40'
                                    }
                                ),
                            ]),

                            # Footer
                            html.Div([
                                html.Hr(style={'margin': '2rem 0 1.5rem 0', 'opacity': '0.2'}),
                                html.P([
                                    html.I(className='far fa-copyright me-1'),
                                    f" {datetime.now().year} Badan Pendapatan Daerah"
                                ], style={
                                    'color': COLORS['text_secondary'],
                                    'fontSize': '0.85rem',
                                    'marginBottom': '0.25rem'
                                }),
                                html.P(
                                    "Provinsi Jawa Timur",
                                    style={
                                        'color': COLORS['text_secondary'],
                                        'fontSize': '0.85rem',
                                        'marginBottom': '0'
                                    }
                                ),
                            ], style={'textAlign': 'center'}),

                        ], style={'padding': '2.5rem'})
                    ], style={
                        'borderRadius': '20px',
                        'boxShadow': '0 20px 60px rgba(0,0,0,0.3)',
                        'border': 'none',
                        'background': f'linear-gradient(145deg, {COLORS["white"]} 0%, {COLORS["light_bg"]} 100%)',
                        'maxWidth': '420px',
                        'margin': '0 auto'
                    })
                ], width=12, md=6, lg=5, xl=4)
            ], className='justify-content-center align-items-center', style={'minHeight': '100vh'})
        ], fluid=True)
    ], style={'minHeight': '100vh', 'fontFamily': "'Plus Jakarta Sans', sans-serif"})
