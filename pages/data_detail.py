"""
Data Detail Page - Detailed data views and exports
"""

from dash import html, dcc, Input, Output, callback, no_update
import dash_bootstrap_components as dbc
import pandas as pd
from io import StringIO

from config import COLORS


def create_detail_layout():
    """Create the detail data layout"""
    return html.Div([
        html.H3("Detail Data"),
        html.P("Halaman detail data akan ditampilkan di sini.")
    ])


def register_callbacks(app):
    """Register detail page callbacks"""

    @app.callback(
        Output('download-opd-csv', 'data'),
        Input('download-opd-btn', 'n_clicks'),
        prevent_initial_call=True
    )
    def download_opd_data(n_clicks):
        """Download OPD summary as CSV"""
        if not n_clicks:
            return no_update

        from utils.data_service import get_data_service
        from datetime import datetime

        data_service = get_data_service()
        df = data_service.get_all_transactions()
        opd_summary = data_service.get_opd_summary(df, top_n=None)

        if opd_summary.empty:
            return no_update

        return dcc.send_data_frame(
            opd_summary.to_csv,
            f"rekap_opd_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            index=False
        )

    @app.callback(
        Output('download-transaction-csv', 'data'),
        Input('download-transaction-btn', 'n_clicks'),
        prevent_initial_call=True
    )
    def download_transaction_data(n_clicks):
        """Download all transactions as CSV"""
        if not n_clicks:
            return no_update

        from utils.data_service import get_data_service
        from datetime import datetime

        data_service = get_data_service()
        df = data_service.get_all_transactions()

        if df.empty:
            return no_update

        # Select relevant columns
        export_cols = [
            'kode_billing', 'tanggal_terima', 'tanggal_setor',
            'tanggal_validasi_bank', 'nama_opd', 'nominal',
            'jenis_pembayaran_nama', 'nama_kasir', 'keterangan_umum'
        ]

        export_df = df[export_cols].copy()

        return dcc.send_data_frame(
            export_df.to_csv,
            f"transaksi_sts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            index=False
        )
