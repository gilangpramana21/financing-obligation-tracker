"""Flask Application for Financing Obligation Tracker."""

from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import date, timedelta
from sqlalchemy import func
import os
from werkzeug.utils import secure_filename

# Scheduler only works in non-serverless environments
# For Vercel deployment, use Vercel Cron Jobs instead
ENABLE_SCHEDULER = os.getenv('ENABLE_SCHEDULER', 'false').lower() == 'true'

if ENABLE_SCHEDULER:
    from apscheduler.schedulers.background import BackgroundScheduler
    from apscheduler.triggers.cron import CronTrigger

from models import get_session, Agreement, ReportingObligation, Covenant, OtherObligation
from monitoring import (
    check_covenant_status, check_reporting_status, check_renewal_status,
    get_days_until, format_currency, CovenantStatus, ReportingStatus, RenewalStatus
)
from notifications import NotificationService, run_daily_check

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['UPLOAD_FOLDER'] = '/tmp/documents' if os.getenv('VERCEL') else 'documents'
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024  # 200MB max file size

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

session = get_session()

# Initialize notification service
notifier = NotificationService()

# Setup scheduler for daily alerts (only in non-serverless environments)
if ENABLE_SCHEDULER:
    scheduler = BackgroundScheduler()
    # Run daily at 9:00 AM
    scheduler.add_job(
        func=run_daily_check,
        trigger=CronTrigger(hour=9, minute=0),
        id='daily_obligation_check',
        name='Daily Obligation Check',
        replace_existing=True
    )
    scheduler.start()


@app.route('/')
def index():
    """Dashboard overview page."""
    # Get all agreements
    agreements = session.query(Agreement).all()
    
    # Calculate metrics
    total_agreements = len(agreements)
    total_facility = sum(a.facility_amount for a in agreements)
    currency = agreements[0].currency if agreements else 'USD'
    
    # Get reporting obligations
    reporting_obligations = session.query(ReportingObligation).all()
    overdue_reports = sum(1 for r in reporting_obligations 
                         if check_reporting_status(r) == ReportingStatus.OVERDUE)
    
    # Get covenants
    covenants = session.query(Covenant).all()
    breached_covenants = sum(1 for c in covenants 
                            if c.current_value and 
                            ((c.type == 'minimum' and c.current_value < c.threshold) or
                             (c.type == 'maximum' and c.current_value > c.threshold)))
    
    return render_template('index.html',
                         total_agreements=total_agreements,
                         total_facility=format_currency(total_facility, currency),
                         overdue_reports=overdue_reports,
                         breached_covenants=breached_covenants,
                         agreements=agreements,
                         today=date.today())


@app.route('/obligations')
def obligations():
    """Detailed obligations page."""
    # Get filter from query params
    selected_financier = request.args.get('financier', 'All')
    
    # Get all agreements for filter
    agreements = session.query(Agreement).all()
    financiers = ['All'] + sorted(list(set(a.financier for a in agreements)))
    
    # Get reporting obligations
    query = session.query(ReportingObligation).join(Agreement)
    if selected_financier != 'All':
        query = query.filter(Agreement.financier == selected_financier)
    reporting_obligations = query.all()
    
    # Get covenants
    query = session.query(Covenant).join(Agreement)
    if selected_financier != 'All':
        query = query.filter(Agreement.financier == selected_financier)
    covenants = query.all()
    
    # Get other obligations
    query = session.query(OtherObligation).join(Agreement)
    if selected_financier != 'All':
        query = query.filter(Agreement.financier == selected_financier)
    other_obligations = query.all()
    
    return render_template('obligations.html',
                         financiers=financiers,
                         selected_financier=selected_financier,
                         reporting_obligations=reporting_obligations,
                         covenants=covenants,
                         other_obligations=other_obligations,
                         check_reporting_status=check_reporting_status,
                         check_covenant_status=check_covenant_status,
                         get_days_until=get_days_until,
                         format_currency=format_currency,
                         ReportingStatus=ReportingStatus,
                         CovenantStatus=CovenantStatus)


