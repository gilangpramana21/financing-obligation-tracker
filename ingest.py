"""Load financing agreement data into the database."""

from datetime import datetime
from models import init_db, get_session, Agreement, ReportingObligation, Covenant, OtherObligation
from dummy_data import DUMMY_AGREEMENTS


def load_dummy_data(db_path='obligation_tracker.db'):
    """Load dummy financing agreements into database."""
    # Initialize database
    engine = init_db(db_path)
    session = get_session(engine)
    
    try:
        # Clear existing data
        session.query(OtherObligation).delete()
        session.query(Covenant).delete()
        session.query(ReportingObligation).delete()
        session.query(Agreement).delete()
        session.commit()
        
        # Load dummy agreements
        for agreement_data in DUMMY_AGREEMENTS:
            # Create agreement
            agreement = Agreement(
                financier=agreement_data['financier'],
                agreement_name=agreement_data['agreement_name'],
                contract_start=agreement_data['contract_start'],
                contract_end=agreement_data['contract_end'],
                facility_amount=agreement_data['facility_amount'],
                currency=agreement_data['currency']
            )
            session.add(agreement)
            session.flush()  # Get agreement.id
            
            # Add reporting obligations
            for report in agreement_data['reporting_obligations']:
                reporting = ReportingObligation(
                    agreement_id=agreement.id,
                    report_name=report['report_name'],
                    frequency=report['frequency'],
                    due_day=report['due_day'],
                    description=report['description'],
                    next_due=report['next_due']
                )
                session.add(reporting)
            
            # Add covenants
            for covenant in agreement_data['covenants']:
                cov = Covenant(
                    agreement_id=agreement.id,
                    name=covenant['name'],
                    type=covenant['type'],
                    metric=covenant['metric'],
                    threshold=covenant['threshold'],
                    unit=covenant['unit'],
                    description=covenant['description'],
                    current_value=covenant.get('current_value'),
                    last_updated=datetime.now().date()
                )
                session.add(cov)
            
            # Add other obligations
            for obligation in agreement_data['other_obligations']:
                other = OtherObligation(
                    agreement_id=agreement.id,
                    category=obligation['category'],
                    description=obligation['description'],
                    is_ongoing=obligation['is_ongoing']
                )
                session.add(other)
        
        session.commit()
        print(f"✅ Successfully loaded {len(DUMMY_AGREEMENTS)} agreements into database")
        
        # Print summary
        total_reports = session.query(ReportingObligation).count()
        total_covenants = session.query(Covenant).count()
        total_other = session.query(OtherObligation).count()
        
        print(f"   📊 {total_reports} reporting obligations")
        print(f"   📈 {total_covenants} covenants")
        print(f"   📋 {total_other} other obligations")
        
    except Exception as e:
        session.rollback()
        print(f"❌ Error loading data: {e}")
        raise
    finally:
        session.close()


if __name__ == '__main__':
    load_dummy_data()
