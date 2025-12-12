"""
Dashboard Page - Main monitoring dashboard
"""

from dash import html, dcc, Input, Output, State, callback, no_update
import dash_bootstrap_components as dbc
from datetime import datetime
import pandas as pd

from config import COLORS, MONTH_NAMES_SHORT
from components.header import create_header
from components.sidebar import create_sidebar, create_period_selector
from components.cards import create_metric_cards, create_info_box, create_section_header
from components.charts import create_opd_chart, create_payment_chart, create_trend_chart, create_monthly_chart
from components.tables import create_opd_table, create_transaction_table, create_bendahara_table
from components.footer import create_footer
from utils.data_service import get_data_service
from utils.formatters import format_date


def create_dashboard_layout():
    """Create the main dashboard layout"""
    return html.Div([
        # Header
        html.Div(id='header-container'),

        # Main content area
        dbc.Row([
            # Sidebar
            dbc.Col([
                html.Div(id='sidebar-content')
            ], width=12, lg=3, className='sidebar-col', style={
                'position': 'sticky',
                'top': '0',
                'height': '100vh',
                'overflowY': 'auto'
            }),

            # Main content
            dbc.Col([
                html.Div([
                    # Info box
                    html.Div(id='info-box-container'),

                    # Metric cards
                    html.Div(id='metric-cards-container'),

                    # Charts row 1: OPD Chart
                    html.Div([
                        create_section_header("Penerimaan per OPD (Top 15)", "fa-chart-bar"),
                        html.Div(id='opd-chart-container', style={
                            'background': COLORS['white'],
                            'borderRadius': '12px',
                            'padding': '1rem',
                            'boxShadow': '0 3px 10px rgba(0,0,0,0.06)'
                        })
                    ], className='mb-4'),

                    # Charts row 2: Payment & Trend
                    dbc.Row([
                        dbc.Col([
                            create_section_header("Jenis Pembayaran", "fa-credit-card"),
                            html.Div(id='payment-chart-container', style={
                                'background': COLORS['white'],
                                'borderRadius': '12px',
                                'padding': '1rem',
                                'boxShadow': '0 3px 10px rgba(0,0,0,0.06)'
                            }),
                            html.Div(id='payment-table-container', className='mt-3')
                        ], width=12, lg=4, className='mb-4'),

                        dbc.Col([
                            create_section_header("Tren Penerimaan Harian", "fa-chart-line"),
                            html.Div(id='trend-chart-container', style={
                                'background': COLORS['white'],
                                'borderRadius': '12px',
                                'padding': '1rem',
                                'boxShadow': '0 3px 10px rgba(0,0,0,0.06)'
                            })
                        ], width=12, lg=8, className='mb-4')
                    ]),

                    # Charts row 3: Monthly
                    html.Div([
                        create_section_header("Rekap Penerimaan Bulanan", "fa-calendar-alt"),
                        html.Div(id='monthly-chart-container', style={
                            'background': COLORS['white'],
                            'borderRadius': '12px',
                            'padding': '1rem',
                            'boxShadow': '0 3px 10px rgba(0,0,0,0.06)'
                        })
                    ], className='mb-4'),

                    # Detail data tabs
                    html.Div([
                        create_section_header("Detail Data", "fa-table"),
                        dbc.Tabs([
                            dbc.Tab(
                                html.Div(id='opd-table-container', className='p-3'),
                                label="Rekap per OPD",
                                tab_id="tab-opd",
                                label_style={'fontWeight': '600'}
                            ),
                            dbc.Tab(
                                html.Div(id='transaction-table-container', className='p-3'),
                                label="Daftar Transaksi STS",
                                tab_id="tab-transaction",
                                label_style={'fontWeight': '600'}
                            ),
                            dbc.Tab(
                                html.Div(id='bendahara-table-container', className='p-3'),
                                label="Rekap per Bendahara",
                                tab_id="tab-bendahara",
                                label_style={'fontWeight': '600'}
                            ),
                        ],
                            id='detail-tabs',
                            active_tab='tab-opd',
                            style={
                                'background': COLORS['white'],
                                'borderRadius': '12px',
                                'boxShadow': '0 3px 10px rgba(0,0,0,0.06)'
                            }
                        )
                    ], className='mb-4'),

                    # Footer
                    create_footer()

                ], style={'padding': '1.5rem'})
            ], width=12, lg=9)
        ], className='g-0'),

        # Hidden stores for data
        dcc.Store(id='filtered-data-store'),
        dcc.Store(id='period-label-store'),

        # Download components
        dcc.Download(id='download-opd-csv'),
        dcc.Download(id='download-transaction-csv'),

    ], style={
        'backgroundColor': COLORS['light_bg'],
        'minHeight': '100vh',
        'fontFamily': "'Plus Jakarta Sans', sans-serif"
    })


