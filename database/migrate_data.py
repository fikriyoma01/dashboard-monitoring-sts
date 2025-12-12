"""
Script untuk migrasi data dari CSV ke Database
"""

import pandas as pd
import os
import sys
from datetime import datetime
from hashlib import sha256

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.schema import (
    Base, User, OPD, Rekening, Bendahara, Transaksi, OPDRekening,
    create_database, DashboardConfig
)
from database.connection import get_db_engine, get_db_session


def hash_password(password: str) -> str:
    """Simple password hashing (use bcrypt in production)"""
    return sha256(password.encode()).hexdigest()


def migrate_users(session):
    """Migrasi default users"""
    print("Migrating users...")

    # Default admin user
    admin = User(
        username='bapendaptip',
        password_hash=hash_password('ptipbapenda2025'),
        nama_lengkap='Admin PTIP BAPENDA',
        email='ptip@bapenda.jatimprov.go.id',
        role='admin',
        is_active=True
    )

    # Check if user exists
    existing = session.query(User).filter_by(username='bapendaptip').first()
    if not existing:
        session.add(admin)
        session.commit()
        print(f"  Created user: {admin.username}")
    else:
        print(f"  User already exists: {existing.username}")


def migrate_opd(session, data_dir: str):
    """Migrasi data OPD dari Excel"""
    print("\nMigrating OPD data...")

    excel_path = os.path.join(data_dir, "TABEL_REFERENSI_KASDASTS.xlsx")
    if not os.path.exists(excel_path):
        print(f"  File not found: {excel_path}")
        return {}

    df = pd.read_excel(excel_path, sheet_name="OPD")
    df.columns = ['KODE_OPD', 'NAMA_OPD', 'TAHUN', 'KODE_QRCODE']
    df['KODE_OPD'] = df['KODE_OPD'].astype(str)

    opd_map = {}
    count = 0

    for _, row in df.iterrows():
        kode = str(row['KODE_OPD']).strip()

        # Check if OPD exists
        existing = session.query(OPD).filter_by(kode_opd=kode).first()
        if existing:
            opd_map[kode] = existing.id
            continue

        opd = OPD(
            kode_opd=kode,
            nama_opd=str(row['NAMA_OPD']) if pd.notna(row['NAMA_OPD']) else 'Tidak Diketahui',
            tahun=int(row['TAHUN']) if pd.notna(row['TAHUN']) else None,
            kode_qrcode=str(row['KODE_QRCODE']) if pd.notna(row['KODE_QRCODE']) else None
        )
        session.add(opd)
        count += 1

        if count % 100 == 0:
            session.flush()

    session.commit()

    # Build mapping
    for opd in session.query(OPD).all():
        opd_map[opd.kode_opd] = opd.id

    print(f"  Migrated {count} OPD records")
    return opd_map


def migrate_rekening(session, data_dir: str):
    """Migrasi data Rekening"""
    print("\nMigrating Rekening data...")

    csv_path = os.path.join(data_dir, "rek_202512100823.csv")
    if not os.path.exists(csv_path):
        print(f"  File not found: {csv_path}")
        return {}

    df = pd.read_csv(csv_path)
    df['KODE'] = df['KODE'].astype(str)

    # Drop duplicates based on KODE, keep first occurrence
    df = df.drop_duplicates(subset=['KODE'], keep='first')

    rek_map = {}
    count = 0
    seen_codes = set()

    for _, row in df.iterrows():
        kode = str(row['KODE']).strip()

        # Skip if already processed
        if kode in seen_codes:
            continue
        seen_codes.add(kode)

        # Check if rekening exists in database
        existing = session.query(Rekening).filter_by(kode_rekening=kode).first()
        if existing:
            rek_map[kode] = existing.id
            continue

        # Determine level based on code length
        level = len(kode) // 2 if len(kode) <= 12 else len(kode) // 3

        rek = Rekening(
            kode_rekening=kode,
            nama_rekening=str(row['NAMA_REK']) if pd.notna(row['NAMA_REK']) else None,
            tahun=int(row['TAHUN']) if pd.notna(row['TAHUN']) else None,
            skt=str(row['SKT']) if pd.notna(row['SKT']) else None,
            prefix=str(row['PREFIX']) if pd.notna(row['PREFIX']) else None,
            level=level
        )
        session.add(rek)
        count += 1

        if count % 500 == 0:
            session.flush()

    session.commit()

    # Build mapping
    for rek in session.query(Rekening).all():
        rek_map[rek.kode_rekening] = rek.id

    print(f"  Migrated {count} Rekening records")
    return rek_map