@app.route('/renewals')
def renewals():
    """Contract renewals page."""
    agreements = session.query(Agreement).all()
    
    renewals = []
    for agreement in agreements:
        days_left = (agreement.contract_end - date.today()).days
        status = check_renewal_status(agreement)
        
        renewals.append({
            'financier': agreement.financier,
            'agreement': agreement.agreement_name,
            'start_date': agreement.contract_start,
            'end_date': agreement.contract_end,
            'amount': format_currency(agreement.facility_amount, agreement.currency),
            'days_left': days_left,
            'status': status
        })
    
    # Sort by days left
    renewals.sort(key=lambda x: x['days_left'])
    
    return render_template('renewals.html',
                         renewals=renewals,
                         RenewalStatus=RenewalStatus)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """Upload PDF page."""
    if request.method == 'POST':
        if 'files[]' not in request.files:
            return jsonify({'error': 'No files uploaded'}), 400
        
        files = request.files.getlist('files[]')
        
        # For now, only process first file and show preview
        if len(files) > 0:
            file = files[0]
            if file and file.filename.endswith('.pdf'):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                try:
                    # Process PDF
                    from extractor import DocumentExtractor
                    extractor = DocumentExtractor(llm_provider="gemini")
                    
                    # Extract text
                    document_text = extractor.extract_text(filepath)
                    
                    # Extract data
                    agreement_data = extractor.extract_obligations_from_text(document_text)
                    
                    if agreement_data:
                        # Validate data
                        extractor.validate_extracted_data(agreement_data)
                        
                        # Check if exists
                        existing = session.query(Agreement).filter(
                            Agreement.financier == agreement_data['financier'],
                            Agreement.agreement_name == agreement_data['agreement_name']
                        ).first()
                        
                        if existing:
                            # Clean up file
                            if os.path.exists(filepath):
                                os.unlink(filepath)
                            return jsonify({'error': 'Agreement already exists in database'}), 400
                        
                        # Upload to Cloudinary if configured
                        pdf_url = None
                        if os.getenv('VERCEL'):
                            from cloud_storage import upload_pdf, is_cloudinary_configured
                            if is_cloudinary_configured():
                                pdf_url = upload_pdf(filepath, filename)
                                if pdf_url:
                                    agreement_data['pdf_url'] = pdf_url
                        
                        # Store data in session for preview
                        from flask import session as flask_session
                        flask_session['preview_data'] = agreement_data
                        flask_session['preview_filename'] = filename
                        
                        # Clean up local file
                        if os.path.exists(filepath):
                            os.unlink(filepath)
                        
                        return jsonify({'success': True, 'redirect': '/upload/preview'})
                    else:
                        # Clean up file
                        if os.path.exists(filepath):
                            os.unlink(filepath)
                        return jsonify({'error': 'Failed to extract data from PDF'}), 400
                
                except Exception as e:
                    # Clean up file
                    if os.path.exists(filepath):
                        os.unlink(filepath)
                    return jsonify({'error': str(e)}), 500
            else:
                return jsonify({'error': 'Only PDF files are supported'}), 400
        else:
            return jsonify({'error': 'No files uploaded'}), 400
    
    return render_template('upload.html')


@app.route('/upload/preview')
def upload_preview():
    """Show preview of extracted data before saving."""
    from flask import session as flask_session
    
    if 'preview_data' not in flask_session:
        return redirect(url_for('upload'))
    
    data = flask_session['preview_data']
    filename = flask_session.get('preview_filename', 'document.pdf')
    
    return render_template('upload_preview.html', data=data, filename=filename)


@app.route('/upload/confirm', methods=['POST'])
def upload_confirm():
    """Save confirmed data to database."""
    from flask import session as flask_session
    from datetime import datetime
    
    if 'preview_data' not in flask_session:
        return jsonify({'error': 'No preview data found'}), 400
    
    agreement_data = flask_session['preview_data']
    
    try:
        # Create Agreement
        agreement = Agreement(
            financier=agreement_data['financier'],
            agreement_name=agreement_data['agreement_name'],
            contract_start=datetime.strptime(agreement_data['contract_start'], '%Y-%m-%d').date(),
            contract_end=datetime.strptime(agreement_data['contract_end'], '%Y-%m-%d').date(),
            facility_amount=float(agreement_data['facility_amount']),
            currency=agreement_data['currency']
        )
        session.add(agreement)
        session.flush()
        
        # Add obligations, covenants, etc.
        for report in agreement_data.get('reporting_obligations', []):
            reporting = ReportingObligation(
                agreement_id=agreement.id,
                report_name=report['report_name'],
                frequency=report['frequency'],
                due_day=report['due_day'],
                description=report.get('description', ''),
                next_due=datetime.strptime(report['next_due'], '%Y-%m-%d').date()
            )
            session.add(reporting)
        
        for cov in agreement_data.get('covenants', []):
            covenant = Covenant(
                agreement_id=agreement.id,
                name=cov['name'],
                type=cov['type'],
                metric=cov['metric'],
                threshold=float(cov['threshold']),
                unit=cov['unit'],
                description=cov.get('description', ''),
                current_value=None,
                last_updated=None
            )
            session.add(covenant)
        
        for other in agreement_data.get('other_obligations', []):
            obligation = OtherObligation(
                agreement_id=agreement.id,
                category=other['category'],
                description=other['description'],
                is_ongoing=other.get('is_ongoing', True)
            )
            session.add(obligation)
        
        session.commit()
        
        # Clear session data
        flask_session.pop('preview_data', None)
        flask_session.pop('preview_filename', None)
        
        return jsonify({'success': True, 'message': 'Agreement saved successfully', 'redirect': '/'})
    
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/update_covenant/<int:covenant_id>', methods=['POST'])
def update_covenant(covenant_id):
    """API endpoint to update covenant value."""
    data = request.get_json()
    new_value = data.get('value')
    
    if new_value is None:
        return jsonify({'error': 'No value provided'}), 400
    
    covenant = session.query(Covenant).get(covenant_id)
    if not covenant:
        return jsonify({'error': 'Covenant not found'}), 404
    
    covenant.current_value = float(new_value)
    covenant.last_updated = date.today()
    session.commit()
    
    return jsonify({'success': True, 'message': 'Covenant updated'})


