"""
Table Components using Dash DataTable
"""

from dash import dash_table, html
import dash_bootstrap_components as dbc
import pandas as pd

from config import COLORS, TABLE_PAGE_SIZE
from utils.formatters import format_rupiah, format_date


def create_base_table_style():
    """Create base style for all tables"""
    return {
        'style_table': {
            'overflowX': 'auto',
            'borderRadius': '8px',
            'border': f'1px solid {COLORS["border"]}'
        },
        'style_header': {
            'backgroundColor': COLORS['primary'],
            'color': COLORS['white'],
            'fontWeight': '600',
            'textAlign': 'left',
            'padding': '12px 16px',
            'fontSize': '0.9rem',
            'borderBottom': f'2px solid {COLORS["primary_dark"]}'
        },
        'style_cell': {
            'textAlign': 'left',
            'padding': '10px 16px',
            'fontSize': '0.9rem',
            'fontFamily': "'Plus Jakarta Sans', sans-serif",
            'border': 'none',
            'borderBottom': f'1px solid {COLORS["border"]}'
        },
        'style_data': {
            'backgroundColor': COLORS['white'],
            'color': COLORS['text_primary']
        },
        'style_data_conditional': [
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': COLORS['light_bg']
            },
            {
                'if': {'state': 'selected'},
                'backgroundColor': f'{COLORS["accent"]}20',
                'border': f'1px solid {COLORS["accent"]}'
            },
            {
                'if': {'state': 'active'},
                'backgroundColor': f'{COLORS["accent"]}30',
                'border': f'1px solid {COLORS["accent"]}'
            }
        ],
        'style_filter': {
            'backgroundColor': COLORS['light_bg'],
            'padding': '8px',
            'fontSize': '0.85rem'
        },
        'page_size': TABLE_PAGE_SIZE,
        'page_action': 'native',
        'sort_action': 'native',
        'filter_action': 'native',
        'sort_mode': 'multi',
    }


def create_opd_table(df: pd.DataFrame):
    """
    Create OPD summary table

    Args:
        df: DataFrame with columns ['nama_opd', 'total', 'jumlah', 'rata_rata', 'minimum', 'maksimum']
    """
    if df.empty:
        return html.Div("Tidak ada data", style={'padding': '2rem', 'textAlign': 'center'})

    # Format columns
    display_df = df.copy()
    display_df['total'] = display_df['total'].apply(format_rupiah)
    display_df['rata_rata'] = display_df['rata_rata'].apply(format_rupiah)
    display_df['minimum'] = display_df['minimum'].apply(format_rupiah)
    display_df['maksimum'] = display_df['maksimum'].apply(format_rupiah)
    display_df['jumlah'] = display_df['jumlah'].apply(lambda x: f"{x:,}".replace(",", "."))

    columns = [
        {'name': 'Nama OPD', 'id': 'nama_opd'},
        {'name': 'Total Penerimaan', 'id': 'total'},
        {'name': 'Jumlah STS', 'id': 'jumlah'},
        {'name': 'Rata-rata', 'id': 'rata_rata'},
        {'name': 'Minimum', 'id': 'minimum'},
        {'name': 'Maksimum', 'id': 'maksimum'},
    ]

    base_style = create_base_table_style()

    return html.Div([
        dash_table.DataTable(
            id='opd-table',
            columns=columns,
            data=display_df.to_dict('records'),
            **base_style,
            style_cell_conditional=[
                {'if': {'column_id': 'nama_opd'}, 'width': '35%', 'textAlign': 'left'},
                {'if': {'column_id': 'total'}, 'width': '15%', 'textAlign': 'right'},
                {'if': {'column_id': 'jumlah'}, 'width': '10%', 'textAlign': 'center'},
                {'if': {'column_id': 'rata_rata'}, 'width': '15%', 'textAlign': 'right'},
                {'if': {'column_id': 'minimum'}, 'width': '12%', 'textAlign': 'right'},
                {'if': {'column_id': 'maksimum'}, 'width': '13%', 'textAlign': 'right'},
            ],
            export_format='csv',
            export_headers='display',
        ),
        html.Div([
            dbc.Button([
                html.I(className='fas fa-download me-2'),
                "Download CSV"
            ],
                id='download-opd-btn',
                color='primary',
                outline=True,
                size='sm',
                className='mt-3'
            )
        ], style={'textAlign': 'right'})
    ])


