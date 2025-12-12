"""
Monitoring STS Dashboard - BAPENDA Jawa Timur
Main Dash Application
"""

import dash
from dash import Dash, html, dcc, Input, Output, State, callback, no_update
import dash_bootstrap_components as dbc
from flask import Flask, session
import os
import uuid
from datetime import datetime

from config import (
    APP_NAME, DEBUG, HOST, PORT, SECRET_KEY, COLORS,
    AUTO_REFRESH_INTERVAL, ENABLE_AUTO_REFRESH
)

# Initialize Flask server
server = Flask(__name__)
server.secret_key = SECRET_KEY

# Initialize Dash app with Bootstrap theme
app = Dash(
    __name__,
    server=server,
    suppress_callback_exceptions=True,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        dbc.icons.FONT_AWESOME,
        'https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap'
    ],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
        {"name": "description", "content": "Dashboard Monitoring STS - BAPENDA Jawa Timur"},
    ],
    title=APP_NAME,
    update_title='Memuat...'
)

# Import components and pages after app initialization
from components.layout import create_main_layout
from components.login import create_login_layout
from pages.dashboard import register_callbacks as register_dashboard_callbacks
from pages.data_detail import register_callbacks as register_detail_callbacks
from utils.auth import is_authenticated, logout_user

# Register callbacks
register_dashboard_callbacks(app)
register_detail_callbacks(app)

# Main app layout with session handling
app.layout = html.Div([
    # Store components for state management
    dcc.Store(id='session-store', storage_type='session'),
    dcc.Store(id='filter-store', storage_type='memory'),
    dcc.Store(id='data-store', storage_type='memory'),

    # Location for URL routing
    dcc.Location(id='url', refresh=False),

    # Interval for auto-refresh
    dcc.Interval(
        id='refresh-interval',
        interval=AUTO_REFRESH_INTERVAL * 1000,
        n_intervals=0,
        disabled=not ENABLE_AUTO_REFRESH
    ),

    # Main content container
    html.Div(id='page-content')
])


@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname'),
     Input('session-store', 'data')]
)
def display_page(pathname, session_data):
    """Route pages based on authentication state"""
    if session_data and session_data.get('authenticated'):
        return create_main_layout()
    return create_login_layout()


@app.callback(
    [Output('session-store', 'data'),
     Output('login-error', 'children'),
     Output('login-error', 'style')],
    [Input('login-button', 'n_clicks')],
    [State('username-input', 'value'),
     State('password-input', 'value'),
     State('session-store', 'data')],
    prevent_initial_call=True
)
def handle_login(n_clicks, username, password, session_data):
    """Handle login form submission"""
    from utils.auth import authenticate_user

    if not n_clicks:
        return no_update, no_update, no_update

    if not username or not password:
        return (
            session_data,
            "Username dan password harus diisi",
            {'display': 'block'}
        )

    success, user_data = authenticate_user(username, password)

    if success:
        return (
            {
                'authenticated': True,
                'user': user_data,
                'login_time': datetime.now().isoformat(),
                'session_id': str(uuid.uuid4())
            },
            "",
            {'display': 'none'}
        )
    else:
        return (
            session_data,
            "Username atau password salah!",
            {'display': 'block'}
        )


@app.callback(
    Output('session-store', 'data', allow_duplicate=True),
    Input('logout-button', 'n_clicks'),
    prevent_initial_call=True
)
def handle_logout(n_clicks):
    """Handle logout button click"""
    if n_clicks:
        return {'authenticated': False, 'user': None}
    return no_update


# Custom index string with proper meta tags
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            /* Custom scrollbar */
            ::-webkit-scrollbar {
                width: 8px;
                height: 8px;
            }
            ::-webkit-scrollbar-track {
                background: #f1f1f1;
                border-radius: 4px;
            }
            ::-webkit-scrollbar-thumb {
                background: #c1c1c1;
                border-radius: 4px;
            }
            ::-webkit-scrollbar-thumb:hover {
                background: #a1a1a1;
            }

            /* Smooth animations */
            * {
                transition: background-color 0.2s ease, color 0.2s ease;
            }

            /* Loading spinner */
            ._dash-loading {
                margin: auto;
                color: ''' + COLORS['primary'] + ''';
                font-size: 1.2em;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''


if __name__ == '__main__':
    # Initialize database if needed
    from database.migrate_data import run_migration
    import os

    db_path = os.path.join('data', 'monitoring_sts.db')
    if not os.path.exists(db_path):
        print("Database not found. Running migration...")
        run_migration()

    # Run the app
    app.run(
        debug=DEBUG,
        host=HOST,
        port=PORT
    )
