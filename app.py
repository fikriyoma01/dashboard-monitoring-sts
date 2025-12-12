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

# Login credentials
LOGIN_USERNAME = "bapendaptip"
LOGIN_PASSWORD = "ptipbapenda2025"

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

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

# Custom CSS with Jawa Timur Theme - Improved Typography
st.markdown(f"""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    /* Global Styles */
    html, body, .stApp {{
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        font-size: 16px;
        line-height: 1.6;
    }}

    /* Header Styling */
    .main-header {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['dark']} 100%);
        padding: 1.25rem 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.25rem;
        box-shadow: 0 4px 12px rgba(0, 104, 139, 0.25);
        display: flex;
        align-items: center;
        gap: 16px;
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
        font-size: 1.75rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.3px;
    }}

    .header-subtitle {{
        color: {COLORS['accent']};
        font-size: 1.1rem;
        margin: 6px 0 0 0;
        font-weight: 500;
    }}

    .header-org {{
        color: {COLORS['gold']};
        font-size: 0.95rem;
        margin: 4px 0 0 0;
        font-weight: 600;
        letter-spacing: 0.5px;
    }}

    /* Metric Cards */
    .metric-container {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1.25rem;
        margin-bottom: 1.5rem;
    }}

    .metric-card {{
        background: linear-gradient(145deg, {COLORS['white']} 0%, {COLORS['light_bg']} 100%);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 3px 12px rgba(0,0,0,0.08);
        border-left: 5px solid {COLORS['primary']};
        transition: transform 0.2s, box-shadow 0.2s;
    }}

    .metric-card:hover {{
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.12);
    }}

    .metric-card.green {{ border-left-color: {COLORS['secondary']}; }}
    .metric-card.gold {{ border-left-color: {COLORS['gold']}; }}
    .metric-card.accent {{ border-left-color: {COLORS['accent']}; }}

    .metric-icon {{
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }}

    .metric-value {{
        font-size: 1.75rem;
        font-weight: 700;
        color: {COLORS['dark']};
        margin: 0;
        letter-spacing: -0.5px;
    }}

    .metric-label {{
        font-size: 1rem;
        color: #555;
        margin: 0.25rem 0 0 0;
        font-weight: 500;
    }}

    /* Section Headers */
    .section-header {{
        background: linear-gradient(90deg, {COLORS['primary']} 0%, {COLORS['accent']} 100%);
        color: white;
        padding: 0.875rem 1.25rem;
        border-radius: 8px;
        margin: 1.5rem 0 1rem 0;
        font-weight: 600;
        font-size: 1.15rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }}

    /* Info Box */
    .info-box {{
        background: linear-gradient(135deg, {COLORS['light_bg']} 0%, #E6F3FF 100%);
        border: 1px solid rgba(0, 181, 239, 0.3);
        border-radius: 10px;
        padding: 1rem 1.5rem;
        margin-bottom: 1.25rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 1rem;
    }}

    .info-item {{
        display: flex;
        align-items: center;
        gap: 10px;
    }}

    .info-icon {{
        font-size: 1.5rem;
    }}

    .info-label {{
        color: #666;
        font-size: 0.9rem;
        font-weight: 500;
    }}

    .info-value {{
        color: {COLORS['primary']};
        font-weight: 700;
        font-size: 1.1rem;
    }}

    /* Chart Container */
    .chart-container {{
        background: white;
        border-radius: 12px;
        padding: 1.25rem;
        box-shadow: 0 3px 10px rgba(0,0,0,0.06);
        margin-bottom: 1rem;
    }}

    /* Table Styling */
    .stDataFrame {{
        font-size: 0.95rem;
    }}

    .stDataFrame td, .stDataFrame th {{
        padding: 0.75rem 1rem !important;
        font-size: 0.95rem !important;
    }}

    /* Footer */
    .footer {{
        background: linear-gradient(135deg, {COLORS['dark']} 0%, {COLORS['primary']} 100%);
        color: white;
        text-align: center;
        padding: 1.75rem;
        border-radius: 12px;
        margin-top: 2rem;
    }}

    .footer p {{
        margin: 0.35rem 0;
    }}

    .footer-title {{
        font-weight: 600;
        font-size: 1.15rem;
        color: {COLORS['gold']};
    }}

    .footer-subtitle {{
        font-size: 0.95rem;
        color: #ccc;
    }}

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {COLORS['light_bg']} 0%, white 100%);
    }}

    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stMultiSelect label {{
        color: {COLORS['primary']};
        font-weight: 600;
        font-size: 1rem;
    }}

    section[data-testid="stSidebar"] .stMarkdown p {{
        font-size: 1rem;
    }}

    section[data-testid="stSidebar"] h3 {{
        font-size: 1.25rem !important;
        margin-bottom: 0.75rem;
    }}

    /* Hide Streamlit Branding */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}

    /* Custom Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 6px;
    }}

    .stTabs [data-baseweb="tab"] {{
        background: {COLORS['light_bg']};
        border-radius: 8px 8px 0 0;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 1rem;
    }}

    .stTabs [aria-selected="true"] {{
        background: {COLORS['primary']};
        color: white;
    }}

    /* Plotly Chart Font Override */
    .js-plotly-plot .plotly .gtitle {{
        font-size: 16px !important;
    }}

    /* Download Button */
    .stDownloadButton button {{
        font-size: 1rem;
        padding: 0.75rem 1.5rem;
    }}

    /* Caption */
    .stCaption {{
        font-size: 0.9rem;
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

    # Exclude Badan Pendapatan Daerah (BAPENDA) from the data
    df = df[~df['NAMA_OPD'].str.contains('Badan Pendapatan Daerah', case=False, na=False)]

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

def show_login_page():
    """Display login page"""
    # Custom CSS for login page
    st.markdown(f"""
    <style>
        .login-container {{
            max-width: 450px;
            margin: 100px auto;
            padding: 40px;
            background: linear-gradient(145deg, {COLORS['white']} 0%, {COLORS['light_bg']} 100%);
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0, 104, 139, 0.15);
            border-top: 5px solid {COLORS['primary']};
        }}

        .login-header {{
            text-align: center;
            margin-bottom: 30px;
        }}

        .login-logo {{
            width: 100px;
            margin-bottom: 20px;
        }}

        .login-title {{
            color: {COLORS['primary']};
            font-size: 1.8rem;
            font-weight: 700;
            margin-bottom: 8px;
        }}

        .login-subtitle {{
            color: {COLORS['dark']};
            font-size: 1rem;
            font-weight: 500;
        }}

        .login-org {{
            color: {COLORS['gold']};
            font-size: 0.9rem;
            font-weight: 600;
            margin-top: 5px;
        }}
    </style>
    """, unsafe_allow_html=True)

    # Login container
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        # Logo and header
        logo_path = os.path.join(ASSETS_DIR, "logo_jawa-timur.svg")
        if os.path.exists(logo_path):
            st.image(logo_path, width=120)

        st.markdown(f"""
        <div class="login-header">
            <h1 class="login-title">🔐 Login Sistem</h1>
            <p class="login-subtitle">Monitoring STS - Retribusi & PAD</p>
            <p class="login-org">BAPENDA JAWA TIMUR</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Login form
        with st.form("login_form"):
            username = st.text_input("👤 Username", placeholder="Masukkan username")
            password = st.text_input("🔒 Password", type="password", placeholder="Masukkan password")

            submit_button = st.form_submit_button("🚀 Masuk", use_container_width=True)

            if submit_button:
                if username == LOGIN_USERNAME and password == LOGIN_PASSWORD:
                    st.session_state.logged_in = True
                    st.success("✅ Login berhasil! Mengalihkan ke dashboard...")
                    st.rerun()
                else:
                    st.error("❌ Username atau password salah!")

        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="text-align: center; color: #666; font-size: 0.85rem;">
            <p>© {datetime.now().year} Badan Pendapatan Daerah Provinsi Jawa Timur</p>
            <p>Pengembangan Teknologi Informasi Pendapatan (PTIP)</p>
        </div>
        """, unsafe_allow_html=True)

def logout():
    """Logout function"""
    st.session_state.logged_in = False
    st.rerun()

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

        # Logout button
        if st.button("🚪 Logout", use_container_width=True, type="primary"):
            logout()

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

    # Determine scale based on max value
    max_value = opd_summary['Total Penerimaan'].max()
    if max_value >= 1e9:  # Milyar
        scale_factor = 1e9
        scale_suffix = ' M'
        scale_label = '(Rp dalam Milyar)'
    else:  # Juta
        scale_factor = 1e6
        scale_suffix = ' Jt'
        scale_label = '(Rp dalam Juta)'

    fig_opd = go.Figure()
    fig_opd.add_trace(go.Bar(
        y=opd_summary['OPD'],
        x=opd_summary['Total Penerimaan'] / scale_factor,
        orientation='h',
        marker=dict(
            color=opd_summary['Total Penerimaan'],
            colorscale=[[0, '#E6F3FF'], [0.5, '#00B5EF'], [1, '#00688B']],
            line=dict(color='#00688B', width=1)
        ),
        text=opd_summary['Total Penerimaan'].apply(format_rupiah_short),
        textposition='outside',
        textfont=dict(size=14, color='#333', family='Plus Jakarta Sans'),
        hovertemplate='<b>%{y}</b><br>Total: %{text}<br>Jumlah STS: %{customdata}<extra></extra>',
        customdata=opd_summary['Jumlah STS']
    ))

    fig_opd.update_layout(
        height=500,
        margin=dict(l=10, r=120, t=20, b=20),
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(
            title=dict(text=f'Total Penerimaan {scale_label}', font=dict(size=14)),
            gridcolor='#eee',
            showline=True,
            linecolor='#ddd',
            tickfont=dict(size=13),
            tickformat='.0f',
            ticksuffix=scale_suffix,
            range=[0, (max_value / scale_factor) * 1.15]
        ),
        yaxis=dict(
            title='',
            showgrid=False,
            tickfont=dict(size=13)
        ),
        font=dict(family='Plus Jakarta Sans, sans-serif', size=14)
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
            textfont=dict(size=14, family='Plus Jakarta Sans'),
            hovertemplate='<b>%{label}</b><br>Total: Rp %{value:,.0f}<br>Persentase: %{percent}<extra></extra>'
        )])

        fig_payment.update_layout(
            height=380,
            margin=dict(l=20, r=20, t=25, b=20),
            showlegend=False,
            annotations=[dict(text=f'<b>{format_rupiah_short(total_all)}</b>', x=0.5, y=0.5, font_size=16, showarrow=False)],
            paper_bgcolor='white',
            font=dict(family='Plus Jakarta Sans, sans-serif', size=14)
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

        # Determine scale based on max value
        max_value_daily = daily_trend['Total Penerimaan'].max()
        if max_value_daily >= 1e9:  # Milyar
            scale_factor_daily = 1e9
            scale_suffix_daily = ' M'
            scale_label_daily = '(Rp dalam Milyar)'
        else:  # Juta
            scale_factor_daily = 1e6
            scale_suffix_daily = ' Jt'
            scale_label_daily = '(Rp dalam Juta)'

        fig_trend = go.Figure()

        fig_trend.add_trace(go.Scatter(
            x=daily_trend['Tanggal'],
            y=daily_trend['Total Penerimaan'] / scale_factor_daily,
            mode='lines+markers',
            name='Total Penerimaan',
            line=dict(color='#00688B', width=3),
            marker=dict(size=6, color='#00688B'),
            fill='tozeroy',
            fillcolor='rgba(0, 104, 139, 0.1)',
            hovertemplate='<b>%{x|%d %b %Y}</b><br>Total: Rp %{y:,.0f}<extra></extra>'
        ))

        fig_trend.update_layout(
            height=420,
            margin=dict(l=15, r=15, t=20, b=15),
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis=dict(
                title=dict(text='Tanggal', font=dict(size=14)),
                gridcolor='#eee',
                showline=True,
                linecolor='#ddd',
                tickfont=dict(size=12)
            ),
            yaxis=dict(
                title=dict(text=f'Total Penerimaan {scale_label_daily}', font=dict(size=14)),
                gridcolor='#eee',
                showline=True,
                linecolor='#ddd',
                tickfont=dict(size=12),
                tickformat='.0f',
                ticksuffix=scale_suffix_daily,
                range=[0, (max_value_daily / scale_factor_daily) * 1.1]
            ),
            hovermode='x unified',
            font=dict(family='Plus Jakarta Sans, sans-serif', size=14)
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

    # Determine scale based on max value
    max_value_monthly = monthly_summary['Total Penerimaan'].max()
    if max_value_monthly >= 1e9:  # Milyar
        scale_factor_monthly = 1e9
        scale_suffix_monthly = ' M'
        scale_label_monthly = '(Rp dalam Milyar)'
    else:  # Juta
        scale_factor_monthly = 1e6
        scale_suffix_monthly = ' Jt'
        scale_label_monthly = '(Rp dalam Juta)'

    fig_monthly = go.Figure()

    fig_monthly.add_trace(go.Bar(
        x=monthly_summary['Periode'],
        y=monthly_summary['Total Penerimaan'] / scale_factor_monthly,
        marker=dict(
            color=monthly_summary['Total Penerimaan'],
            colorscale=[[0, '#00A550'], [0.5, '#00B5EF'], [1, '#00688B']],
            line=dict(color='white', width=1)
        ),
        text=monthly_summary['Total Penerimaan'].apply(format_rupiah_short),
        textposition='outside',
        textfont=dict(size=13, family='Plus Jakarta Sans'),
        hovertemplate='<b>%{x}</b><br>Total: %{text}<br>Jumlah STS: %{customdata}<extra></extra>',
        customdata=monthly_summary['Jumlah STS']
    ))

    fig_monthly.update_layout(
        height=380,
        margin=dict(l=15, r=15, t=60, b=15),
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(title='', gridcolor='#eee', tickangle=-45, tickfont=dict(size=13)),
        yaxis=dict(
            title=dict(text=f'Total Penerimaan {scale_label_monthly}', font=dict(size=14)),
            gridcolor='#eee',
            tickfont=dict(size=12),
            tickformat='.0f',
            ticksuffix=scale_suffix_monthly,
            range=[0, (max_value_monthly / scale_factor_monthly) * 1.2]
        ),
        font=dict(family='Plus Jakarta Sans, sans-serif', size=14)
    )
    st.plotly_chart(fig_monthly, use_container_width=True)

    # Section 4: Detail Data
    st.markdown('<div class="section-header">📋 Detail Data</div>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📊 Rekap per OPD", "📄 Daftar Transaksi STS", "👤 Rekap per Bendahara"])

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
        # Info box untuk menjelaskan perbedaan tanggal
        st.markdown("""
        <div style="background: linear-gradient(135deg, #e3f2fd 0%, #fff3e0 100%); padding: 1.25rem; border-radius: 10px; margin-bottom: 1.25rem; border-left: 5px solid #00688B; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
            <p style="margin: 0; font-weight: 700; color: #00688B; font-size: 1rem;">📋 Keterangan Jenis Tanggal:</p>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-top: 1rem;">
                <div style="background: #fff; padding: 1rem; border-radius: 8px; border-left: 4px solid #2196F3; box-shadow: 0 1px 4px rgba(0,0,0,0.05);">
                    <p style="margin: 0; font-weight: 700; color: #2196F3; font-size: 0.9rem;">📥 Tanggal Terima</p>
                    <p style="margin: 0.5rem 0 0 0; font-size: 0.85rem; color: #333; line-height: 1.5;">
                        <strong>Dana diterima bendahara</strong><br>
                        <span style="color: #666;">Tanggal saat dana dari wajib retribusi diterima oleh bendahara penerimaan.</span>
                    </p>
                </div>
                <div style="background: #fff; padding: 1rem; border-radius: 8px; border-left: 4px solid #FF9800; box-shadow: 0 1px 4px rgba(0,0,0,0.05);">
                    <p style="margin: 0; font-weight: 700; color: #FF9800; font-size: 0.9rem;">💰 Tanggal Setor</p>
                    <p style="margin: 0.5rem 0 0 0; font-size: 0.85rem; color: #333; line-height: 1.5;">
                        <strong>Dana disetor bendahara ke RKUD</strong><br>
                        <span style="color: #666;">Tanggal saat bendahara menyetorkan dana ke Rekening Kas Umum Daerah (RKUD).</span>
                    </p>
                </div>
                <div style="background: #fff; padding: 1rem; border-radius: 8px; border-left: 4px solid #4CAF50; box-shadow: 0 1px 4px rgba(0,0,0,0.05);">
                    <p style="margin: 0; font-weight: 700; color: #4CAF50; font-size: 0.9rem;">✅ Tanggal Validasi Bank</p>
                    <p style="margin: 0.5rem 0 0 0; font-size: 0.85rem; color: #333; line-height: 1.5;">
                        <strong>Pengakuan dana masuk ke RKUD dari Bank Jatim</strong><br>
                        <span style="color: #666;">Tanggal validasi/konfirmasi dari Bank Jatim bahwa dana sudah masuk ke RKUD.</span>
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        display_cols = ['KDBILL', 'TGTERIMA', 'TGSETOR', 'TGVALIDBANK', 'NAMA_OPD', 'RPPOKOK', 'JENIS_PEMBAYARAN', 'NAMA_KASIR', 'KETUM']
        sts_display = df_filtered[display_cols].copy()
        sts_display.columns = ['Kode Billing', '📥 Tgl Terima', '💰 Tgl Setor', '✅ Tgl Valid Bank', 'OPD', 'Nominal', 'Jenis Bayar', 'Bendahara', 'Keterangan']

        # Format tanggal dengan lebih detail
        for col in ['📥 Tgl Terima', '💰 Tgl Setor', '✅ Tgl Valid Bank']:
            sts_display[col] = pd.to_datetime(sts_display[col]).dt.strftime('%d/%m/%Y')

        sts_display['Nominal'] = sts_display['Nominal'].apply(format_rupiah)
        sts_display = sts_display.sort_values('📥 Tgl Terima', ascending=False)

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
        bendahara_detail = df_filtered.groupby(['NAMA_KASIR', 'NIP_KASIR']).agg({
            'RPPOKOK': ['sum', 'count'],
            'NAMA_OPD': lambda x: x.mode()[0] if len(x.mode()) > 0 else 'N/A'
        }).reset_index()
        bendahara_detail.columns = ['Nama Bendahara', 'NIP', 'Total Penerimaan', 'Jumlah STS', 'OPD']
        bendahara_detail = bendahara_detail.sort_values('Total Penerimaan', ascending=False)
        bendahara_detail['Total Penerimaan'] = bendahara_detail['Total Penerimaan'].apply(format_rupiah)

        st.dataframe(bendahara_detail.head(100), use_container_width=True, hide_index=True, height=400)

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
    # Check login status
    if not st.session_state.logged_in:
        show_login_page()
    else:
        main()