def create_transaction_table(df: pd.DataFrame, max_rows: int = 500):
    """
    Create transaction detail table

    Args:
        df: DataFrame with transaction data
        max_rows: Maximum rows to display
    """
    if df.empty:
        return html.Div("Tidak ada transaksi", style={'padding': '2rem', 'textAlign': 'center'})

    # Prepare display data
    display_df = df.head(max_rows).copy()

    # Format columns
    display_df['tanggal_terima'] = pd.to_datetime(display_df['tanggal_terima']).dt.strftime('%d/%m/%Y')
    display_df['tanggal_setor'] = pd.to_datetime(display_df['tanggal_setor']).dt.strftime('%d/%m/%Y')
    display_df['tanggal_validasi_bank'] = pd.to_datetime(display_df['tanggal_validasi_bank']).dt.strftime('%d/%m/%Y')
    display_df['nominal'] = display_df['nominal'].apply(format_rupiah)

    # Select and rename columns
    display_df = display_df[[
        'kode_billing', 'tanggal_terima', 'tanggal_setor', 'tanggal_validasi_bank',
        'nama_opd', 'nominal', 'jenis_pembayaran_nama', 'nama_kasir', 'keterangan_umum'
    ]]

    columns = [
        {'name': 'Kode Billing', 'id': 'kode_billing'},
        {'name': 'Tgl Terima', 'id': 'tanggal_terima'},
        {'name': 'Tgl Setor', 'id': 'tanggal_setor'},
        {'name': 'Tgl Valid Bank', 'id': 'tanggal_validasi_bank'},
        {'name': 'OPD', 'id': 'nama_opd'},
        {'name': 'Nominal', 'id': 'nominal'},
        {'name': 'Jenis Bayar', 'id': 'jenis_pembayaran_nama'},
        {'name': 'Bendahara', 'id': 'nama_kasir'},
        {'name': 'Keterangan', 'id': 'keterangan_umum'},
    ]

    base_style = create_base_table_style()

    # Date type info box
    info_box = html.Div([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.I(className='fas fa-inbox me-2', style={'color': '#2196F3'}),
                    html.Strong("Tgl Terima"),
                    html.Br(),
                    html.Small("Dana diterima bendahara", style={'color': COLORS['text_secondary']})
                ], style={
                    'background': COLORS['white'],
                    'padding': '0.75rem',
                    'borderRadius': '8px',
                    'borderLeft': '4px solid #2196F3'
                })
            ], width=4),
            dbc.Col([
                html.Div([
                    html.I(className='fas fa-paper-plane me-2', style={'color': '#FF9800'}),
                    html.Strong("Tgl Setor"),
                    html.Br(),
                    html.Small("Dana disetor ke RKUD", style={'color': COLORS['text_secondary']})
                ], style={
                    'background': COLORS['white'],
                    'padding': '0.75rem',
                    'borderRadius': '8px',
                    'borderLeft': '4px solid #FF9800'
                })
            ], width=4),
            dbc.Col([
                html.Div([
                    html.I(className='fas fa-check-circle me-2', style={'color': '#4CAF50'}),
                    html.Strong("Tgl Valid Bank"),
                    html.Br(),
                    html.Small("Validasi dari Bank Jatim", style={'color': COLORS['text_secondary']})
                ], style={
                    'background': COLORS['white'],
                    'padding': '0.75rem',
                    'borderRadius': '8px',
                    'borderLeft': '4px solid #4CAF50'
                })
            ], width=4),
        ])
    ], style={
        'background': f'linear-gradient(135deg, {COLORS["light_bg"]} 0%, #fff3e0 100%)',
        'padding': '1rem',
        'borderRadius': '10px',
        'marginBottom': '1rem',
        'borderLeft': f'5px solid {COLORS["primary"]}'
    })

    return html.Div([
        info_box,
        dash_table.DataTable(
            id='transaction-table',
            columns=columns,
            data=display_df.to_dict('records'),
            **base_style,
            style_cell_conditional=[
                {'if': {'column_id': 'kode_billing'}, 'width': '12%'},
                {'if': {'column_id': 'tanggal_terima'}, 'width': '9%', 'textAlign': 'center'},
                {'if': {'column_id': 'tanggal_setor'}, 'width': '9%', 'textAlign': 'center'},
                {'if': {'column_id': 'tanggal_validasi_bank'}, 'width': '9%', 'textAlign': 'center'},
                {'if': {'column_id': 'nama_opd'}, 'width': '18%'},
                {'if': {'column_id': 'nominal'}, 'width': '10%', 'textAlign': 'right'},
                {'if': {'column_id': 'jenis_pembayaran_nama'}, 'width': '10%'},
                {'if': {'column_id': 'nama_kasir'}, 'width': '10%'},
                {'if': {'column_id': 'keterangan_umum'}, 'width': '13%', 'maxWidth': '200px', 'overflow': 'hidden', 'textOverflow': 'ellipsis'},
            ],
            tooltip_data=[
                {column: {'value': str(value), 'type': 'markdown'} for column, value in row.items()}
                for row in display_df.to_dict('records')
            ],
            tooltip_duration=None,
        ),
        html.Div([
            html.Small(
                f"Menampilkan {len(display_df):,} dari {len(df):,} transaksi",
                style={'color': COLORS['text_secondary']}
            ),
            dbc.Button([
                html.I(className='fas fa-download me-2'),
                "Download Semua (CSV)"
            ],
                id='download-transaction-btn',
                color='primary',
                outline=True,
                size='sm',
                className='ms-3'
            )
        ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'space-between', 'marginTop': '1rem'})
    ])


