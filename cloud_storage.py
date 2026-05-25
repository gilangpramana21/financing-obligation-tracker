"""Cloud storage handler for PDF uploads using Cloudinary."""

import os
import cloudinary
import cloudinary.uploader
from typing import Optional

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)


def upload_pdf(file_path: str, filename: str) -> Optional[str]:
    """
    Upload PDF to Cloudinary.
    
    Args:
        file_path: Local path to PDF file
        filename: Original filename
        
    Returns:
        Cloudinary URL of uploaded file, or None if upload fails
    """
    try:
        # Upload to Cloudinary
        result = cloudinary.uploader.upload(
            file_path,
            resource_type="raw",  # For non-image files
            folder="financing-agreements",
            public_id=filename.replace('.pdf', ''),
            overwrite=True
        )
        
        return result.get('secure_url')
    
    except Exception as e:
        print(f"Error uploading to Cloudinary: {e}")
        return None


def download_pdf(url: str, local_path: str) -> bool:
    """
    Download PDF from Cloudinary to local path.
    
    Args:
        url: Cloudinary URL
        local_path: Local path to save file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        import requests
        
        response = requests.get(url)
        response.raise_for_status()
        
        with open(local_path, 'wb') as f:
            f.write(response.content)
        
        return True
    
    except Exception as e:
        print(f"Error downloading from Cloudinary: {e}")
        return False


def delete_pdf(url: str) -> bool:
    """
    Delete PDF from Cloudinary.
    
    Args:
        url: Cloudinary URL
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Extract public_id from URL
        public_id = url.split('/')[-1].replace('.pdf', '')
        
        result = cloudinary.uploader.destroy(
            f"financing-agreements/{public_id}",
            resource_type="raw"
        )
        
        return result.get('result') == 'ok'
    
    except Exception as e:
        print(f"Error deleting from Cloudinary: {e}")
        return False


def is_cloudinary_configured() -> bool:
    """Check if Cloudinary is properly configured."""
    return all([
        os.getenv('CLOUDINARY_CLOUD_NAME'),
        os.getenv('CLOUDINARY_API_KEY'),
        os.getenv('CLOUDINARY_API_SECRET')
    ])
