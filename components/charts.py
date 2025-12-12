"""
Chart Components using Plotly
"""

import plotly.express as px
import plotly.graph_objects as go
from dash import dcc
import pandas as pd

from config import COLORS, CHART_COLORS, CHART_COLORSCALE, PLOTLY_LAYOUT, PLOTLY_CONFIG
from utils.formatters import format_rupiah_short, scale_value


def create_opd_chart(df: pd.DataFrame, top_n: int = 15):
    """
    Create horizontal bar chart for OPD penerimaan

    Args:
        df: DataFrame with columns ['nama_opd', 'total', 'jumlah']
        top_n: Number of top OPD to show
    """
    if df.empty:
        return _create_empty_chart("Tidak ada data OPD")

    # Get top N
    chart_data = df.nlargest(top_n, 'total').sort_values('total', ascending=True)

    # Determine scale
    max_value = chart_data['total'].max()
    scale_factor, scale_suffix, scale_label = scale_value(max_value)

    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=chart_data['nama_opd'],
        x=chart_data['total'] / scale_factor,
        orientation='h',
        marker=dict(
            color=chart_data['total'],
            colorscale=CHART_COLORSCALE,
            line=dict(color=COLORS['primary'], width=1)
        ),
        text=chart_data['total'].apply(format_rupiah_short),
        textposition='outside',
        textfont=dict(size=12, color=COLORS['text_primary']),
        hovertemplate='<b>%{y}</b><br>' +
                      'Total: %{text}<br>' +
                      'Jumlah STS: %{customdata}<extra></extra>',
        customdata=chart_data['jumlah']
    ))

    fig.update_layout(
        **PLOTLY_LAYOUT,
        height=450,
        margin=dict(l=10, r=100, t=10, b=40),
        xaxis=dict(
            title=dict(text=f'Total Penerimaan {scale_label}', font=dict(size=13)),
            gridcolor='#eee',
            showline=True,
            linecolor='#ddd',
            tickformat='.0f',
            ticksuffix=scale_suffix,
            range=[0, (max_value / scale_factor) * 1.15]
        ),
        yaxis=dict(
            title='',
            showgrid=False,
            tickfont=dict(size=11)
        ),
        bargap=0.3
    )

    return dcc.Graph(
        figure=fig,
        config=PLOTLY_CONFIG,
        style={'height': '100%'}
    )


def create_payment_chart(df: pd.DataFrame):
    """
    Create donut chart for payment types

    Args:
        df: DataFrame with columns ['jenis_pembayaran', 'total', 'jumlah', 'persentase']
    """
    if df.empty:
        return _create_empty_chart("Tidak ada data pembayaran")

    total_all = df['total'].sum()

    fig = go.Figure(data=[go.Pie(
        labels=df['jenis_pembayaran'],
        values=df['total'],
        hole=0.5,
        marker=dict(
            colors=CHART_COLORS[:len(df)],
            line=dict(color=COLORS['white'], width=2)
        ),
        textinfo='percent+label',
        textposition='outside',
        textfont=dict(size=12),
        hovertemplate='<b>%{label}</b><br>' +
                      'Total: Rp %{value:,.0f}<br>' +
                      'Persentase: %{percent}<extra></extra>'
    )])

    fig.update_layout(
        **PLOTLY_LAYOUT,
        height=350,
        margin=dict(l=20, r=20, t=20, b=20),
        showlegend=False,
        annotations=[dict(
            text=f'<b>{format_rupiah_short(total_all)}</b>',
            x=0.5, y=0.5,
            font_size=14,
            showarrow=False
        )]
    )

    return dcc.Graph(
        figure=fig,
        config=PLOTLY_CONFIG,
        style={'height': '100%'}
    )


