"""
Storage service for handling file uploads
"""
import os
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Optional
from PIL import Image
from config.settings import UPLOAD_DIR, ALLOWED_EXTENSIONS, MAX_FILE_SIZE_MB


class StorageService:
    """Handles file storage operations"""
    
    def __init__(self, upload_dir: Path = UPLOAD_DIR):
        """Initialize storage service"""
        self.upload_dir = upload_dir
        self.upload_dir.mkdir(parents=True, exist_ok=True)
    
    def save_image(self, uploaded_file, optimize: bool = True) -> Optional[str]:
        """
        Save uploaded image to disk
        
        Args:
            uploaded_file: Streamlit UploadedFile object
            optimize: Whether to optimize the image
            
        Returns:
            Relative path to saved file or None if failed
        """
        try:
            # Validate file
            if not self._validate_file(uploaded_file):
                return None
            
            # Generate unique filename
            filename = self._generate_filename(uploaded_file.name)
            file_path = self.upload_dir / filename
            
            # Open and process image
            image = Image.open(uploaded_file)
            
            # Optimize if requested
            if optimize:
                image = self._optimize_image(image)
            
            # Save image
            image.save(file_path, quality=85, optimize=True)
            
            # Return relative path
            return f"uploads/{filename}"
            
        except Exception as e:
            print(f"Error saving image: {e}")
            return None
    
    def delete_image(self, relative_path: str) -> bool:
        """Delete image from disk"""
        try:
            file_path = self.upload_dir.parent / relative_path
            if file_path.exists():
                file_path.unlink()
                return True
            return False
        except Exception as e:
            print(f"Error deleting image: {e}")
            return False
    
    def get_image_path(self, relative_path: str) -> Path:
        """Get absolute path for an image"""
        return self.upload_dir.parent / relative_path
    
    def _validate_file(self, uploaded_file) -> bool:
        """Validate uploaded file"""
        # Check extension
        file_ext = Path(uploaded_file.name).suffix.lower()
        if file_ext not in ALLOWED_EXTENSIONS:
            return False
        
        # Check file size
        uploaded_file.seek(0, os.SEEK_END)
        file_size_mb = uploaded_file.tell() / (1024 * 1024)
        uploaded_file.seek(0)
        
        if file_size_mb > MAX_FILE_SIZE_MB:
            return False
        
        return True
    
    def _generate_filename(self, original_name: str) -> str:
        """Generate unique filename"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        hash_obj = hashlib.md5(f"{original_name}{timestamp}".encode())
        hash_str = hash_obj.hexdigest()[:8]
        ext = Path(original_name).suffix.lower()
        return f"pothole_{timestamp}_{hash_str}{ext}"
    
    def _optimize_image(self, image: Image.Image, max_size: tuple = (1920, 1080)) -> Image.Image:
        """Optimize image size and quality"""
        # Convert RGBA to RGB if necessary
        if image.mode == 'RGBA':
            background = Image.new('RGB', image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[3])
            image = background
        
        # Resize if too large
        if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
            image.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        return image
