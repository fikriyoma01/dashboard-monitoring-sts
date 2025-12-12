"""
Configuration Settings untuk Monitoring STS Dashboard
"""

import os

# Application Settings
APP_NAME = "Monitoring STS - BAPENDA Jawa Timur"
APP_VERSION = "2.0.0"
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# Server Settings
HOST = os.environ.get('HOST', '0.0.0.0')
PORT = int(os.environ.get('PORT', 8050))

# Database Settings
DATABASE_URL = os.environ.get(
    'DATABASE_URL',
    'sqlite:///data/monitoring_sts.db'
)

# Authentication
SECRET_KEY = os.environ.get('SECRET_KEY', 'bapenda-jatim-secret-key-2025')
SESSION_TIMEOUT = int(os.environ.get('SESSION_TIMEOUT', 3600))  # 1 hour

# Default Credentials (for initial setup)
DEFAULT_USERNAME = 'bapendaptip'
DEFAULT_PASSWORD = 'ptipbapenda2025'

# Data Settings
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
ASSETS_DIR = os.path.join(os.path.dirname(__file__), 'assets')

# Auto Refresh Settings
AUTO_REFRESH_INTERVAL = 30  # seconds
ENABLE_AUTO_REFRESH = True

# UI Theme Colors - Jawa Timur Government
COLORS = {
    'primary': '#00688B',      # Biru tua (profesional)
    'primary_light': '#0088B4',
    'primary_dark': '#004D66',
    'secondary': '#00A550',    # Hijau Jatim
    'secondary_light': '#00C964',
    'accent': '#00B5EF',       # Biru muda Jatim
    'dark': '#1a1a2e',
    'dark_light': '#2d2d4a',
    'gold': '#D4AF37',
    'gold_light': '#E5C158',
    'white': '#FFFFFF',
    'light_bg': '#F0F8FF',
    'light_gray': '#F5F7FA',
    'gray': '#6c757d',
    'success': '#28a745',
    'warning': '#ffc107',
    'danger': '#dc3545',
    'info': '#17a2b8',
    'text_primary': '#212529',
    'text_secondary': '#6c757d',
    'border': '#dee2e6',
}

# Chart Color Scales
CHART_COLORS = [
    '#00688B', '#00A550', '#00B5EF', '#D4AF37', '#6c757d',
    '#17a2b8', '#28a745', '#ffc107', '#dc3545', '#6610f2'
]

CHART_COLORSCALE = [
    [0, '#E6F3FF'],
    [0.5, '#00B5EF'],
    [1, '#00688B']
]

# Payment Type Mapping
PAYMENT_TYPES = {
    1: 'Tunai',
    2: 'E-Samsat/Giro/Transfer',
    3: 'EDC',
    4: 'Virtual Account',
    5: 'QRIS'
}

# Month Names (Indonesian)
MONTH_NAMES = {
    1: 'Januari', 2: 'Februari', 3: 'Maret', 4: 'April',
    5: 'Mei', 6: 'Juni', 7: 'Juli', 8: 'Agustus',
    9: 'September', 10: 'Oktober', 11: 'November', 12: 'Desember'
}

MONTH_NAMES_SHORT = {
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr',
    5: 'Mei', 6: 'Jun', 7: 'Jul', 8: 'Agu',
    9: 'Sep', 10: 'Okt', 11: 'Nov', 12: 'Des'
}

# Day Names (Indonesian)
DAY_NAMES = {
    'Monday': 'Senin',
    'Tuesday': 'Selasa',
    'Wednesday': 'Rabu',
    'Thursday': 'Kamis',
    'Friday': 'Jumat',
    'Saturday': 'Sabtu',
    'Sunday': 'Minggu'
}

# Display Settings
MAX_DISPLAY_ROWS = 500
TABLE_PAGE_SIZE = 20
TOP_OPD_COUNT = 15

# Plotly Layout Defaults
PLOTLY_CONFIG = {
    'displayModeBar': True,
    'displaylogo': False,
    'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
    'responsive': True
}

PLOTLY_LAYOUT = {
    'font': {'family': 'Plus Jakarta Sans, -apple-system, BlinkMacSystemFont, sans-serif'},
    'paper_bgcolor': 'white',
    'plot_bgcolor': 'white',
    'margin': {'l': 20, 'r': 20, 't': 40, 'b': 20},
    'hoverlabel': {
        'bgcolor': 'white',
        'font_size': 13,
        'font_family': 'Plus Jakarta Sans'
    }
}
