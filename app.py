import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
import base64

# Page config
st.set_page_config(
    page_title="Monitoring STS - BAPENDA Jawa Timur",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Jawa Timur Government Color Theme
COLORS = {
    'primary': '#00688B',      # Biru tua (profesional)
    'secondary': '#00A550',    # Hijau Jatim
    'accent': '#00B5EF',       # Biru muda Jatim
    'dark': '#1a1a2e',         # Gelap
    'gold': '#D4AF37',         # Emas
    'white': '#FFFFFF',
    'light_bg': '#F0F8FF',     # Background biru sangat muda
    'success': '#28a745',
    'warning': '#ffc107',
    'danger': '#dc3545',
}

# Custom CSS with Jawa Timur Theme
st.markdown(f"""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* Global Styles */
    .stApp {{
        font-family: 'Inter', sans-serif;
    }}

    /* Header Styling */
    .main-header {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['dark']} 100%);
        padding: 1.5rem 2rem;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(0, 104, 139, 0.3);
        display: flex;
        align-items: center;
        gap: 20px;
    }}

    .header-logo {{
        width: 80px;
        height: auto;
    }}

    .header-text {{
        flex: 1;
    }}

    .header-title {{
        color: {COLORS['white']};
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }}

    .header-subtitle {{
        color: {COLORS['accent']};
        font-size: 1rem;
        margin: 5px 0 0 0;
        font-weight: 500;
    }}

    .header-org {{
        color: {COLORS['gold']};
        font-size: 0.9rem;
        margin: 3px 0 0 0;
        font-weight: 600;
    }}

    /* Metric Cards */
    .metric-container {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin-bottom: 1.5rem;
    }}

    .metric-card {{
        background: linear-gradient(145deg, {COLORS['white']} 0%, {COLORS['light_bg']} 100%);
        padding: 1.2rem;
        border-radius: 12px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.08);
        border-left: 4px solid {COLORS['primary']};
        transition: transform 0.2s, box-shadow 0.2s;
    }}

    .metric-card:hover {{
        transform: translateY(-3px);
        box-shadow: 0 5px 20px rgba(0,0,0,0.12);
    }}

    .metric-card.green {{ border-left-color: {COLORS['secondary']}; }}
    .metric-card.gold {{ border-left-color: {COLORS['gold']}; }}
    .metric-card.accent {{ border-left-color: {COLORS['accent']}; }}

    .metric-icon {{
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }}

    .metric-value {{
        font-size: 1.5rem;
        font-weight: 700;
        color: {COLORS['dark']};
        margin: 0;
    }}

    .metric-label {{
        font-size: 0.85rem;
        color: #666;
        margin: 0;
        font-weight: 500;
    }}

    /* Section Headers */
    .section-header {{
        background: linear-gradient(90deg, {COLORS['primary']} 0%, {COLORS['accent']} 100%);
        color: white;
        padding: 0.8rem 1.2rem;
        border-radius: 8px;
        margin: 1.5rem 0 1rem 0;
        font-weight: 600;
        font-size: 1.1rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }}

    /* Info Box */
    .info-box {{
        background: linear-gradient(135deg, {COLORS['light_bg']} 0%, #E6F3FF 100%);
        border: 1px solid {COLORS['accent']};
        border-radius: 10px;
        padding: 1rem 1.5rem;
        margin-bottom: 1.5rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 1rem;
    }}

    .info-item {{
        display: flex;
        align-items: center;
        gap: 8px;
    }}

    .info-icon {{
        font-size: 1.2rem;
    }}

    .info-label {{
        color: #555;
        font-size: 0.85rem;
    }}

    .info-value {{
        color: {COLORS['primary']};
        font-weight: 600;
        font-size: 0.95rem;
    }}

    /* Chart Container */
    .chart-container {{
        background: white;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        margin-bottom: 1rem;
    }}

    /* Table Styling */
    .dataframe {{
        border-radius: 8px;
        overflow: hidden;
    }}

    /* Footer */
    .footer {{
        background: linear-gradient(135deg, {COLORS['dark']} 0%, {COLORS['primary']} 100%);
        color: white;
        text-align: center;
        padding: 1.5rem;
        border-radius: 12px;
        margin-top: 2rem;
    }}

    .footer p {{
        margin: 0.3rem 0;
    }}

    .footer-title {{
        font-weight: 600;
        font-size: 1rem;
        color: {COLORS['gold']};
    }}

    .footer-subtitle {{
        font-size: 0.85rem;
        color: #aaa;
    }}

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {COLORS['light_bg']} 0%, white 100%);
    }}

    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stMultiSelect label {{
        color: {COLORS['primary']};
        font-weight: 600;
    }}

    /* Hide Streamlit Branding */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}

    /* Custom Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
    }}

    .stTabs [data-baseweb="tab"] {{
        background: {COLORS['light_bg']};
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        font-weight: 500;
    }}

    .stTabs [aria-selected="true"] {{
        background: {COLORS['primary']};
        color: white;
    }}
</style>
""", unsafe_allow_html=True)

# Data paths
DATA_DIR = "data"
ASSETS_DIR = "assets"

def get_base64_image(image_path):
    """Convert image to base64 for embedding in HTML"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return None

@st.cache_data
def load_data():
    """Load all CSV data files"""
    kasdasts = pd.read_csv(
        os.path.join(DATA_DIR, "kasdasts_202512100801.csv"),
        parse_dates=['TGTERIMA', 'TGSETOR', 'TGVALIDBANK'],
        dayfirst=False
    )

    bpp = pd.read_csv(os.path.join(DATA_DIR, "bpp_202512100822.csv"))
    rek = pd.read_csv(os.path.join(DATA_DIR, "rek_202512100823.csv"))
    rek['KODE'] = rek['KODE'].astype(str)
    opdrek = pd.read_csv(os.path.join(DATA_DIR, "opdrek_202512100820.csv"))

    opd_ref = pd.read_excel(
        os.path.join(DATA_DIR, "TABEL_REFERENSI_KASDASTS.xlsx"),
        sheet_name="OPD"
    )
    opd_ref.columns = ['KODE_OPD', 'NAMA_OPD', 'TAHUN', 'KODE_QRCODE']
    opd_ref['KODE_OPD'] = opd_ref['KODE_OPD'].astype(str)

    return kasdasts, bpp, rek, opdrek, opd_ref

@st.cache_data
def process_data(kasdasts, bpp, opd_ref, rek):
    """Process and enrich transaction data"""
    df = kasdasts.copy()

    df['KODE_OPD'] = df['AYAT'].str[:15]
    df['KODE_REK'] = df['AYAT'].str[15:]

    df = df.merge(opd_ref[['KODE_OPD', 'NAMA_OPD']], on='KODE_OPD', how='left')
    df = df.merge(bpp[['IDSIBAKU', 'NAMA', 'NIP']], left_on='KDKASIR', right_on='IDSIBAKU', how='left')
    df.rename(columns={'NAMA': 'NAMA_KASIR', 'NIP': 'NIP_KASIR'}, inplace=True)
    df = df.merge(rek[['KODE', 'NAMA_REK']], left_on='KODE_REK', right_on='KODE', how='left')

    df['NAMA_OPD'] = df['NAMA_OPD'].fillna('OPD Tidak Diketahui')

    df['TANGGAL'] = df['TGTERIMA'].dt.date
    df['TAHUN'] = df['TGTERIMA'].dt.year
    df['BULAN'] = df['TGTERIMA'].dt.month
    df['NAMA_BULAN'] = df['TGTERIMA'].dt.month_name()
    df['MINGGU_TAHUN'] = df['TGTERIMA'].dt.isocalendar().week
    df['HARI'] = df['TGTERIMA'].dt.day_name()

    payment_map = {1: 'Tunai', 2: 'E-Samsat/Giro/Transfer', 3: 'EDC', 4: 'Virtual Account', 5: 'QRIS'}
    df['JENIS_PEMBAYARAN'] = df['KDTUNAI'].map(payment_map).fillna('Lainnya')

    return df

def format_rupiah(value):
    """Format number as Indonesian Rupiah"""
    if pd.isna(value):
        return "Rp 0"
    return f"Rp {value:,.0f}".replace(",", ".")

def format_rupiah_short(value):
    """Format number as shortened Rupiah"""
    if value >= 1e12:
        return f"Rp {value/1e12:.2f} T"
    elif value >= 1e9:
        return f"Rp {value/1e9:.2f} M"
    elif value >= 1e6:
        return f"Rp {value/1e6:.1f} Jt"
    else:
        return f"Rp {value:,.0f}".replace(",", ".")

def main():
    # Load logo
    logo_path = os.path.join(ASSETS_DIR, "logo_jawa-timur.svg")
    logo_base64 = get_base64_image(logo_path)

    # Header with Logo
    header_html = f"""
    <div class="main-header">
        <img src="data:image/svg+xml;base64,{logo_base64}" class="header-logo" alt="Logo Jawa Timur">
        <div class="header-text">
            <p class="header-title">📊 MONITORING PENERIMAAN RETRIBUSI & PAD</p>
            <p class="header-subtitle">Surat Tanda Setoran (STS)</p>
            <p class="header-org">BADAN PENDAPATAN DAERAH PROVINSI JAWA TIMUR</p>
        </div>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)

    # Load data
    with st.spinner("Memuat data..."):
        kasdasts, bpp, rek, opdrek, opd_ref = load_data()
        df = process_data(kasdasts, bpp, opd_ref, rek)

    # Sidebar with logo
    with st.sidebar:
        st.image(os.path.join(ASSETS_DIR, "bapendajatim_logo.png"), use_container_width=True)
        st.markdown("---")

        st.markdown(f"### 🔍 Filter Data")

        # Period filter
        st.markdown("**📅 Periode Waktu**")
        period_type = st.selectbox(
            "Pilih Jenis Periode",
            ["Semua Data", "Harian", "Mingguan", "Bulanan", "Tahunan", "Rentang Tanggal"],
            label_visibility="collapsed"
        )

        min_date = df['TGTERIMA'].min().date()
        max_date = df['TGTERIMA'].max().date()

        if period_type == "Harian":
            selected_date = st.date_input("Pilih Tanggal", value=max_date, min_value=min_date, max_value=max_date)
            df_filtered = df[df['TANGGAL'] == selected_date]
            period_label = f"{selected_date.strftime('%d %B %Y')}"
        elif period_type == "Mingguan":
            available_weeks = sorted(df['MINGGU_TAHUN'].unique())
            col1, col2 = st.columns(2)
            selected_week = col1.selectbox("Minggu", available_weeks, index=len(available_weeks)-1)
            selected_year = col2.selectbox("Tahun", sorted(df['TAHUN'].unique()), index=0)
            df_filtered = df[(df['MINGGU_TAHUN'] == selected_week) & (df['TAHUN'] == selected_year)]
            period_label = f"Minggu ke-{selected_week}, {selected_year}"
        elif period_type == "Bulanan":
            months = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'Mei', 6:'Jun', 7:'Jul', 8:'Agu', 9:'Sep', 10:'Okt', 11:'Nov', 12:'Des'}
            months_full = {1:'Januari', 2:'Februari', 3:'Maret', 4:'April', 5:'Mei', 6:'Juni', 7:'Juli', 8:'Agustus', 9:'September', 10:'Oktober', 11:'November', 12:'Desember'}
            available_months = sorted(df['BULAN'].unique())
            col1, col2 = st.columns(2)
            selected_month = col1.selectbox("Bulan", available_months, format_func=lambda x: months[x])
            selected_year = col2.selectbox("Tahun ", sorted(df['TAHUN'].unique()), index=0)
            df_filtered = df[(df['BULAN'] == selected_month) & (df['TAHUN'] == selected_year)]
            period_label = f"{months_full[selected_month]} {selected_year}"
        elif period_type == "Tahunan":
            selected_year = st.selectbox("Pilih Tahun", sorted(df['TAHUN'].unique()), index=0)
            df_filtered = df[df['TAHUN'] == selected_year]
            period_label = f"Tahun {selected_year}"
        elif period_type == "Rentang Tanggal":
            col1, col2 = st.columns(2)
            start_date = col1.date_input("Dari", value=min_date, min_value=min_date, max_value=max_date)
            end_date = col2.date_input("Sampai", value=max_date, min_value=min_date, max_value=max_date)
            df_filtered = df[(df['TANGGAL'] >= start_date) & (df['TANGGAL'] <= end_date)]
            period_label = f"{start_date.strftime('%d/%m/%Y')} - {end_date.strftime('%d/%m/%Y')}"
        else:
            df_filtered = df.copy()
            period_label = "Semua Data"

        st.markdown("---")
        st.markdown("**🏢 Perangkat Daerah**")
        opd_list = ['Semua OPD'] + sorted(df_filtered['NAMA_OPD'].unique().tolist())
        selected_opd = st.multiselect("Pilih OPD", opd_list, default=['Semua OPD'], label_visibility="collapsed")

        if 'Semua OPD' not in selected_opd and len(selected_opd) > 0:
            df_filtered = df_filtered[df_filtered['NAMA_OPD'].isin(selected_opd)]

        st.markdown("---")
        st.markdown("**💳 Jenis Pembayaran**")
        payment_list = ['Semua'] + sorted(df_filtered['JENIS_PEMBAYARAN'].unique().tolist())
        selected_payment = st.selectbox("Pilih Jenis", payment_list, label_visibility="collapsed")

        if selected_payment != 'Semua':
            df_filtered = df_filtered[df_filtered['JENIS_PEMBAYARAN'] == selected_payment]

    # Info Box
    info_html = f"""
    <div class="info-box">
        <div class="info-item">
            <span class="info-icon">📅</span>
            <div>
                <div class="info-label">Periode</div>
                <div class="info-value">{period_label}</div>
            </div>
        </div>
        <div class="info-item">
            <span class="info-icon">📋</span>
            <div>
                <div class="info-label">Total Transaksi</div>
                <div class="info-value">{len(df_filtered):,}</div>
            </div>
        </div>
        <div class="info-item">
            <span class="info-icon">🏢</span>
            <div>
                <div class="info-label">Jumlah OPD</div>
                <div class="info-value">{df_filtered['NAMA_OPD'].nunique()}</div>
            </div>
        </div>
        <div class="info-item">
            <span class="info-icon">📆</span>
            <div>
                <div class="info-label">Rentang Data</div>
                <div class="info-value">{min_date.strftime('%d/%m/%Y')} - {max_date.strftime('%d/%m/%Y')}</div>
            </div>
        </div>
    </div>
    """
    st.markdown(info_html, unsafe_allow_html=True)

    # Summary Metrics
    total_penerimaan = df_filtered['RPPOKOK'].sum()
    jumlah_sts = len(df_filtered)
    rata_rata = df_filtered['RPPOKOK'].mean() if len(df_filtered) > 0 else 0
    jumlah_opd = df_filtered['NAMA_OPD'].nunique()

    metrics_html = f"""
    <div class="metric-container">
        <div class="metric-card">
            <div class="metric-icon">💰</div>
            <p class="metric-value">{format_rupiah_short(total_penerimaan)}</p>
            <p class="metric-label">Total Penerimaan</p>
        </div>
        <div class="metric-card green">
            <div class="metric-icon">📄</div>
            <p class="metric-value">{jumlah_sts:,}</p>
            <p class="metric-label">Jumlah STS</p>
        </div>
        <div class="metric-card gold">
            <div class="metric-icon">📊</div>
            <p class="metric-value">{format_rupiah_short(rata_rata)}</p>
            <p class="metric-label">Rata-rata per STS</p>
        </div>
        <div class="metric-card accent">
            <div class="metric-icon">🏛️</div>
            <p class="metric-value">{jumlah_opd}</p>
            <p class="metric-label">Perangkat Daerah</p>
        </div>
    </div>
    """
    st.markdown(metrics_html, unsafe_allow_html=True)

    # Section 1: Penerimaan per OPD
    st.markdown('<div class="section-header">📊 Penerimaan per OPD (Top 15)</div>', unsafe_allow_html=True)

    opd_summary = df_filtered.groupby('NAMA_OPD').agg({
        'RPPOKOK': 'sum',
        'KDBILL': 'count'
    }).reset_index()
    opd_summary.columns = ['OPD', 'Total Penerimaan', 'Jumlah STS']
    opd_summary = opd_summary.sort_values('Total Penerimaan', ascending=True).tail(15)

    fig_opd = go.Figure()
    fig_opd.add_trace(go.Bar(
        y=opd_summary['OPD'],
        x=opd_summary['Total Penerimaan'],
        orientation='h',
        marker=dict(
            color=opd_summary['Total Penerimaan'],
            colorscale=[[0, '#E6F3FF'], [0.5, '#00B5EF'], [1, '#00688B']],
            line=dict(color='#00688B', width=1)
        ),
        text=opd_summary['Total Penerimaan'].apply(format_rupiah_short),
        textposition='outside',
        textfont=dict(size=11, color='#333'),
        hovertemplate='<b>%{y}</b><br>Total: %{text}<br>Jumlah STS: %{customdata}<extra></extra>',
        customdata=opd_summary['Jumlah STS']
    ))

    fig_opd.update_layout(
        height=450,
        margin=dict(l=10, r=100, t=20, b=20),
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(
            title='Total Penerimaan (Rp)',
            gridcolor='#eee',
            showline=True,
            linecolor='#ddd'
        ),
        yaxis=dict(
            title='',
            showgrid=False
        ),
        font=dict(family='Inter, sans-serif')
    )
    st.plotly_chart(fig_opd, use_container_width=True)

    # Section 2: Jenis Pembayaran & Tren Bulanan
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown('<div class="section-header">💳 Jenis Pembayaran</div>', unsafe_allow_html=True)

        payment_summary = df_filtered.groupby('JENIS_PEMBAYARAN').agg({
            'RPPOKOK': 'sum',
            'KDBILL': 'count'
        }).reset_index()
        payment_summary.columns = ['Jenis Pembayaran', 'Total Penerimaan', 'Jumlah STS']
        payment_summary = payment_summary.sort_values('Total Penerimaan', ascending=False)

        total_all = payment_summary['Total Penerimaan'].sum()
        payment_summary['Persentase'] = (payment_summary['Total Penerimaan'] / total_all * 100).round(2)

        colors_pie = ['#00688B', '#00A550', '#00B5EF', '#D4AF37', '#6c757d']

        fig_payment = go.Figure(data=[go.Pie(
            labels=payment_summary['Jenis Pembayaran'],
            values=payment_summary['Total Penerimaan'],
            hole=0.5,
            marker=dict(colors=colors_pie[:len(payment_summary)], line=dict(color='white', width=2)),
            textinfo='percent+label',
            textposition='outside',
            textfont=dict(size=12),
            hovertemplate='<b>%{label}</b><br>Total: Rp %{value:,.0f}<br>Persentase: %{percent}<extra></extra>'
        )])

        fig_payment.update_layout(
            height=350,
            margin=dict(l=20, r=20, t=30, b=20),
            showlegend=False,
            annotations=[dict(text=f'<b>{format_rupiah_short(total_all)}</b>', x=0.5, y=0.5, font_size=14, showarrow=False)],
            paper_bgcolor='white'
        )
        st.plotly_chart(fig_payment, use_container_width=True)

        # Payment table
        payment_display = payment_summary.copy()
        payment_display['Total Penerimaan'] = payment_display['Total Penerimaan'].apply(format_rupiah)
        payment_display['Persentase'] = payment_display['Persentase'].apply(lambda x: f"{x:.2f}%")
        st.dataframe(payment_display, use_container_width=True, hide_index=True)

    with col2:
        st.markdown('<div class="section-header">📈 Tren Penerimaan Harian</div>', unsafe_allow_html=True)

        daily_trend = df_filtered.groupby('TANGGAL').agg({
            'RPPOKOK': 'sum',
            'KDBILL': 'count'
        }).reset_index()
        daily_trend.columns = ['Tanggal', 'Total Penerimaan', 'Jumlah STS']

        fig_trend = go.Figure()

        fig_trend.add_trace(go.Scatter(
            x=daily_trend['Tanggal'],
            y=daily_trend['Total Penerimaan'],
            mode='lines+markers',
            name='Total Penerimaan',
            line=dict(color='#00688B', width=2.5),
            marker=dict(size=6, color='#00688B'),
            fill='tozeroy',
            fillcolor='rgba(0, 104, 139, 0.1)',
            hovertemplate='<b>%{x|%d %b %Y}</b><br>Total: Rp %{y:,.0f}<extra></extra>'
        ))

        fig_trend.update_layout(
            height=400,
            margin=dict(l=10, r=10, t=20, b=10),
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis=dict(
                title='Tanggal',
                gridcolor='#eee',
                showline=True,
                linecolor='#ddd'
            ),
            yaxis=dict(
                title='Total Penerimaan (Rp)',
                gridcolor='#eee',
                showline=True,
                linecolor='#ddd'
            ),
            hovermode='x unified',
            font=dict(family='Inter, sans-serif')
        )
        st.plotly_chart(fig_trend, use_container_width=True)

    # Section 3: Rekap Bulanan
    st.markdown('<div class="section-header">📆 Rekap Penerimaan Bulanan</div>', unsafe_allow_html=True)

    monthly_summary = df_filtered.groupby(['TAHUN', 'BULAN']).agg({
        'RPPOKOK': 'sum',
        'KDBILL': 'count'
    }).reset_index()
    monthly_summary.columns = ['Tahun', 'Bulan', 'Total Penerimaan', 'Jumlah STS']

    months_name = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'Mei', 6:'Jun', 7:'Jul', 8:'Agu', 9:'Sep', 10:'Okt', 11:'Nov', 12:'Des'}
    monthly_summary['Nama Bulan'] = monthly_summary['Bulan'].map(months_name)
    monthly_summary['Periode'] = monthly_summary['Nama Bulan'] + ' ' + monthly_summary['Tahun'].astype(str)

    fig_monthly = go.Figure()

    fig_monthly.add_trace(go.Bar(
        x=monthly_summary['Periode'],
        y=monthly_summary['Total Penerimaan'],
        marker=dict(
            color=monthly_summary['Total Penerimaan'],
            colorscale=[[0, '#00A550'], [0.5, '#00B5EF'], [1, '#00688B']],
            line=dict(color='white', width=1)
        ),
        text=monthly_summary['Total Penerimaan'].apply(format_rupiah_short),
        textposition='outside',
        textfont=dict(size=10),
        hovertemplate='<b>%{x}</b><br>Total: %{text}<br>Jumlah STS: %{customdata}<extra></extra>',
        customdata=monthly_summary['Jumlah STS']
    ))

    fig_monthly.update_layout(
        height=350,
        margin=dict(l=10, r=10, t=20, b=10),
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(title='', gridcolor='#eee', tickangle=-45),
        yaxis=dict(title='Total Penerimaan (Rp)', gridcolor='#eee'),
        font=dict(family='Inter, sans-serif')
    )
    st.plotly_chart(fig_monthly, use_container_width=True)

    # Section 4: Detail Data
    st.markdown('<div class="section-header">📋 Detail Data</div>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📊 Rekap per OPD", "📄 Daftar Transaksi STS", "👤 Rekap per Kasir"])

    with tab1:
        opd_detail = df_filtered.groupby('NAMA_OPD').agg({
            'RPPOKOK': ['sum', 'count', 'mean', 'min', 'max']
        }).reset_index()
        opd_detail.columns = ['Nama OPD', 'Total Penerimaan', 'Jumlah STS', 'Rata-rata', 'Minimum', 'Maksimum']
        opd_detail = opd_detail.sort_values('Total Penerimaan', ascending=False)

        opd_detail_display = opd_detail.copy()
        for col in ['Total Penerimaan', 'Rata-rata', 'Minimum', 'Maksimum']:
            opd_detail_display[col] = opd_detail_display[col].apply(format_rupiah)

        st.dataframe(opd_detail_display, use_container_width=True, hide_index=True, height=400)

        csv = opd_detail.to_csv(index=False)
        st.download_button(
            label="📥 Download Rekap OPD (CSV)",
            data=csv,
            file_name=f"rekap_opd_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

    with tab2:
        display_cols = ['KDBILL', 'TGTERIMA', 'NAMA_OPD', 'RPPOKOK', 'JENIS_PEMBAYARAN', 'NAMA_KASIR', 'KETUM']
        sts_display = df_filtered[display_cols].copy()
        sts_display.columns = ['Kode Billing', 'Tanggal Terima', 'OPD', 'Nominal', 'Jenis Bayar', 'Kasir', 'Keterangan']
        sts_display['Nominal'] = sts_display['Nominal'].apply(format_rupiah)
        sts_display = sts_display.sort_values('Tanggal Terima', ascending=False)

        st.dataframe(sts_display.head(500), use_container_width=True, hide_index=True, height=400)
        st.caption(f"Menampilkan 500 dari {len(sts_display):,} transaksi")

        csv_full = df_filtered.to_csv(index=False)
        st.download_button(
            label="📥 Download Semua Transaksi (CSV)",
            data=csv_full,
            file_name=f"transaksi_sts_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

    with tab3:
        kasir_detail = df_filtered.groupby(['NAMA_KASIR', 'NIP_KASIR']).agg({
            'RPPOKOK': ['sum', 'count'],
            'NAMA_OPD': lambda x: x.mode()[0] if len(x.mode()) > 0 else 'N/A'
        }).reset_index()
        kasir_detail.columns = ['Nama Kasir', 'NIP', 'Total Penerimaan', 'Jumlah STS', 'OPD']
        kasir_detail = kasir_detail.sort_values('Total Penerimaan', ascending=False)
        kasir_detail['Total Penerimaan'] = kasir_detail['Total Penerimaan'].apply(format_rupiah)

        st.dataframe(kasir_detail.head(100), use_container_width=True, hide_index=True, height=400)

    # Footer
    footer_html = f"""
    <div class="footer">
        <p class="footer-title">📊 Aplikasi Monitoring STS - Retribusi & PAD</p>
        <p class="footer-subtitle">Badan Pendapatan Daerah Provinsi Jawa Timur</p>
        <p class="footer-subtitle">© {datetime.now().year} BAPENDA Jatim. All Rights Reserved.</p>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
