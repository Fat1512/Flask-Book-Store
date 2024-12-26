from flask import redirect, url_for
from flask_login import current_user

from app.exception.Unauthorization import Unauthorization
from app.exception.UnauthorizedAccessError import UnauthorizedAccess
from app.model.User import UserRole


def customer_required(f):
    def wrap(*args, **kwargs):
        print("yest1", current_user.is_authenticated)
        if not current_user.is_authenticated:
            return redirect(url_for('account.login_process'))
        if current_user.user_role not in [UserRole.EMPLOYEE_MANAGER, UserRole.EMPLOYEE_MANAGER_WAREHOUSE,
                                          UserRole.EMPLOYEE_SALE, UserRole.ADMIN, UserRole.CUSTOMER]:
            return redirect(url_for('account.login_process'))
        return f(*args, **kwargs)

    wrap.__name__ = f.__name__
    return wrap


def customer_required_api(f):
    def wrap(*args, **kwargs):
        print("yest1", current_user.is_authenticated)
        if not current_user.is_authenticated:
            raise Unauthorization("Login required")
        if current_user.user_role not in [UserRole.EMPLOYEE_MANAGER, UserRole.EMPLOYEE_MANAGER_WAREHOUSE,
                                          UserRole.EMPLOYEE_SALE, UserRole.ADMIN, UserRole.CUSTOMER]:
            raise UnauthorizedAccess(f"Don't have permission to access this resource")
        return f(*args, **kwargs)

    wrap.__name__ = f.__name__
    return wrap


def employee_required(f):
    def wrap(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('account.employee_login'))
        if current_user.user_role not in [UserRole.EMPLOYEE_MANAGER, UserRole.EMPLOYEE_MANAGER_WAREHOUSE,
                                          UserRole.EMPLOYEE_SALE, UserRole.ADMIN]:
            return redirect(url_for('account.employee_login'))
        return f(*args, **kwargs)

    wrap.__name__ = f.__name__
    return wrap


def employee_required_api(f):
    def wrap(*args, **kwargs):
        if not current_user.is_authenticated:
            raise Unauthorization("Login required")
        if current_user.user_role not in [UserRole.EMPLOYEE_MANAGER, UserRole.EMPLOYEE_MANAGER_WAREHOUSE,
                                          UserRole.EMPLOYEE_SALE, UserRole.ADMIN]:
            raise UnauthorizedAccess(f"Don't have permission to access this resource")
        return f(*args, **kwargs)

    wrap.__name__ = f.__name__
    return wrap


def employee_sale_required(f):
    def wrap(*args, **kwargs):
        print("yest1", current_user.is_authenticated)
        if not current_user.is_authenticated:
            return redirect(url_for('account.employee_login'))
        if current_user.user_role not in [UserRole.EMPLOYEE_SALE, UserRole.ADMIN]:
            return redirect(url_for('account.employee_login'))
        return f(*args, **kwargs)

    wrap.__name__ = f.__name__
    return wrap

def employee_sale_required_api(f):
    def wrap(*args, **kwargs):
        print("yest1", current_user.is_authenticated)
        if not current_user.is_authenticated:
            raise Unauthorization("Login required")
        if current_user.user_role not in [UserRole.EMPLOYEE_SALE, UserRole.ADMIN]:
            raise UnauthorizedAccess(f"Don't have permission to access this resource")
        return f(*args, **kwargs)

    wrap.__name__ = f.__name__
    return wrap

def employee_manager_warehouse_required(f):
    def wrap(*args, **kwargs):
        print("yest1", current_user.is_authenticated)
        if not current_user.is_authenticated:
            return redirect(url_for('account.employee_login'))
        if current_user.user_role not in [UserRole.EMPLOYEE_MANAGER_WAREHOUSE, UserRole.ADMIN]:
            return redirect(url_for('account.employee_login'))
        return f(*args, **kwargs)

    wrap.__name__ = f.__name__
    return wrap

def employee_manager_warehouse_required_api(f):
    def wrap(*args, **kwargs):
        print("yest1", current_user.is_authenticated)
        if not current_user.is_authenticated:
            raise Unauthorization("Login required")
        if current_user.user_role not in [UserRole.EMPLOYEE_MANAGER_WAREHOUSE, UserRole.ADMIN]:
            raise UnauthorizedAccess(f"Don't have permission to access this resource")
        return f(*args, **kwargs)

    wrap.__name__ = f.__name__
    return wrap

def employee_manager_required(f):
    def wrap(*args, **kwargs):
        print("yest1", current_user.is_authenticated)
        if not current_user.is_authenticated:
            return redirect(url_for('account.employee_login'))
        if current_user.user_role not in [UserRole.EMPLOYEE_MANAGER, UserRole.ADMIN]:
            return redirect(url_for('account.employee_login'))
        return f(*args, **kwargs)

    wrap.__name__ = f.__name__
    return wrap

def employee_manager_required_api(f):
    def wrap(*args, **kwargs):
        print("yest1", current_user.is_authenticated)
        if not current_user.is_authenticated:
            raise Unauthorization("Login required")
        if current_user.user_role not in [UserRole.EMPLOYEE_MANAGER, UserRole.ADMIN]:
            raise UnauthorizedAccess(f"Don't have permission to access this resource")
        return f(*args, **kwargs)

    wrap.__name__ = f.__name__
    return wrap