def create_trend_chart(df: pd.DataFrame):
    """
    Create line chart for daily trend

    Args:
        df: DataFrame with columns ['tanggal', 'total', 'jumlah']
    """
    if df.empty:
        return _create_empty_chart("Tidak ada data tren")

    max_value = df['total'].max()
    scale_factor, scale_suffix, scale_label = scale_value(max_value)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df['tanggal'],
        y=df['total'] / scale_factor,
        mode='lines+markers',
        name='Total Penerimaan',
        line=dict(color=COLORS['primary'], width=3),
        marker=dict(size=6, color=COLORS['primary']),
        fill='tozeroy',
        fillcolor=f'rgba(0, 104, 139, 0.1)',
        hovertemplate='<b>%{x|%d %b %Y}</b><br>' +
                      f'Total: Rp %{{y:,.0f}}{scale_suffix}<br>' +
                      '<extra></extra>'
    ))

    fig.update_layout(
        **PLOTLY_LAYOUT,
        height=380,
        margin=dict(l=15, r=15, t=10, b=40),
        xaxis=dict(
            title=dict(text='Tanggal', font=dict(size=13)),
            gridcolor='#eee',
            showline=True,
            linecolor='#ddd'
        ),
        yaxis=dict(
            title=dict(text=f'Total Penerimaan {scale_label}', font=dict(size=13)),
            gridcolor='#eee',
            showline=True,
            linecolor='#ddd',
            tickformat='.0f',
            ticksuffix=scale_suffix,
            range=[0, (max_value / scale_factor) * 1.1]
        ),
        hovermode='x unified'
    )

    return dcc.Graph(
        figure=fig,
        config=PLOTLY_CONFIG,
        style={'height': '100%'}
    )


def create_monthly_chart(df: pd.DataFrame):
    """
    Create bar chart for monthly summary

    Args:
        df: DataFrame with columns ['periode', 'total', 'jumlah']
    """
    if df.empty:
        return _create_empty_chart("Tidak ada data bulanan")

    max_value = df['total'].max()
    scale_factor, scale_suffix, scale_label = scale_value(max_value)

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df['periode'],
        y=df['total'] / scale_factor,
        marker=dict(
            color=df['total'],
            colorscale=[[0, COLORS['secondary']], [0.5, COLORS['accent']], [1, COLORS['primary']]],
            line=dict(color=COLORS['white'], width=1)
        ),
        text=df['total'].apply(format_rupiah_short),
        textposition='outside',
        textfont=dict(size=11),
        hovertemplate='<b>%{x}</b><br>' +
                      'Total: %{text}<br>' +
                      'Jumlah STS: %{customdata}<extra></extra>',
        customdata=df['jumlah']
    ))

    fig.update_layout(
        **PLOTLY_LAYOUT,
        height=350,
        margin=dict(l=15, r=15, t=40, b=60),
        xaxis=dict(
            title='',
            gridcolor='#eee',
            tickangle=-45,
            tickfont=dict(size=11)
        ),
        yaxis=dict(
            title=dict(text=f'Total Penerimaan {scale_label}', font=dict(size=13)),
            gridcolor='#eee',
            tickformat='.0f',
            ticksuffix=scale_suffix,
            range=[0, (max_value / scale_factor) * 1.2]
        ),
        bargap=0.3
    )

    return dcc.Graph(
        figure=fig,
        config=PLOTLY_CONFIG,
        style={'height': '100%'}
    )


def create_comparison_chart(df: pd.DataFrame, compare_by: str = 'year'):
    """
    Create comparison chart (year over year or month over month)

    Args:
        df: Source DataFrame
        compare_by: 'year' or 'month'
    """
    if df.empty:
        return _create_empty_chart("Tidak ada data perbandingan")

    # Implementation depends on specific comparison needs
    # This is a placeholder for future enhancement

    return _create_empty_chart("Fitur dalam pengembangan")


def create_heatmap_chart(df: pd.DataFrame):
    """
    Create heatmap for daily activity

    Args:
        df: DataFrame with transaction data
    """
    if df.empty:
        return _create_empty_chart("Tidak ada data aktivitas")

    # Group by day of week and hour (if available)
    # This is a placeholder for future enhancement

    return _create_empty_chart("Fitur dalam pengembangan")


def _create_empty_chart(message: str = "Tidak ada data"):
    """Create an empty chart placeholder"""
    fig = go.Figure()

    fig.add_annotation(
        text=message,
        xref='paper',
        yref='paper',
        x=0.5, y=0.5,
        showarrow=False,
        font=dict(size=16, color=COLORS['text_secondary'])
    )

    fig.update_layout(
        **PLOTLY_LAYOUT,
        height=300,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False)
    )

    return dcc.Graph(
        figure=fig,
        config=PLOTLY_CONFIG
    )
