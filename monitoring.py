"""Monitoring logic for covenants, reporting deadlines, and renewals."""

from datetime import date, timedelta
from enum import Enum


class CovenantStatus(Enum):
    """Covenant compliance status."""
    OK = "OK"
    AT_RISK = "AT RISK"
    BREACH = "BREACH"
    UNKNOWN = "UNKNOWN"


class ReportingStatus(Enum):
    """Reporting deadline status."""
    OK = "OK"
    UPCOMING = "UPCOMING"
    DUE_SOON = "DUE SOON"
    OVERDUE = "OVERDUE"


class RenewalStatus(Enum):
    """Contract renewal urgency status."""
    OK = "OK"
    WATCH = "WATCH"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"
    EXPIRED = "EXPIRED"


def check_covenant_status(covenant):
    """
    Determine covenant compliance status.
    
    For MINIMUM covenants:
    - BREACH   → current_value < threshold
    - AT RISK  → current_value < threshold * 1.10  (within 10%)
    - OK       → current_value >= threshold * 1.10
    
    For MAXIMUM covenants:
    - BREACH   → current_value > threshold
    - AT RISK  → current_value > threshold * 0.90  (within 10%)
    - OK       → current_value <= threshold * 0.90
    """
    if covenant.current_value is None:
        return CovenantStatus.UNKNOWN
    
    if covenant.type == "minimum":
        if covenant.current_value < covenant.threshold:
            return CovenantStatus.BREACH
        elif covenant.current_value < covenant.threshold * 1.10:
            return CovenantStatus.AT_RISK
        else:
            return CovenantStatus.OK
    
    elif covenant.type == "maximum":
        if covenant.current_value > covenant.threshold:
            return CovenantStatus.BREACH
        elif covenant.current_value > covenant.threshold * 0.90:
            return CovenantStatus.AT_RISK
        else:
            return CovenantStatus.OK
    
    return CovenantStatus.UNKNOWN


def check_reporting_status(reporting_obligation, reference_date=None):
    """
    Determine reporting deadline status.
    
    OVERDUE   → days_left < 0
    DUE SOON  → 0 <= days_left <= 7
    UPCOMING  → 7 < days_left <= 30
    OK        → days_left > 30
    """
    if reference_date is None:
        reference_date = date.today()
    
    days_left = (reporting_obligation.next_due - reference_date).days
    
    if days_left < 0:
        return ReportingStatus.OVERDUE
    elif days_left <= 7:
        return ReportingStatus.DUE_SOON
    elif days_left <= 30:
        return ReportingStatus.UPCOMING
    else:
        return ReportingStatus.OK


def check_renewal_status(agreement, reference_date=None):
    """
    Determine contract renewal urgency.
    
    90 days → WATCH 🟡
    30 days → WARNING 🟠
    7 days  → CRITICAL 🔴
    1 day   → CRITICAL 🔴
    Expired → EXPIRED ⚫
    """
    if reference_date is None:
        reference_date = date.today()
    
    days_left = (agreement.contract_end - reference_date).days
    
    if days_left < 0:
        return RenewalStatus.EXPIRED
    elif days_left <= 7:
        return RenewalStatus.CRITICAL
    elif days_left <= 30:
        return RenewalStatus.WARNING
    elif days_left <= 90:
        return RenewalStatus.WATCH
    else:
        return RenewalStatus.OK


def get_status_emoji(status):
    """Get emoji for status indicator."""
    emoji_map = {
        # Covenant statuses
        CovenantStatus.OK: "🟢",
        CovenantStatus.AT_RISK: "🟡",
        CovenantStatus.BREACH: "🔴",
        CovenantStatus.UNKNOWN: "⚪",
        
        # Reporting statuses
        ReportingStatus.OK: "🟢",
        ReportingStatus.UPCOMING: "🔵",
        ReportingStatus.DUE_SOON: "🟠",
        ReportingStatus.OVERDUE: "🔴",
        
        # Renewal statuses
        RenewalStatus.OK: "🟢",
        RenewalStatus.WATCH: "🟡",
        RenewalStatus.WARNING: "🟠",
        RenewalStatus.CRITICAL: "🔴",
        RenewalStatus.EXPIRED: "⚫"
    }
    return emoji_map.get(status, "⚪")


def get_days_until(target_date, reference_date=None):
    """Calculate days until target date."""
    if reference_date is None:
        reference_date = date.today()
    return (target_date - reference_date).days


def format_currency(amount, currency):
    """Format currency amount for display."""
    if currency == "IDR":
        # Format in billions for IDR
        if amount >= 1_000_000_000:
            return f"IDR {amount / 1_000_000_000:.2f}B"
        elif amount >= 1_000_000:
            return f"IDR {amount / 1_000_000:.2f}M"
        else:
            return f"IDR {amount:,.0f}"
    elif currency == "USD":
        # Format in millions for USD
        if amount >= 1_000_000:
            return f"USD {amount / 1_000_000:.2f}M"
        else:
            return f"USD {amount:,.0f}"
    else:
        return f"{currency} {amount:,.2f}"
