"""
Authentication utilities
"""

from hashlib import sha256
from datetime import datetime
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import DEFAULT_USERNAME, DEFAULT_PASSWORD


def hash_password(password: str) -> str:
    """
    Hash password using SHA256

    Note: In production, use bcrypt or argon2
    """
    return sha256(password.encode()).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    """
    Verify password against hash
    """
    return hash_password(password) == password_hash


def authenticate_user(username: str, password: str) -> tuple:
    """
    Authenticate user credentials

    Args:
        username: Username to authenticate
        password: Password to verify

    Returns:
        Tuple of (success: bool, user_data: dict or None)
    """
    try:
        from database.connection import get_db_session
        from database.schema import User

        session = get_db_session()

        try:
            user = session.query(User).filter_by(
                username=username,
                is_active=True
            ).first()

            if user and verify_password(password, user.password_hash):
                # Update last login
                user.last_login = datetime.utcnow()
                session.commit()

                return True, {
                    'id': user.id,
                    'username': user.username,
                    'nama_lengkap': user.nama_lengkap,
                    'email': user.email,
                    'role': user.role
                }

        finally:
            session.close()

    except Exception as e:
        print(f"Database auth error: {e}")
        # Fallback to default credentials if database is not available
        pass

    # Fallback authentication (for initial setup or if DB is unavailable)
    if username == DEFAULT_USERNAME and password == DEFAULT_PASSWORD:
        return True, {
            'id': 0,
            'username': username,
            'nama_lengkap': 'Admin PTIP BAPENDA',
            'email': 'ptip@bapenda.jatimprov.go.id',
            'role': 'admin'
        }

    return False, None


def is_authenticated(session_data: dict) -> bool:
    """
    Check if user is authenticated from session data

    Args:
        session_data: Session data dictionary

    Returns:
        True if authenticated, False otherwise
    """
    if not session_data:
        return False
    return session_data.get('authenticated', False)


def get_user_info(session_data: dict) -> dict:
    """
    Get user info from session data

    Args:
        session_data: Session data dictionary

    Returns:
        User info dictionary or empty dict
    """
    if not session_data:
        return {}
    return session_data.get('user', {})


def logout_user(session_data: dict) -> dict:
    """
    Clear session data for logout

    Args:
        session_data: Current session data

    Returns:
        Cleared session data
    """
    return {
        'authenticated': False,
        'user': None,
        'login_time': None,
        'session_id': None
    }


def check_permission(user_data: dict, required_role: str) -> bool:
    """
    Check if user has required role/permission

    Args:
        user_data: User data dictionary
        required_role: Required role name

    Returns:
        True if user has permission, False otherwise
    """
    if not user_data:
        return False

    user_role = user_data.get('role', 'viewer')

    # Role hierarchy: admin > user > viewer
    role_hierarchy = {
        'admin': 3,
        'user': 2,
        'viewer': 1
    }

    user_level = role_hierarchy.get(user_role, 0)
    required_level = role_hierarchy.get(required_role, 0)

    return user_level >= required_level
