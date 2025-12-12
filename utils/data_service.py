"""
Data Service - Database queries and data processing
"""

import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy import func, and_, or_, extract
from typing import Optional, List, Tuple
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import PAYMENT_TYPES, MONTH_NAMES, MONTH_NAMES_SHORT


class DataService:
    """Service class for data operations"""

    def __init__(self):
        self._cached_data = None
        self._cache_time = None
        self._cache_duration = 60  # seconds

    def _get_session(self):
        """Get database session"""
        from database.connection import get_db_session
        return get_db_session()

    def _should_refresh_cache(self):
        """Check if cache should be refreshed"""
        if self._cached_data is None:
            return True
        if self._cache_time is None:
            return True
        return (datetime.now() - self._cache_time).seconds > self._cache_duration

    def get_all_transactions(self, use_cache: bool = True) -> pd.DataFrame:
        """
        Get all transactions with related data

        Args:
            use_cache: Whether to use cached data

        Returns:
            DataFrame with all transactions
        """
        if use_cache and not self._should_refresh_cache():
            return self._cached_data.copy()

        session = self._get_session()

        try:
            from database.schema import Transaksi, OPD, Bendahara, Rekening

            query = session.query(
                Transaksi.id,
                Transaksi.kode_billing,
                Transaksi.tanggal_terima,
                Transaksi.tanggal_setor,
                Transaksi.tanggal_validasi_bank,
                Transaksi.nominal,
                Transaksi.jenis_pembayaran,
                Transaksi.keterangan_umum,
                Transaksi.keterangan_khusus,
                Transaksi.ayat,
                OPD.kode_opd,
                OPD.nama_opd,
                Bendahara.nama.label('nama_kasir'),
                Bendahara.nip.label('nip_kasir'),
                Rekening.kode_rekening,
                Rekening.nama_rekening
            ).outerjoin(
                OPD, Transaksi.opd_id == OPD.id
            ).outerjoin(
                Bendahara, Transaksi.bendahara_id == Bendahara.id
            ).outerjoin(
                Rekening, Transaksi.rekening_id == Rekening.id
            )

            df = pd.read_sql(query.statement, session.bind)

            # Process data
            df['tanggal_terima'] = pd.to_datetime(df['tanggal_terima'])
            df['tanggal_setor'] = pd.to_datetime(df['tanggal_setor'])
            df['tanggal_validasi_bank'] = pd.to_datetime(df['tanggal_validasi_bank'])

            # Add calculated columns
            df['tanggal'] = df['tanggal_terima'].dt.date
            df['tahun'] = df['tanggal_terima'].dt.year
            df['bulan'] = df['tanggal_terima'].dt.month
            df['nama_bulan'] = df['bulan'].map(MONTH_NAMES)
            df['minggu_tahun'] = df['tanggal_terima'].dt.isocalendar().week
            df['hari'] = df['tanggal_terima'].dt.day_name()
            df['jenis_pembayaran_nama'] = df['jenis_pembayaran'].map(PAYMENT_TYPES).fillna('Lainnya')

            # Fill missing OPD names
            df['nama_opd'] = df['nama_opd'].fillna('OPD Tidak Diketahui')

            # Exclude BAPENDA from analysis
            df = df[~df['nama_opd'].str.contains('Badan Pendapatan Daerah', case=False, na=False)]

            # Update cache
            self._cached_data = df
            self._cache_time = datetime.now()

            return df.copy()

        finally:
            session.close()

    def get_date_range(self) -> Tuple[datetime, datetime]:
        """Get min and max dates from transactions"""
        df = self.get_all_transactions()
        if df.empty:
            return datetime.now(), datetime.now()
        return df['tanggal_terima'].min(), df['tanggal_terima'].max()

    def get_opd_list(self) -> List[str]:
        """Get list of all OPD names"""
        df = self.get_all_transactions()
        return sorted(df['nama_opd'].dropna().unique().tolist())

    def get_payment_types(self) -> List[str]:
        """Get list of all payment types"""
        df = self.get_all_transactions()
        return sorted(df['jenis_pembayaran_nama'].dropna().unique().tolist())

    def filter_data(
        self,
        df: pd.DataFrame,
        period_type: str = "Semua Data",
        selected_date: Optional[datetime] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        selected_week: Optional[int] = None,
        selected_month: Optional[int] = None,
        selected_year: Optional[int] = None,
        selected_opd: Optional[List[str]] = None,
        selected_payment: Optional[str] = None
    ) -> Tuple[pd.DataFrame, str]:
        """
        Filter data based on various criteria

        Returns:
            Tuple of (filtered DataFrame, period label)
        """
        df_filtered = df.copy()
        period_label = "Semua Data"

        # Period filter
        if period_type == "Harian" and selected_date:
            df_filtered = df_filtered[df_filtered['tanggal'] == selected_date]
            period_label = selected_date.strftime('%d %B %Y') if hasattr(selected_date, 'strftime') else str(selected_date)

        elif period_type == "Mingguan" and selected_week and selected_year:
            df_filtered = df_filtered[
                (df_filtered['minggu_tahun'] == selected_week) &
                (df_filtered['tahun'] == selected_year)
            ]
            period_label = f"Minggu ke-{selected_week}, {selected_year}"

        elif period_type == "Bulanan" and selected_month and selected_year:
            df_filtered = df_filtered[
                (df_filtered['bulan'] == selected_month) &
                (df_filtered['tahun'] == selected_year)
            ]
            month_name = MONTH_NAMES.get(selected_month, str(selected_month))
            period_label = f"{month_name} {selected_year}"

        elif period_type == "Tahunan" and selected_year:
            df_filtered = df_filtered[df_filtered['tahun'] == selected_year]
            period_label = f"Tahun {selected_year}"

        elif period_type == "Rentang Tanggal" and start_date and end_date:
            df_filtered = df_filtered[
                (df_filtered['tanggal'] >= start_date) &
                (df_filtered['tanggal'] <= end_date)
            ]
            period_label = f"{start_date.strftime('%d/%m/%Y')} - {end_date.strftime('%d/%m/%Y')}"

        # OPD filter
        if selected_opd and 'Semua OPD' not in selected_opd:
            df_filtered = df_filtered[df_filtered['nama_opd'].isin(selected_opd)]

        # Payment type filter
        if selected_payment and selected_payment != 'Semua':
            df_filtered = df_filtered[df_filtered['jenis_pembayaran_nama'] == selected_payment]

        return df_filtered, period_label

    def get_summary_metrics(self, df: pd.DataFrame) -> dict:
        """
        Calculate summary metrics from DataFrame

        Returns:
            Dictionary with metric values
        """
        return {
            'total_penerimaan': df['nominal'].sum() if not df.empty else 0,
            'jumlah_sts': len(df),
            'rata_rata': df['nominal'].mean() if not df.empty else 0,
            'jumlah_opd': df['nama_opd'].nunique(),
            'min_nominal': df['nominal'].min() if not df.empty else 0,
            'max_nominal': df['nominal'].max() if not df.empty else 0,
        }

    def get_opd_summary(self, df: pd.DataFrame, top_n: int = 15) -> pd.DataFrame:
        """
        Get summary by OPD

        Args:
            df: Source DataFrame
            top_n: Number of top OPD to return

        Returns:
            DataFrame with OPD summary
        """
        if df.empty:
            return pd.DataFrame()

        summary = df.groupby('nama_opd').agg({
            'nominal': ['sum', 'count', 'mean', 'min', 'max']
        }).reset_index()

        summary.columns = ['nama_opd', 'total', 'jumlah', 'rata_rata', 'minimum', 'maksimum']
        summary = summary.sort_values('total', ascending=False)

        if top_n:
            return summary.head(top_n)
        return summary

    def get_payment_summary(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Get summary by payment type

        Returns:
            DataFrame with payment type summary
        """
        if df.empty:
            return pd.DataFrame()

        summary = df.groupby('jenis_pembayaran_nama').agg({
            'nominal': ['sum', 'count']
        }).reset_index()

        summary.columns = ['jenis_pembayaran', 'total', 'jumlah']
        summary['persentase'] = (summary['total'] / summary['total'].sum() * 100).round(2)
        summary = summary.sort_values('total', ascending=False)

        return summary

    def get_daily_trend(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Get daily trend data

        Returns:
            DataFrame with daily trend
        """
        if df.empty:
            return pd.DataFrame()

        trend = df.groupby('tanggal').agg({
            'nominal': 'sum',
            'kode_billing': 'count'
        }).reset_index()

        trend.columns = ['tanggal', 'total', 'jumlah']
        trend = trend.sort_values('tanggal')

        return trend

    def get_monthly_summary(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Get monthly summary data

        Returns:
            DataFrame with monthly summary
        """
        if df.empty:
            return pd.DataFrame()

        summary = df.groupby(['tahun', 'bulan']).agg({
            'nominal': 'sum',
            'kode_billing': 'count'
        }).reset_index()

        summary.columns = ['tahun', 'bulan', 'total', 'jumlah']
        summary['nama_bulan'] = summary['bulan'].map(MONTH_NAMES_SHORT)
        summary['periode'] = summary['nama_bulan'] + ' ' + summary['tahun'].astype(str)
        summary = summary.sort_values(['tahun', 'bulan'])

        return summary

    def get_bendahara_summary(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Get summary by bendahara

        Returns:
            DataFrame with bendahara summary
        """
        if df.empty:
            return pd.DataFrame()

        summary = df.groupby(['nama_kasir', 'nip_kasir']).agg({
            'nominal': ['sum', 'count'],
            'nama_opd': lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else 'N/A'
        }).reset_index()

        summary.columns = ['nama_kasir', 'nip_kasir', 'total', 'jumlah', 'opd']
        summary = summary.sort_values('total', ascending=False)

        return summary

    def get_transaction_detail(self, df: pd.DataFrame, limit: int = 500) -> pd.DataFrame:
        """
        Get transaction detail for display

        Args:
            df: Source DataFrame
            limit: Maximum rows to return

        Returns:
            DataFrame with transaction details
        """
        if df.empty:
            return pd.DataFrame()

        cols = [
            'kode_billing', 'tanggal_terima', 'tanggal_setor',
            'tanggal_validasi_bank', 'nama_opd', 'nominal',
            'jenis_pembayaran_nama', 'nama_kasir', 'keterangan_umum'
        ]

        detail = df[cols].copy()
        detail = detail.sort_values('tanggal_terima', ascending=False)

        if limit:
            return detail.head(limit)
        return detail

    def refresh_cache(self):
        """Force refresh the data cache"""
        self._cached_data = None
        self._cache_time = None
        return self.get_all_transactions(use_cache=False)


# Singleton instance
_data_service = None


def get_data_service() -> DataService:
    """Get the singleton data service instance"""
    global _data_service
    if _data_service is None:
        _data_service = DataService()
    return _data_service