def migrate_bendahara(session, data_dir: str):
    """Migrasi data Bendahara"""
    print("\nMigrating Bendahara data...")

    csv_path = os.path.join(data_dir, "bpp_202512100822.csv")
    if not os.path.exists(csv_path):
        print(f"  File not found: {csv_path}")
        return {}

    df = pd.read_csv(csv_path)

    bendahara_map = {}
    count = 0

    for _, row in df.iterrows():
        id_sibaku = int(row['IDSIBAKU'])

        # Check if bendahara exists
        existing = session.query(Bendahara).filter_by(id_sibaku=id_sibaku).first()
        if existing:
            bendahara_map[id_sibaku] = existing.id
            continue

        bendahara = Bendahara(
            id_sibaku=id_sibaku,
            nama=str(row['NAMA']) if pd.notna(row['NAMA']) else 'Tidak Diketahui',
            nip=str(row['NIP']) if pd.notna(row['NIP']) else None,
            ip_address=str(row['IP']) if pd.notna(row['IP']) else None
        )
        session.add(bendahara)
        count += 1

        if count % 200 == 0:
            session.flush()

    session.commit()

    # Build mapping
    for b in session.query(Bendahara).all():
        bendahara_map[b.id_sibaku] = b.id

    print(f"  Migrated {count} Bendahara records")
    return bendahara_map


def migrate_transaksi(session, data_dir: str, opd_map: dict, rek_map: dict, bendahara_map: dict):
    """Migrasi data Transaksi STS"""
    print("\nMigrating Transaksi data...")

    csv_path = os.path.join(data_dir, "kasdasts_202512100801.csv")
    if not os.path.exists(csv_path):
        print(f"  File not found: {csv_path}")
        return

    # Read CSV in chunks for memory efficiency
    chunk_size = 5000
    count = 0
    skipped = 0
    seen_billing_codes = set()  # Track already processed billing codes

    for chunk in pd.read_csv(csv_path, chunksize=chunk_size,
                              parse_dates=['TGTERIMA', 'TGSETOR', 'TGVALIDBANK']):

        for _, row in chunk.iterrows():
            kode_billing = str(row['KDBILL'])

            # Skip if already seen in this run
            if kode_billing in seen_billing_codes:
                skipped += 1
                continue
            seen_billing_codes.add(kode_billing)

            # Check if transaction exists in database
            existing = session.query(Transaksi).filter_by(kode_billing=kode_billing).first()
            if existing:
                skipped += 1
                continue

            # Extract OPD and Rekening codes from AYAT
            ayat = str(row['AYAT']) if pd.notna(row['AYAT']) else ''
            kode_opd = ayat[:15] if len(ayat) >= 15 else ayat
            kode_rek = ayat[15:] if len(ayat) > 15 else ''

            # Get foreign key IDs
            opd_id = opd_map.get(kode_opd)
            rek_id = rek_map.get(kode_rek)
            kdkasir = int(row['KDKASIR']) if pd.notna(row['KDKASIR']) else None
            bendahara_id = bendahara_map.get(kdkasir) if kdkasir else None

            transaksi = Transaksi(
                kode_billing=kode_billing,
                opd_id=opd_id,
                rekening_id=rek_id,
                bendahara_id=bendahara_id,
                ayat=ayat,
                nominal=float(row['RPPOKOK']) if pd.notna(row['RPPOKOK']) else 0,
                tanggal_terima=row['TGTERIMA'] if pd.notna(row['TGTERIMA']) else datetime.now(),
                tanggal_setor=row['TGSETOR'] if pd.notna(row['TGSETOR']) else None,
                tanggal_validasi_bank=row['TGVALIDBANK'] if pd.notna(row['TGVALIDBANK']) else None,
                jenis_pembayaran=int(row['KDTUNAI']) if pd.notna(row['KDTUNAI']) else 1,
                minggu=int(row['MINGGU']) if pd.notna(row['MINGGU']) else None,
                rekening_asal=str(row['REKASAL']) if pd.notna(row['REKASAL']) else None,
                rekening_tujuan=str(row['REKTUJUAN']) if pd.notna(row['REKTUJUAN']) else None,
                kode_kegiatan=str(row['KDKEG']) if pd.notna(row['KDKEG']) else None,
                no_ref=str(row['NOREF']) if pd.notna(row['NOREF']) else None,
                no_reg=str(row['NOREG']) if pd.notna(row['NOREG']) else None,
                keterangan_umum=str(row['KETUM']) if pd.notna(row['KETUM']) else None,
                keterangan_khusus=str(row['KETUS']) if pd.notna(row['KETUS']) else None
            )
            session.add(transaksi)
            count += 1

            if count % 1000 == 0:
                session.flush()
                print(f"    Processed {count} transactions...")

        session.commit()

    print(f"  Migrated {count} transactions, skipped {skipped} existing")


