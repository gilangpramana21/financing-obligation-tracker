"""SQLAlchemy ORM models for financing obligation tracker."""

from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, Boolean, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


class Agreement(Base):
    """Financing agreement master record."""
    __tablename__ = 'agreements'
    
    id = Column(Integer, primary_key=True)
    financier = Column(String(200), nullable=False)
    agreement_name = Column(String(300), nullable=False)
    contract_start = Column(Date, nullable=False)
    contract_end = Column(Date, nullable=False)
    facility_amount = Column(Float, nullable=False)
    currency = Column(String(10), nullable=False)
    created_at = Column(Date, default=datetime.now)
    
    # Relationships
    reporting_obligations = relationship("ReportingObligation", back_populates="agreement", cascade="all, delete-orphan")
    covenants = relationship("Covenant", back_populates="agreement", cascade="all, delete-orphan")
    other_obligations = relationship("OtherObligation", back_populates="agreement", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Agreement(financier='{self.financier}', name='{self.agreement_name}')>"


class ReportingObligation(Base):
    """Reporting requirements from financing agreements."""
    __tablename__ = 'reporting_obligations'
    
    id = Column(Integer, primary_key=True)
    agreement_id = Column(Integer, ForeignKey('agreements.id'), nullable=False)
    report_name = Column(String(300), nullable=False)
    frequency = Column(String(50), nullable=False)  # monthly, quarterly, semi-annual, annual
    due_day = Column(Integer, nullable=False)  # day of month/quarter/year
    description = Column(Text)
    next_due = Column(Date, nullable=False)
    
    agreement = relationship("Agreement", back_populates="reporting_obligations")
    
    def __repr__(self):
        return f"<ReportingObligation(report='{self.report_name}', next_due='{self.next_due}')>"


class Covenant(Base):
    """Financial covenants to be monitored."""
    __tablename__ = 'covenants'
    
    id = Column(Integer, primary_key=True)
    agreement_id = Column(Integer, ForeignKey('agreements.id'), nullable=False)
    name = Column(String(300), nullable=False)
    type = Column(String(20), nullable=False)  # minimum or maximum
    metric = Column(String(200), nullable=False)
    threshold = Column(Float, nullable=False)
    unit = Column(String(50), nullable=False)  # IDR, USD, ratio, percent
    description = Column(Text)
    current_value = Column(Float)  # Actual current value (updated separately)
    last_updated = Column(Date)
    
    agreement = relationship("Agreement", back_populates="covenants")
    
    def __repr__(self):
        return f"<Covenant(name='{self.name}', type='{self.type}', threshold={self.threshold})>"


class OtherObligation(Base):
    """Other obligations (notifications, approvals, restrictions, actions)."""
    __tablename__ = 'other_obligations'
    
    id = Column(Integer, primary_key=True)
    agreement_id = Column(Integer, ForeignKey('agreements.id'), nullable=False)
    category = Column(String(100), nullable=False)  # Notification, Approval Required, Restriction, Action Required
    description = Column(Text, nullable=False)
    is_ongoing = Column(Boolean, default=True)
    
    agreement = relationship("Agreement", back_populates="other_obligations")
    
    def __repr__(self):
        return f"<OtherObligation(category='{self.category}')>"


# Database setup
def get_engine(db_path='obligation_tracker.db'):
    """Create and return database engine."""
    import os
    
    # Use PostgreSQL on Vercel, SQLite locally
    if os.getenv('VERCEL') or os.getenv('POSTGRES_URL'):
        database_url = os.getenv('POSTGRES_URL') or os.getenv('DATABASE_URL')
        if database_url:
            # Vercel Postgres uses 'postgres://' but SQLAlchemy needs 'postgresql://'
            if database_url.startswith('postgres://'):
                database_url = database_url.replace('postgres://', 'postgresql://', 1)
            return create_engine(database_url, echo=False)
    
    # Fallback to SQLite for local development
    return create_engine(f'sqlite:///{db_path}', echo=False)


def init_db(db_path='obligation_tracker.db'):
    """Initialize database with all tables."""
    engine = get_engine(db_path)
    Base.metadata.create_all(engine)
    return engine


def get_session(engine=None):
    """Get database session."""
    if engine is None:
        engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()
