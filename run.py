#!/usr/bin/env python3
"""
Monitoring STS Dashboard - BAPENDA Jawa Timur
Main Entry Point

Usage:
    python run.py              # Run Dash app (default)
    python run.py --migrate    # Run database migration only
    python run.py --streamlit  # Run old Streamlit app
"""

import os
import sys
import argparse


def run_migration():
    """Run database migration"""
    print("=" * 60)
    print("MIGRASI DATA CSV KE DATABASE")
    print("=" * 60)

    from database.migrate_data import run_migration as migrate
    migrate()


def run_dash_app():
    """Run Dash application"""
    from config import DEBUG, HOST, PORT

    # Check if database exists, if not run migration
    db_path = os.path.join('data', 'monitoring_sts.db')
    if not os.path.exists(db_path):
        print("\n[INFO] Database tidak ditemukan. Menjalankan migrasi...")
        run_migration()
        print("\n[INFO] Migrasi selesai. Memulai aplikasi...\n")

    print("=" * 60)
    print("MONITORING STS DASHBOARD")
    print("BAPENDA Jawa Timur")
    print("=" * 60)
    print(f"\nServer berjalan di: http://{HOST}:{PORT}")
    print("Tekan Ctrl+C untuk menghentikan server\n")

    from dash_app import app
    app.run(debug=DEBUG, host=HOST, port=PORT)


def run_streamlit_app():
    """Run old Streamlit application"""
    print("Menjalankan aplikasi Streamlit...")
    os.system("streamlit run app.py")


def main():
    parser = argparse.ArgumentParser(description='Monitoring STS Dashboard')
    parser.add_argument('--migrate', action='store_true', help='Run database migration only')
    parser.add_argument('--streamlit', action='store_true', help='Run old Streamlit app')
    parser.add_argument('--port', type=int, default=8050, help='Port number (default: 8050)')

    args = parser.parse_args()

    if args.migrate:
        run_migration()
    elif args.streamlit:
        run_streamlit_app()
    else:
        if args.port != 8050:
            os.environ['PORT'] = str(args.port)
        run_dash_app()


if __name__ == '__main__':
    main()
