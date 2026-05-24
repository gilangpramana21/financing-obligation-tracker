"""Email notification system for obligation alerts."""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date, timedelta
from models import get_session, Agreement, ReportingObligation, Covenant
from monitoring import check_reporting_status, check_renewal_status, ReportingStatus, RenewalStatus
import os
from dotenv import load_dotenv

load_dotenv()


class NotificationService:
    """Handle email notifications for obligations."""
    
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.sender_email = os.getenv('SENDER_EMAIL')
        self.sender_password = os.getenv('SENDER_PASSWORD')
        self.recipient_emails = os.getenv('RECIPIENT_EMAILS', '').split(',')
        
        if not self.sender_email or not self.sender_password:
            print("WARNING: Email credentials not configured in .env file")
    
    def send_email(self, subject, body_html):
        """Send email notification."""
        if not self.sender_email or not self.sender_password:
            print(f"\n{'='*60}")
            print("📧 EMAIL DEMO MODE (No credentials configured)")
            print(f"{'='*60}")
            print(f"To: {', '.join(self.recipient_emails)}")
            print(f"Subject: {subject}")
            print(f"\n{body_html[:500]}...")
            print(f"{'='*60}\n")
            return True
        
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.sender_email
            msg['To'] = ', '.join(self.recipient_emails)
            
            html_part = MIMEText(body_html, 'html')
            msg.attach(html_part)
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            print(f"✅ Email sent: {subject}")
            return True
        
        except Exception as e:
            print(f"❌ Failed to send email: {str(e)}")
            return False
    
    def check_and_send_alerts(self):
        """Check all obligations and send alerts if needed."""
        session = get_session()
        alerts = []
        
        # Check renewal alerts
        renewal_alerts = self._check_renewal_alerts(session)
        if renewal_alerts:
            alerts.append(renewal_alerts)
        
        # Check reporting alerts
        reporting_alerts = self._check_reporting_alerts(session)
        if reporting_alerts:
            alerts.append(reporting_alerts)
        
        # Check covenant alerts
        covenant_alerts = self._check_covenant_alerts(session)
        if covenant_alerts:
            alerts.append(covenant_alerts)
        
        # Send combined alert email if there are any alerts
        if alerts:
            subject = f"🔔 Financing Obligation Alerts - {date.today().strftime('%B %d, %Y')}"
            body = self._generate_alert_email(alerts)
            self.send_email(subject, body)
            return True
        else:
            print("✅ No alerts to send today")
            return False
    
    def _check_renewal_alerts(self, session):
        """Check for contract renewals that need alerts."""
        agreements = session.query(Agreement).all()
        alerts = []
        
        for agreement in agreements:
            days_left = (agreement.contract_end - date.today()).days
            status = check_renewal_status(agreement)
            
            # Alert at: 90, 60, 30, 7, 1 days before
            alert_days = [90, 60, 30, 7, 1]
            
            if days_left in alert_days or status in [RenewalStatus.EXPIRED, RenewalStatus.CRITICAL]:
                alerts.append({
                    'type': 'renewal',
                    'financier': agreement.financier,
                    'agreement': agreement.agreement_name,
                    'days_left': days_left,
                    'end_date': agreement.contract_end,
                    'status': status,
                    'urgency': 'critical' if days_left <= 7 else 'warning' if days_left <= 30 else 'info'
                })
        
        return {'category': 'Contract Renewals', 'items': alerts} if alerts else None
    
    def _check_reporting_alerts(self, session):
        """Check for overdue or due soon reports."""
        reports = session.query(ReportingObligation).all()
        alerts = []
        
        for report in reports:
            status = check_reporting_status(report)
            
            if status in [ReportingStatus.OVERDUE, ReportingStatus.DUE_SOON]:
                days_until = (report.next_due - date.today()).days
                alerts.append({
                    'type': 'reporting',
                    'financier': report.agreement.financier,
                    'report_name': report.report_name,
                    'frequency': report.frequency,
                    'next_due': report.next_due,
                    'days_until': days_until,
                    'status': status,
                    'urgency': 'critical' if status == ReportingStatus.OVERDUE else 'warning'
                })
        
        return {'category': 'Reporting Obligations', 'items': alerts} if alerts else None
    
    def _check_covenant_alerts(self, session):
        """Check for covenant breaches or at-risk covenants."""
        covenants = session.query(Covenant).all()
        alerts = []
        
        for covenant in covenants:
            if not covenant.current_value:
                continue
            
            is_breach = False
            is_at_risk = False
            
            if covenant.type == 'minimum':
                if covenant.current_value < covenant.threshold:
                    is_breach = True
                elif covenant.current_value < covenant.threshold * 1.1:  # Within 10% of breach
                    is_at_risk = True
            elif covenant.type == 'maximum':
                if covenant.current_value > covenant.threshold:
                    is_breach = True
                elif covenant.current_value > covenant.threshold * 0.9:  # Within 10% of breach
                    is_at_risk = True
            
            if is_breach or is_at_risk:
                alerts.append({
                    'type': 'covenant',
                    'financier': covenant.agreement.financier,
                    'covenant_name': covenant.name,
                    'threshold': covenant.threshold,
                    'current_value': covenant.current_value,
                    'covenant_type': covenant.type,
                    'unit': covenant.unit,
                    'is_breach': is_breach,
                    'urgency': 'critical' if is_breach else 'warning'
                })
        
        return {'category': 'Financial Covenants', 'items': alerts} if alerts else None
    
    def _generate_alert_email(self, alerts):
        """Generate HTML email body for alerts."""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background: linear-gradient(135deg, #0f2027 0%, #2c5364 100%);
                    color: white;
                    padding: 30px;
                    border-radius: 10px;
                    margin-bottom: 30px;
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 28px;
                }}
                .header p {{
                    margin: 10px 0 0 0;
                    opacity: 0.9;
                }}
                .section {{
                    margin-bottom: 30px;
                    background: #f8f9fa;
                    padding: 20px;
                    border-radius: 10px;
                    border-left: 5px solid #6c757d;
                }}
                .section.critical {{
                    border-left-color: #dc3545;
                    background: #fff5f5;
                }}
                .section.warning {{
                    border-left-color: #ffc107;
                    background: #fffbf0;
                }}
                .section.info {{
                    border-left-color: #0dcaf0;
                    background: #f0f9ff;
                }}
                .section h2 {{
                    margin-top: 0;
                    color: #1a202c;
                    font-size: 20px;
                }}
                .alert-item {{
                    background: white;
                    padding: 15px;
                    margin: 10px 0;
                    border-radius: 8px;
                    border: 1px solid #dee2e6;
                }}
                .alert-item strong {{
                    color: #1a202c;
                }}
                .badge {{
                    display: inline-block;
                    padding: 5px 10px;
                    border-radius: 5px;
                    font-size: 12px;
                    font-weight: bold;
                    margin-left: 10px;
                }}
                .badge.critical {{
                    background: #dc3545;
                    color: white;
                }}
                .badge.warning {{
                    background: #ffc107;
                    color: #000;
                }}
                .badge.info {{
                    background: #0dcaf0;
                    color: #000;
                }}
                .footer {{
                    margin-top: 40px;
                    padding-top: 20px;
                    border-top: 2px solid #dee2e6;
                    text-align: center;
                    color: #6c757d;
                    font-size: 14px;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🔔 Financing Obligation Alerts</h1>
                <p>{date.today().strftime('%A, %B %d, %Y')}</p>
            </div>
        """
        
        for alert_group in alerts:
            category = alert_group['category']
            items = alert_group['items']
            
            # Determine section class based on highest urgency
            urgencies = [item['urgency'] for item in items]
            section_class = 'critical' if 'critical' in urgencies else 'warning' if 'warning' in urgencies else 'info'
            
            html += f"""
            <div class="section {section_class}">
                <h2>{category} ({len(items)} alert{'s' if len(items) > 1 else ''})</h2>
            """
            
            for item in items:
                if item['type'] == 'renewal':
                    html += f"""
                    <div class="alert-item">
                        <strong>{item['financier']}</strong> - {item['agreement']}
                        <span class="badge {item['urgency']}">{item['days_left']} DAYS LEFT</span>
                        <br>
                        <small>Contract ends: {item['end_date'].strftime('%B %d, %Y')}</small>
                    </div>
                    """
                
                elif item['type'] == 'reporting':
                    html += f"""
                    <div class="alert-item">
                        <strong>{item['financier']}</strong> - {item['report_name']}
                        <span class="badge {item['urgency']}">{'OVERDUE' if item['days_until'] < 0 else 'DUE SOON'}</span>
                        <br>
                        <small>Due: {item['next_due'].strftime('%B %d, %Y')} ({item['frequency']})</small>
                    </div>
                    """
                
                elif item['type'] == 'covenant':
                    status_text = 'BREACH' if item['is_breach'] else 'AT RISK'
                    html += f"""
                    <div class="alert-item">
                        <strong>{item['financier']}</strong> - {item['covenant_name']}
                        <span class="badge {item['urgency']}">{status_text}</span>
                        <br>
                        <small>
                            Current: {item['current_value']:,.2f} {item['unit']} | 
                            Threshold ({item['covenant_type']}): {item['threshold']:,.2f} {item['unit']}
                        </small>
                    </div>
                    """
            
            html += "</div>"
        
        html += """
            <div class="footer">
                <p>This is an automated alert from your Financing Obligation Tracker.</p>
                <p>Please review the dashboard for full details and take necessary actions.</p>
            </div>
        </body>
        </html>
        """
        
        return html


def run_daily_check():
    """Run daily obligation check and send alerts."""
    print(f"\n{'='*60}")
    print(f"Running Daily Obligation Check - {date.today().strftime('%B %d, %Y')}")
    print(f"{'='*60}\n")
    
    notifier = NotificationService()
    notifier.check_and_send_alerts()
    
    print(f"\n{'='*60}")
    print("Daily check completed")
    print(f"{'='*60}\n")


if __name__ == '__main__':
    # Test the notification system
    run_daily_check()
