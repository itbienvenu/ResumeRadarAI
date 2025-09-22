import os
import mimetypes

class FileAuth:
    def __init__(self, max_size_mb=3, allowed_types=None):
        """
        max_size_mb: Maximum allowed file size in megabytes
        allowed_types: List of allowed MIME types (e.g., ['text/plain', 'application/pdf'])
        """
        self.max_size = max_size_mb * 1024 * 1024
        if allowed_types is None:
            self.allowed_types = ['text/plain', 'application/pdf']
        else:
            self.allowed_types = allowed_types

    def check_size(self, file_path):
        """Check if file size is within allowed limit"""
        size = os.path.getsize(file_path)
        if size > self.max_size:
            raise ValueError(f"File too large: {size / (1024*1024):.2f} MB (max {self.max_size / (1024*1024)} MB)")
        return True

    def check_type(self, file_path):
        """Check if file MIME type is allowed"""
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type not in self.allowed_types:
            raise ValueError(f"File type '{mime_type}' not allowed")
        return True

    def validate_file(self, file_path):
        """Run all checks"""
        self.check_size(file_path)
        self.check_type(file_path)
        return True