def register_callbacks(app):
    """Register all dashboard callbacks"""

    @app.callback(
        Output('header-container', 'children'),
        Input('session-store', 'data')
    )
    def update_header(session_data):
        """Update header with user info"""
        user_info = session_data.get('user', {}) if session_data else {}
        return create_header(user_info)

    @app.callback(
        Output('sidebar-content', 'children'),
        Input('session-store', 'data')
    )
    def update_sidebar(session_data):
        """Initialize sidebar with data"""
        data_service = get_data_service()

        try:
            df = data_service.get_all_transactions()
            min_date, max_date = data_service.get_date_range()
            opd_list = data_service.get_opd_list()
            payment_types = data_service.get_payment_types()

            years = sorted(df['tahun'].unique().tolist()) if not df.empty else [datetime.now().year]
            weeks = sorted(df['minggu_tahun'].unique().tolist()) if not df.empty else list(range(1, 53))

        except Exception as e:
            print(f"Error loading data: {e}")
            min_date = max_date = datetime.now().date()
            opd_list = []
            payment_types = []
            years = [datetime.now().year]
            weeks = list(range(1, 53))

        return create_sidebar(
            min_date=min_date.date() if hasattr(min_date, 'date') else min_date,
            max_date=max_date.date() if hasattr(max_date, 'date') else max_date,
            opd_list=opd_list,
            payment_types=payment_types,
            years=years,
            weeks=weeks
        )

    @app.callback(
        Output('period-selector-container', 'children'),
        Input('period-type-dropdown', 'value'),
        State('session-store', 'data')
    )
    def update_period_selector(period_type, session_data):
        """Update period selector based on period type"""
        data_service = get_data_service()

        try:
            df = data_service.get_all_transactions()
            min_date, max_date = data_service.get_date_range()
            years = sorted(df['tahun'].unique().tolist()) if not df.empty else [datetime.now().year]
            weeks = sorted(df['minggu_tahun'].unique().tolist()) if not df.empty else list(range(1, 53))
        except:
            min_date = max_date = datetime.now()
            years = [datetime.now().year]
            weeks = list(range(1, 53))

        return create_period_selector(
            period_type,
            min_date.date() if hasattr(min_date, 'date') else min_date,
            max_date.date() if hasattr(max_date, 'date') else max_date,
            years,
            weeks
        )

    @app.callback(
        [Output('filtered-data-store', 'data'),
         Output('period-label-store', 'data')],
        [Input('period-type-dropdown', 'value'),
         Input('opd-dropdown', 'value'),
         Input('payment-dropdown', 'value'),
         Input('date-picker-single', 'date'),
         Input('date-picker-start', 'date'),
         Input('date-picker-end', 'date'),
         Input('week-dropdown', 'value'),
         Input('year-dropdown-week', 'value'),
         Input('month-dropdown', 'value'),
         Input('year-dropdown-month', 'value'),
         Input('year-dropdown', 'value'),
         Input('manual-refresh-button', 'n_clicks'),
         Input('refresh-interval', 'n_intervals')],
        prevent_initial_call=False
    )
    def filter_data(
        period_type, selected_opd, selected_payment,
        single_date, start_date, end_date,
        selected_week, year_week,
        selected_month, year_month,
        selected_year,
        refresh_clicks, refresh_intervals
    ):
        """Filter data based on all filter inputs"""
        data_service = get_data_service()

        try:
            df = data_service.get_all_transactions()

            # Parse dates
            if single_date:
                single_date = pd.to_datetime(single_date).date()
            if start_date:
                start_date = pd.to_datetime(start_date).date()
            if end_date:
                end_date = pd.to_datetime(end_date).date()

            # Apply filters
            df_filtered, period_label = data_service.filter_data(
                df,
                period_type=period_type or 'Semua Data',
                selected_date=single_date,
                start_date=start_date,
                end_date=end_date,
                selected_week=selected_week,
                selected_month=selected_month,
                selected_year=selected_year or year_week or year_month,
                selected_opd=selected_opd,
                selected_payment=selected_payment
            )

            # Convert to serializable format
            data_dict = df_filtered.to_dict('records')

            # Convert datetime objects to strings
            for record in data_dict:
                for key, value in record.items():
                    if isinstance(value, (datetime, pd.Timestamp)):
                        record[key] = value.isoformat()
                    elif pd.isna(value):
                        record[key] = None

            return data_dict, period_label

        except Exception as e:
            print(f"Error filtering data: {e}")
            return [], "Semua Data"

    @app.callback(
        Output('info-box-container', 'children'),
        [Input('filtered-data-store', 'data'),
         Input('period-label-store', 'data')]
    )
    def update_info_box(data, period_label):
        """Update info box"""
        if not data:
            return create_info_box("Semua Data", 0, 0, "-")

        df = pd.DataFrame(data)
        data_service = get_data_service()
        min_date, max_date = data_service.get_date_range()

        date_range = f"{format_date(min_date)} - {format_date(max_date)}"

        return create_info_box(
            period_label or "Semua Data",
            len(df),
            df['nama_opd'].nunique() if not df.empty else 0,
            date_range
        )

    @app.callback(
        Output('metric-cards-container', 'children'),
        Input('filtered-data-store', 'data')
    )
    def update_metric_cards(data):
        """Update metric cards"""
        if not data:
            return create_metric_cards({
                'total_penerimaan': 0,
                'jumlah_sts': 0,
                'rata_rata': 0,
                'jumlah_opd': 0
            })

        df = pd.DataFrame(data)
        data_service = get_data_service()
        metrics = data_service.get_summary_metrics(df)

        return create_metric_cards(metrics)

    @app.callback(
        Output('opd-chart-container', 'children'),
        Input('filtered-data-store', 'data')
    )
    def update_opd_chart(data):
        """Update OPD chart"""
        if not data:
            return html.Div("Tidak ada data", style={'padding': '2rem', 'textAlign': 'center'})

        df = pd.DataFrame(data)
        data_service = get_data_service()
        opd_summary = data_service.get_opd_summary(df, top_n=15)

        return create_opd_chart(opd_summary)

    @app.callback(
        [Output('payment-chart-container', 'children'),
         Output('payment-table-container', 'children')],
        Input('filtered-data-store', 'data')
    )
    def update_payment_section(data):
        """Update payment chart and table"""
        if not data:
            return html.Div("Tidak ada data"), html.Div()

        df = pd.DataFrame(data)
        data_service = get_data_service()
        payment_summary = data_service.get_payment_summary(df)

        chart = create_payment_chart(payment_summary)

        # Simple payment table
        if not payment_summary.empty:
            from utils.formatters import format_rupiah, format_percentage
            table_df = payment_summary.copy()
            table_df['total'] = table_df['total'].apply(format_rupiah)
            table_df['persentase'] = table_df['persentase'].apply(lambda x: f"{x:.1f}%")

            table = dbc.Table.from_dataframe(
                table_df[['jenis_pembayaran', 'total', 'jumlah', 'persentase']],
                striped=True,
                bordered=True,
                hover=True,
                size='sm',
                style={'fontSize': '0.85rem'}
            )
        else:
            table = html.Div()

        return chart, table

    @app.callback(
        Output('trend-chart-container', 'children'),
        Input('filtered-data-store', 'data')
    )
    def update_trend_chart(data):
        """Update daily trend chart"""
        if not data:
            return html.Div("Tidak ada data", style={'padding': '2rem', 'textAlign': 'center'})

        df = pd.DataFrame(data)
        df['tanggal'] = pd.to_datetime(df['tanggal_terima']).dt.date
        data_service = get_data_service()
        trend_data = data_service.get_daily_trend(df)

        return create_trend_chart(trend_data)

    @app.callback(
        Output('monthly-chart-container', 'children'),
        Input('filtered-data-store', 'data')
    )
    def update_monthly_chart(data):
        """Update monthly chart"""
        if not data:
            return html.Div("Tidak ada data", style={'padding': '2rem', 'textAlign': 'center'})

        df = pd.DataFrame(data)
        df['tanggal_terima'] = pd.to_datetime(df['tanggal_terima'])
        df['tahun'] = df['tanggal_terima'].dt.year
        df['bulan'] = df['tanggal_terima'].dt.month

        data_service = get_data_service()
        monthly_data = data_service.get_monthly_summary(df)

        return create_monthly_chart(monthly_data)

    @app.callback(
        Output('opd-table-container', 'children'),
        Input('filtered-data-store', 'data')
    )
    def update_opd_table(data):
        """Update OPD table"""
        if not data:
            return html.Div("Tidak ada data")

        df = pd.DataFrame(data)
        data_service = get_data_service()
        opd_summary = data_service.get_opd_summary(df, top_n=None)

        return create_opd_table(opd_summary)

    @app.callback(
        Output('transaction-table-container', 'children'),
        Input('filtered-data-store', 'data')
    )
    def update_transaction_table(data):
        """Update transaction table"""
        if not data:
            return html.Div("Tidak ada data")

        df = pd.DataFrame(data)
        data_service = get_data_service()
        detail_data = data_service.get_transaction_detail(df, limit=500)

        return create_transaction_table(detail_data)

    @app.callback(
        Output('bendahara-table-container', 'children'),
        Input('filtered-data-store', 'data')
    )
    def update_bendahara_table(data):
        """Update bendahara table"""
        if not data:
            return html.Div("Tidak ada data")

        df = pd.DataFrame(data)
        data_service = get_data_service()
        bendahara_data = data_service.get_bendahara_summary(df)

        return create_bendahara_table(bendahara_data)

    @app.callback(
        Output('refresh-interval', 'disabled'),
        Input('auto-refresh-switch', 'value')
    )
    def toggle_auto_refresh(enabled):
        """Toggle auto refresh"""
        return not enabled

    @app.callback(
        [Output('data-info-text', 'children'),
         Output('last-update-text', 'children')],
        Input('filtered-data-store', 'data')
    )
    def update_data_info(data):
        """Update data info in sidebar"""
        if not data:
            return "Tidak ada data", ""

        df = pd.DataFrame(data)
        info_text = f"{len(df):,} transaksi | {df['nama_opd'].nunique()} OPD"
        update_text = f"Update: {datetime.now().strftime('%H:%M:%S')}"

        return info_text, update_text
