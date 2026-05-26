"""Google Drive integration for automatic PDF processing."""

import os
import io
import base64
from typing import Optional, Dict, Any
from datetime import datetime

try:
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaIoBaseDownload
    from google.oauth2 import service_account
    GOOGLE_DRIVE_AVAILABLE = True
except ImportError:
    GOOGLE_DRIVE_AVAILABLE = False


class GoogleDriveSync:
    """Sync PDFs from Google Drive folder."""
    
    def __init__(self):
        """Initialize Google Drive API client."""
        if not GOOGLE_DRIVE_AVAILABLE:
            raise ImportError("Google Drive libraries not installed. Run: pip install google-api-python-client google-auth")
        
        # Load credentials from environment variable (JSON string)
        credentials_json = os.getenv('GOOGLE_DRIVE_CREDENTIALS')
        if not credentials_json:
            raise ValueError("GOOGLE_DRIVE_CREDENTIALS environment variable not set")
        
        # Parse credentials
        import json
        credentials_dict = json.loads(credentials_json)
        
        # Create credentials object
        credentials = service_account.Credentials.from_service_account_info(
            credentials_dict,
            scopes=['https://www.googleapis.com/auth/drive.readonly']
        )
        
        # Build Drive API client
        self.service = build('drive', 'v3', credentials=credentials)
        
        # Get folder ID from environment
        self.folder_id = os.getenv('GOOGLE_DRIVE_FOLDER_ID')
        if not self.folder_id:
            raise ValueError("GOOGLE_DRIVE_FOLDER_ID environment variable not set")
    
    def list_new_pdfs(self, last_check_time: Optional[datetime] = None) -> list:
        """
        List new PDF files in the monitored folder.
        
        Args:
            last_check_time: Only return files modified after this time
            
        Returns:
            List of file metadata dicts
        """
        try:
            # Build query
            query = f"'{self.folder_id}' in parents and mimeType='application/pdf' and trashed=false"
            
            if last_check_time:
                # Format time for Drive API
                time_str = last_check_time.strftime('%Y-%m-%dT%H:%M:%S')
                query += f" and modifiedTime > '{time_str}'"
            
            # List files
            results = self.service.files().list(
                q=query,
                fields='files(id, name, createdTime, modifiedTime, size)',
                orderBy='createdTime desc'
            ).execute()
            
            files = results.get('files', [])
            return files
        
        except Exception as e:
            print(f"Error listing files: {e}")
            return []
    
    def download_pdf(self, file_id: str, output_path: str) -> bool:
        """
        Download PDF file from Google Drive.
        
        Args:
            file_id: Google Drive file ID
            output_path: Local path to save file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Get file
            request = self.service.files().get_media(fileId=file_id)
            
            # Download to file
            with io.FileIO(output_path, 'wb') as fh:
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while not done:
                    status, done = downloader.next_chunk()
            
            return True
        
        except Exception as e:
            print(f"Error downloading file: {e}")
            return False
    
    def get_pdf_as_base64(self, file_id: str) -> Optional[str]:
        """
        Get PDF file content as base64 string.
        
        Args:
            file_id: Google Drive file ID
            
        Returns:
            Base64 encoded PDF content, or None if error
        """
        try:
            # Get file
            request = self.service.files().get_media(fileId=file_id)
            
            # Download to memory
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
            
            # Encode to base64
            fh.seek(0)
            pdf_bytes = fh.read()
            pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')
            
            return pdf_base64
        
        except Exception as e:
            print(f"Error getting file content: {e}")
            return None


def process_new_pdfs_from_drive():
    """
    Check Google Drive for new PDFs and process them.
    This function is called by cron job or webhook.
    """
    from extractor import DocumentExtractor
    from models import get_session, Agreement
    from notifications import NotificationService
    
    try:
        # Initialize Drive sync
        drive_sync = GoogleDriveSync()
        
        # Get last check time from database or file
        # For now, check all files (can be optimized later)
        new_files = drive_sync.list_new_pdfs()
        
        if not new_files:
            print("No new PDFs found in Google Drive")
            return
        
        print(f"Found {len(new_files)} new PDF(s) in Google Drive")
        
        # Initialize extractor
        extractor = DocumentExtractor(llm_provider="gemini")
        
        # Initialize database session
        session = get_session()
        
        # Initialize notification service
        notifier = NotificationService()
        
        # Process each file
        processed_count = 0
        error_count = 0
        
        for file_info in new_files:
            file_id = file_info['id']
            filename = file_info['name']
            
            print(f"Processing: {filename}")
            
            try:
                # Download PDF to temp location
                temp_path = f"/tmp/{filename}"
                success = drive_sync.download_pdf(file_id, temp_path)
                
                if not success:
                    print(f"Failed to download: {filename}")
                    error_count += 1
                    continue
                
                # Extract text
                document_text = extractor.extract_text(temp_path)
                
                # Extract data
                agreement_data = extractor.extract_obligations_from_text(document_text)
                
                if not agreement_data:
                    print(f"Failed to extract data from: {filename}")
                    error_count += 1
                    continue
                
                # Validate data
                extractor.validate_extracted_data(agreement_data)
                
                # Check if already exists
                existing = session.query(Agreement).filter(
                    Agreement.financier == agreement_data['financier'],
                    Agreement.agreement_name == agreement_data['agreement_name']
                ).first()
                
                if existing:
                    print(f"Agreement already exists: {filename}")
                    continue
                
                # Save to database (same logic as upload route)
                from datetime import datetime as dt
                from models import ReportingObligation, Covenant, OtherObligation
                
                agreement = Agreement(
                    financier=agreement_data['financier'],
                    agreement_name=agreement_data['agreement_name'],
                    contract_start=dt.strptime(agreement_data['contract_start'], '%Y-%m-%d').date(),
                    contract_end=dt.strptime(agreement_data['contract_end'], '%Y-%m-%d').date(),
                    facility_amount=float(agreement_data['facility_amount']),
                    currency=agreement_data['currency']
                )
                session.add(agreement)
                session.flush()
                
                # Add obligations
                for report in agreement_data.get('reporting_obligations', []):
                    reporting = ReportingObligation(
                        agreement_id=agreement.id,
                        report_name=report['report_name'],
                        frequency=report['frequency'],
                        due_day=report['due_day'],
                        description=report.get('description', ''),
                        next_due=dt.strptime(report['next_due'], '%Y-%m-%d').date()
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
                
                print(f"✅ Successfully processed: {filename}")
                processed_count += 1
                
                # Send email notification
                try:
                    notifier.send_new_agreement_notification(agreement_data)
                except Exception as e:
                    print(f"Failed to send notification: {e}")
                
                # Clean up temp file
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
            
            except Exception as e:
                print(f"Error processing {filename}: {e}")
                error_count += 1
                session.rollback()
        
        session.close()
        
        print(f"\n=== Summary ===")
        print(f"Processed: {processed_count}")
        print(f"Errors: {error_count}")
        print(f"Total: {len(new_files)}")
        
        return {
            'processed': processed_count,
            'errors': error_count,
            'total': len(new_files)
        }
    
    except Exception as e:
        print(f"Fatal error in process_new_pdfs_from_drive: {e}")
        return {
            'processed': 0,
            'errors': 1,
            'total': 0,
            'error': str(e)
        }