@app.route('/api/mark_submitted/<int:report_id>', methods=['POST'])
def mark_submitted(report_id):
    """API endpoint to mark report as submitted."""
    report = session.query(ReportingObligation).get(report_id)
    if not report:
        return jsonify({'error': 'Report not found'}), 404
    
    # Calculate next due date based on frequency
    from dateutil.relativedelta import relativedelta
    
    current_due = report.next_due
    if report.frequency.lower() == 'monthly':
        report.next_due = current_due + relativedelta(months=1)
    elif report.frequency.lower() == 'quarterly':
        report.next_due = current_due + relativedelta(months=3)
    elif report.frequency.lower() == 'semi-annual':
        report.next_due = current_due + relativedelta(months=6)
    elif report.frequency.lower() == 'annual':
        report.next_due = current_due + relativedelta(years=1)
    else:
        # Default to monthly if unknown
        report.next_due = current_due + relativedelta(months=1)
    
    session.commit()
    
    return jsonify({
        'success': True, 
        'message': 'Report marked as submitted',
        'next_due': report.next_due.strftime('%Y-%m-%d')
    })


@app.route('/api/send_test_alert', methods=['POST'])
def send_test_alert():
    """API endpoint to send test alert email."""
    try:
        notifier.check_and_send_alerts()
        
        # Also save HTML preview
        session_db = get_session()
        alerts = []
        
        renewal_alerts = notifier._check_renewal_alerts(session_db)
        if renewal_alerts:
            alerts.append(renewal_alerts)
        
        reporting_alerts = notifier._check_reporting_alerts(session_db)
        if reporting_alerts:
            alerts.append(reporting_alerts)
        
        covenant_alerts = notifier._check_covenant_alerts(session_db)
        if covenant_alerts:
            alerts.append(covenant_alerts)
        
        if alerts:
            html_content = notifier._generate_alert_email(alerts)
            
            # Save to file
            with open('email_preview.html', 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            return jsonify({
                'success': True, 
                'message': 'Alert check completed. Email preview saved to email_preview.html. Open it in browser to see how email looks.',
                'preview_file': 'email_preview.html'
            })
        else:
            return jsonify({
                'success': True,
                'message': 'No alerts to send today. All obligations are up to date!'
            })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/settings')
def settings():
    """Settings page for email configuration."""
    return render_template('settings.html',
                         smtp_server=os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
                         smtp_port=os.getenv('SMTP_PORT', '587'),
                         sender_email=os.getenv('SENDER_EMAIL', ''),
                         recipient_emails=os.getenv('RECIPIENT_EMAILS', ''))


@app.route('/api/cron/daily-check')
def cron_daily_check():
    """Cron endpoint for daily obligation check (called by Vercel Cron)."""
    # Verify request is from Vercel Cron
    auth_header = request.headers.get('Authorization', '')
    cron_secret = os.getenv('CRON_SECRET', 'default-secret')
    
    if not auth_header.startswith('Bearer ') or auth_header[7:] != cron_secret:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        run_daily_check()
        return jsonify({'success': True, 'message': 'Daily check completed'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    try:
        app.run(debug=True, host='0.0.0.0', port=8080)
    finally:
        # Shutdown scheduler when app closes (only if enabled)
        if ENABLE_SCHEDULER and 'scheduler' in globals():
            scheduler.shutdown()
