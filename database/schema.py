"""
Database Schema untuk Monitoring STS - BAPENDA Jawa Timur
Skema relasional dengan SQLAlchemy ORM
"""

from sqlalchemy import (
    create_engine, Column, Integer, String, Float, DateTime, Date,
    ForeignKey, Text, Boolean, Index, Numeric, Enum
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
import enum

Base = declarative_base()


class PaymentType(enum.Enum):
    """Enum untuk jenis pembayaran"""
    TUNAI = 1
    ESAMSAT_GIRO_TRANSFER = 2
    EDC = 3
    VIRTUAL_ACCOUNT = 4
    QRIS = 5


class User(Base):
    """Tabel users untuk autentikasi"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    nama_lengkap = Column(String(255))
    email = Column(String(255))
    role = Column(String(50), default='user')  # admin, user, viewer
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<User(username='{self.username}', role='{self.role}')>"


class OPD(Base):
    """Tabel Organisasi Perangkat Daerah"""
    __tablename__ = 'opd'

    id = Column(Integer, primary_key=True, autoincrement=True)
    kode_opd = Column(String(20), unique=True, nullable=False, index=True)
    nama_opd = Column(String(255), nullable=False)
    tahun = Column(Integer)
    kode_qrcode = Column(String(100))
    alamat = Column(Text)
    telepon = Column(String(50))
    email = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    transaksi = relationship("Transaksi", back_populates="opd")
    bendahara = relationship("Bendahara", back_populates="opd")

    def __repr__(self):
        return f"<OPD(kode='{self.kode_opd}', nama='{self.nama_opd}')>"


class Rekening(Base):
    """Tabel Rekening/Akun Penerimaan"""
    __tablename__ = 'rekening'

    id = Column(Integer, primary_key=True, autoincrement=True)
    kode_rekening = Column(String(50), unique=True, nullable=False, index=True)
    nama_rekening = Column(String(255))
    tahun = Column(Integer)
    skt = Column(String(50))
    prefix = Column(String(20))
    level = Column(Integer)  # Level hierarki rekening
    parent_kode = Column(String(50))  # Kode rekening parent
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    transaksi = relationship("Transaksi", back_populates="rekening")

    def __repr__(self):
        return f"<Rekening(kode='{self.kode_rekening}', nama='{self.nama_rekening}')>"


class Bendahara(Base):
    """Tabel Bendahara Penerimaan Pembantu (BPP)"""
    __tablename__ = 'bendahara'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_sibaku = Column(Integer, unique=True, nullable=False, index=True)
    nama = Column(String(255), nullable=False)
    nip = Column(String(50))
    ip_address = Column(String(50))
    opd_id = Column(Integer, ForeignKey('opd.id'))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    opd = relationship("OPD", back_populates="bendahara")
    transaksi = relationship("Transaksi", back_populates="bendahara")

    def __repr__(self):
        return f"<Bendahara(nama='{self.nama}', nip='{self.nip}')>"


class Transaksi(Base):
    """Tabel Transaksi STS (Surat Tanda Setoran)"""
    __tablename__ = 'transaksi'

    id = Column(Integer, primary_key=True, autoincrement=True)
    kode_billing = Column(String(50), unique=True, nullable=False, index=True)

    # Foreign Keys
    opd_id = Column(Integer, ForeignKey('opd.id'), index=True)
    rekening_id = Column(Integer, ForeignKey('rekening.id'), index=True)
    bendahara_id = Column(Integer, ForeignKey('bendahara.id'), index=True)

    # Data Transaksi
    ayat = Column(String(50))
    nominal = Column(Numeric(18, 2), nullable=False, default=0)

    # Tanggal-tanggal penting
    tanggal_terima = Column(DateTime, nullable=False, index=True)
    tanggal_setor = Column(DateTime)
    tanggal_validasi_bank = Column(DateTime)

    # Informasi Pembayaran
    jenis_pembayaran = Column(Integer, default=1)  # 1=Tunai, 2=E-Samsat, etc
    minggu = Column(Integer)

    # Rekening Info
    rekening_asal = Column(String(50))
    rekening_tujuan = Column(String(50))
    kode_kegiatan = Column(String(50))

    # Referensi
    no_ref = Column(String(100))
    no_reg = Column(String(100))

    # Keterangan
    keterangan_umum = Column(Text)
    keterangan_khusus = Column(Text)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    opd = relationship("OPD", back_populates="transaksi")
    rekening = relationship("Rekening", back_populates="transaksi")
    bendahara = relationship("Bendahara", back_populates="transaksi")

    # Indexes
    __table_args__ = (
        Index('idx_transaksi_tanggal', 'tanggal_terima'),
        Index('idx_transaksi_opd_tanggal', 'opd_id', 'tanggal_terima'),
        Index('idx_transaksi_jenis_pembayaran', 'jenis_pembayaran'),
    )

    def __repr__(self):
        return f"<Transaksi(billing='{self.kode_billing}', nominal={self.nominal})>"


class OPDRekening(Base):
    """Tabel relasi antara OPD dan Rekening"""
    __tablename__ = 'opd_rekening'

    id = Column(Integer, primary_key=True, autoincrement=True)
    kode_opd = Column(String(20), ForeignKey('opd.kode_opd'), index=True)
    kode_rekening = Column(String(50), ForeignKey('rekening.kode_rekening'), index=True)
    tahun = Column(Integer)
    keterangan = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index('idx_opd_rekening', 'kode_opd', 'kode_rekening'),
    )


class AuditLog(Base):
    """Tabel Audit Log untuk tracking perubahan"""
    __tablename__ = 'audit_log'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    action = Column(String(50))  # CREATE, UPDATE, DELETE, LOGIN, LOGOUT
    table_name = Column(String(100))
    record_id = Column(Integer)
    old_value = Column(Text)
    new_value = Column(Text)
    ip_address = Column(String(50))
    user_agent = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index('idx_audit_user', 'user_id'),
        Index('idx_audit_action', 'action'),
        Index('idx_audit_created', 'created_at'),
    )


class DashboardConfig(Base):
    """Tabel konfigurasi dashboard"""
    __tablename__ = 'dashboard_config'

    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(100), unique=True, nullable=False)
    value = Column(Text)
    description = Column(Text)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


def create_database(db_url: str = "sqlite:///data/monitoring_sts.db"):
    """Membuat database dan semua tabel"""
    engine = create_engine(db_url, echo=False)
    Base.metadata.create_all(engine)
    return engine


def get_session(engine):
    """Mendapatkan session database"""
    Session = sessionmaker(bind=engine)
    return Session()


if __name__ == "__main__":
    # Test create database
    engine = create_database()
    print("Database schema created successfully!")
    print(f"Tables: {Base.metadata.tables.keys()}")
