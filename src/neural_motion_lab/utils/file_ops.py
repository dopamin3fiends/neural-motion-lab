"""
File operation utilities.
"""

import os
import urllib.request
from pathlib import Path
from typing import Optional
from tqdm import tqdm


def ensure_dir(path: str) -> Path:
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        path: Directory path
        
    Returns:
        Path object
    """
    dir_path = Path(path)
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def download_file(
    url: str,
    destination: str,
    show_progress: bool = True
) -> str:
    """
    Download a file from URL with optional progress bar.
    
    Args:
        url: URL to download from
        destination: Destination file path
        show_progress: Whether to show download progress
        
    Returns:
        Path to downloaded file
    """
    dest_path = Path(destination)
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    
    if show_progress:
        class DownloadProgressBar(tqdm):
            def update_to(self, b=1, bsize=1, tsize=None):
                if tsize is not None:
                    self.total = tsize
                self.update(b * bsize - self.n)
        
        with DownloadProgressBar(unit='B', unit_scale=True, miniters=1) as t:
            urllib.request.urlretrieve(url, destination, reporthook=t.update_to)
    else:
        urllib.request.urlretrieve(url, destination)
    
    return str(dest_path)


def get_file_size(path: str) -> int:
    """
    Get file size in bytes.
    
    Args:
        path: File path
        
    Returns:
        File size in bytes
    """
    return os.path.getsize(path)


def list_files(directory: str, pattern: str = "*") -> list:
    """
    List files in directory matching pattern.
    
    Args:
        directory: Directory path
        pattern: Glob pattern (default: all files)
        
    Returns:
        List of file paths
    """
    dir_path = Path(directory)
    return [str(p) for p in dir_path.glob(pattern)]