def create_bendahara_table(df: pd.DataFrame, max_rows: int = 100):
    """
    Create bendahara summary table

    Args:
        df: DataFrame with columns ['nama_kasir', 'nip_kasir', 'total', 'jumlah', 'opd']
        max_rows: Maximum rows to display
    """
    if df.empty:
        return html.Div("Tidak ada data bendahara", style={'padding': '2rem', 'textAlign': 'center'})

    # Format columns
    display_df = df.head(max_rows).copy()
    display_df['total'] = display_df['total'].apply(format_rupiah)
    display_df['jumlah'] = display_df['jumlah'].apply(lambda x: f"{x:,}".replace(",", "."))

    columns = [
        {'name': 'Nama Bendahara', 'id': 'nama_kasir'},
        {'name': 'NIP', 'id': 'nip_kasir'},
        {'name': 'Total Penerimaan', 'id': 'total'},
        {'name': 'Jumlah STS', 'id': 'jumlah'},
        {'name': 'OPD', 'id': 'opd'},
    ]

    base_style = create_base_table_style()

    return html.Div([
        dash_table.DataTable(
            id='bendahara-table',
            columns=columns,
            data=display_df.to_dict('records'),
            **base_style,
            style_cell_conditional=[
                {'if': {'column_id': 'nama_kasir'}, 'width': '25%'},
                {'if': {'column_id': 'nip_kasir'}, 'width': '15%'},
                {'if': {'column_id': 'total'}, 'width': '20%', 'textAlign': 'right'},
                {'if': {'column_id': 'jumlah'}, 'width': '10%', 'textAlign': 'center'},
                {'if': {'column_id': 'opd'}, 'width': '30%'},
            ],
        ),
        html.Small(
            f"Menampilkan {len(display_df):,} dari {len(df):,} bendahara",
            style={'color': COLORS['text_secondary'], 'marginTop': '1rem', 'display': 'block'}
        )
    ])


def create_simple_table(df: pd.DataFrame, columns: list = None, title: str = None):
    """
    Create a simple display table

    Args:
        df: DataFrame to display
        columns: List of column configurations
        title: Optional table title
    """
    if df.empty:
        return html.Div("Tidak ada data", style={'padding': '2rem', 'textAlign': 'center'})

    if columns is None:
        columns = [{'name': col, 'id': col} for col in df.columns]

    base_style = create_base_table_style()

    content = []
    if title:
        content.append(html.H6(title, style={'marginBottom': '1rem', 'fontWeight': '600'}))

    content.append(
        dash_table.DataTable(
            columns=columns,
            data=df.to_dict('records'),
            **base_style
        )
    )

    return html.Div(content)
