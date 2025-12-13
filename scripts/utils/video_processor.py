"""Video processor utility for Neural Motion Lab."""

import cv2
import numpy as np
from pathlib import Path
from typing import List, Optional, Union, Tuple
import logging
import imageio
from PIL import Image

logger = logging.getLogger(__name__)


class VideoProcessor:
    """Process and save video outputs."""
    
    def __init__(self, output_dir: Optional[Union[str, Path]] = None):
        """
        Initialize VideoProcessor.
        
        Args:
            output_dir: Default output directory for saved videos
        """
        self.output_dir = Path(output_dir) if output_dir else Path("outputs")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def save_video(
        self,
        frames: Union[List[np.ndarray], np.ndarray],
        output_path: Union[str, Path],
        fps: int = 24,
        codec: str = 'mp4v',
        quality: int = 9
    ) -> Path:
        """
        Save frames as video file.
        
        Args:
            frames: List of frames or 4D array (num_frames, height, width, channels)
            output_path: Path to save video
            fps: Frames per second
            codec: Video codec ('mp4v', 'avc1', 'h264', 'h265')
            quality: Quality level (0-10, higher is better)
            
        Returns:
            Path to saved video file
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert frames to list of numpy arrays
        if isinstance(frames, np.ndarray):
            if frames.ndim == 4:
                frames = [frames[i] for i in range(frames.shape[0])]
            else:
                frames = [frames]
        
        if not frames:
            raise ValueError("No frames to save")
        
        # Get frame dimensions
        height, width = frames[0].shape[:2]
        
        logger.info(f"Saving video to {output_path} ({len(frames)} frames, {width}x{height}, {fps}fps)")
        
        # Choose save method based on output format
        if output_path.suffix.lower() == '.gif':
            self._save_gif(frames, output_path, fps)
        elif output_path.suffix.lower() in ['.mp4', '.avi', '.mov']:
            self._save_with_opencv(frames, output_path, fps, codec)
        else:
            raise ValueError(f"Unsupported video format: {output_path.suffix}")
        
        logger.info(f"Video saved successfully: {output_path}")
        return output_path
    
    def _save_with_opencv(
        self,
        frames: List[np.ndarray],
        output_path: Path,
        fps: int,
        codec: str
    ) -> None:
        """Save video using OpenCV."""
        height, width = frames[0].shape[:2]
        
        # Get codec fourcc
        fourcc = cv2.VideoWriter_fourcc(*codec)
        
        # Create video writer
        writer = cv2.VideoWriter(
            str(output_path),
            fourcc,
            fps,
            (width, height)
        )
        
        try:
            for frame in frames:
                # Convert RGB to BGR for OpenCV
                if frame.shape[-1] == 3:
                    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                writer.write(frame)
        finally:
            writer.release()
    
    def _save_gif(
        self,
        frames: List[np.ndarray],
        output_path: Path,
        fps: int
    ) -> None:
        """Save video as GIF using imageio."""
        # Convert to uint8 if needed
        frames_uint8 = []
        for frame in frames:
            if frame.dtype != np.uint8:
                frame = np.clip(frame * 255, 0, 255).astype(np.uint8)
            frames_uint8.append(frame)
        
        duration = 1000 / fps  # Duration in milliseconds
        imageio.mimsave(str(output_path), frames_uint8, duration=duration)
    
    def save_frames(
        self,
        frames: Union[List[np.ndarray], np.ndarray],
        output_dir: Union[str, Path],
        prefix: str = "frame",
        format: str = "png"
    ) -> List[Path]:
        """
        Save individual frames as images.
        
        Args:
            frames: List of frames or 4D array
            output_dir: Directory to save frames
            prefix: Filename prefix
            format: Image format (png, jpg, etc.)
            
        Returns:
            List of paths to saved frames
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Convert frames to list
        if isinstance(frames, np.ndarray) and frames.ndim == 4:
            frames = [frames[i] for i in range(frames.shape[0])]
        
        saved_paths = []
        
        logger.info(f"Saving {len(frames)} frames to {output_dir}")
        
        for i, frame in enumerate(frames):
            output_path = output_dir / f"{prefix}_{i:04d}.{format}"
            
            # Convert to PIL Image and save
            if frame.dtype != np.uint8:
                frame = np.clip(frame * 255, 0, 255).astype(np.uint8)
            
            img = Image.fromarray(frame)
            img.save(output_path)
            saved_paths.append(output_path)
        
        logger.info(f"Frames saved successfully")
        return saved_paths
    
    def load_video(
        self,
        video_path: Union[str, Path],
        max_frames: Optional[int] = None
    ) -> Tuple[List[np.ndarray], int]:
        """
        Load video file as frames.
        
        Args:
            video_path: Path to video file
            max_frames: Maximum number of frames to load
            
        Returns:
            Tuple of (frames list, fps)
        """
        video_path = Path(video_path)
        
        if not video_path.exists():
            raise FileNotFoundError(f"Video not found: {video_path}")
        
        logger.info(f"Loading video from {video_path}")
        
        cap = cv2.VideoCapture(str(video_path))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        
        frames = []
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Convert BGR to RGB
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frames.append(frame)
                
                if max_frames and len(frames) >= max_frames:
                    break
        finally:
            cap.release()
        
        logger.info(f"Loaded {len(frames)} frames at {fps}fps")
        return frames, fps
    
    def load_image(self, image_path: Union[str, Path]) -> np.ndarray:
        """
        Load image file.
        
        Args:
            image_path: Path to image file
            
        Returns:
            Image as numpy array (RGB)
        """
        image_path = Path(image_path)
        
        if not image_path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        logger.info(f"Loading image from {image_path}")
        
        img = Image.open(image_path).convert('RGB')
        return np.array(img)
    
    def resize_frames(
        self,
        frames: List[np.ndarray],
        size: Tuple[int, int],
        interpolation: int = cv2.INTER_LANCZOS4
    ) -> List[np.ndarray]:
        """
        Resize frames to target size.
        
        Args:
            frames: List of frames
            size: Target size as (width, height)
            interpolation: Interpolation method
            
        Returns:
            List of resized frames
        """
        logger.info(f"Resizing {len(frames)} frames to {size}")
        
        resized = []
        for frame in frames:
            resized_frame = cv2.resize(frame, size, interpolation=interpolation)
            resized.append(resized_frame)
        
        return resized
    
    def concatenate_videos(
        self,
        video_paths: List[Union[str, Path]],
        output_path: Union[str, Path],
        fps: Optional[int] = None
    ) -> Path:
        """
        Concatenate multiple videos into one.
        
        Args:
            video_paths: List of video file paths
            output_path: Output video path
            fps: Output FPS (uses first video's FPS if None)
            
        Returns:
            Path to concatenated video
        """
        all_frames = []
        video_fps = None
        
        for video_path in video_paths:
            frames, vid_fps = self.load_video(video_path)
            all_frames.extend(frames)
            
            if video_fps is None:
                video_fps = vid_fps
        
        if fps is None:
            fps = video_fps or 24
        
        return self.save_video(all_frames, output_path, fps=fps)
    
    def apply_color_correction(
        self,
        frames: List[np.ndarray],
        brightness: float = 1.0,
        contrast: float = 1.0,
        saturation: float = 1.0
    ) -> List[np.ndarray]:
        """
        Apply color correction to frames.
        
        Args:
            frames: List of frames
            brightness: Brightness multiplier (1.0 = no change)
            contrast: Contrast multiplier (1.0 = no change)
            saturation: Saturation multiplier (1.0 = no change)
            
        Returns:
            List of corrected frames
        """
        corrected = []
        
        for frame in frames:
            # Convert to float
            img = frame.astype(np.float32) / 255.0
            
            # Apply brightness
            img = img * brightness
            
            # Apply contrast
            img = (img - 0.5) * contrast + 0.5
            
            # Apply saturation
            if saturation != 1.0:
                # Convert to HSV
                hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
                hsv[:, :, 1] = hsv[:, :, 1] * saturation
                img = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
            
            # Clip and convert back
            img = np.clip(img * 255, 0, 255).astype(np.uint8)
            corrected.append(img)
        
        return corrected