def migrate_opd_rekening(session, data_dir: str):
    """Migrasi relasi OPD-Rekening"""
    print("\nMigrating OPD-Rekening relations...")

    csv_path = os.path.join(data_dir, "opdrek_202512100820.csv")
    if not os.path.exists(csv_path):
        print(f"  File not found: {csv_path}")
        return

    # This file is large, read in chunks
    chunk_size = 10000
    count = 0

    # First, clear existing relations
    session.query(OPDRekening).delete()
    session.commit()

    # Get unique combinations only
    seen = set()

    for chunk in pd.read_csv(csv_path, chunksize=chunk_size):
        for _, row in chunk.iterrows():
            kode_opd = str(row['KODE_OPD']).strip() if pd.notna(row['KODE_OPD']) else ''
            kode_rek = str(row['KODE_REK']).strip() if pd.notna(row['KODE_REK']) else ''
            tahun = int(row['TAHUN']) if pd.notna(row['TAHUN']) else None

            # Skip duplicates
            key = (kode_opd, kode_rek, tahun)
            if key in seen:
                continue
            seen.add(key)

            if kode_opd and kode_rek:
                relation = OPDRekening(
                    kode_opd=kode_opd,
                    kode_rekening=kode_rek,
                    tahun=tahun,
                    keterangan=str(row['KET']) if pd.notna(row['KET']) else None
                )
                session.add(relation)
                count += 1

                if count % 5000 == 0:
                    session.flush()
                    print(f"    Processed {count} relations...")

        session.commit()

    print(f"  Migrated {count} unique OPD-Rekening relations")


def create_dashboard_config(session):
    """Create default dashboard configuration"""
    print("\nCreating dashboard config...")

    configs = [
        ('app_name', 'Monitoring STS - BAPENDA Jawa Timur', 'Application name'),
        ('refresh_interval', '30', 'Auto refresh interval in seconds'),
        ('default_period', 'Semua Data', 'Default period filter'),
        ('max_display_rows', '500', 'Maximum rows to display in tables'),
        ('theme_primary', '#00688B', 'Primary theme color'),
        ('theme_secondary', '#00A550', 'Secondary theme color'),
        ('theme_accent', '#00B5EF', 'Accent theme color'),
        ('theme_gold', '#D4AF37', 'Gold accent color'),
    ]

    for key, value, description in configs:
        existing = session.query(DashboardConfig).filter_by(key=key).first()
        if not existing:
            config = DashboardConfig(key=key, value=value, description=description)
            session.add(config)

    session.commit()
    print(f"  Created {len(configs)} config entries")


def run_migration(data_dir: str = "data"):
    """Run full migration"""
    print("=" * 60)
    print("MIGRASI DATA CSV KE DATABASE")
    print("Monitoring STS - BAPENDA Jawa Timur")
    print("=" * 60)

    start_time = datetime.now()

    # Create database and tables
    print("\nCreating database schema...")
    engine = get_db_engine()
    Base.metadata.create_all(engine)
    print("  Schema created successfully")

    # Get session
    session = get_db_session()

    try:
        # Run migrations in order
        migrate_users(session)
        opd_map = migrate_opd(session, data_dir)
        rek_map = migrate_rekening(session, data_dir)
        bendahara_map = migrate_bendahara(session, data_dir)
        migrate_transaksi(session, data_dir, opd_map, rek_map, bendahara_map)
        migrate_opd_rekening(session, data_dir)
        create_dashboard_config(session)

        elapsed = datetime.now() - start_time
        print("\n" + "=" * 60)
        print(f"MIGRATION COMPLETED in {elapsed.total_seconds():.2f} seconds")
        print("=" * 60)

    except Exception as e:
        session.rollback()
        print(f"\nError during migration: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    run_migration()
