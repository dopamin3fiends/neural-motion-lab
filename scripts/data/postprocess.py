#!/usr/bin/env python3
"""
Video postprocessing script for Neural Motion Lab.
"""

import argparse
import numpy as np
from pathlib import Path
import imageio


def save_video(frames: np.ndarray, output_path: str, fps: int = 8) -> None:
    """
    Save video frames to file.
    
    Args:
        frames: Array of video frames
        output_path: Path to save video
        fps: Frames per second
    """
    writer = imageio.get_writer(output_path, fps=fps)
    
    for frame in frames:
        writer.append_data(frame)
    
    writer.close()
    print(f"Video saved to: {output_path}")


def extract_frames(video_path: str, output_dir: str) -> None:
    """
    Extract frames from a video file.
    
    Args:
        video_path: Path to input video
        output_dir: Directory to save extracted frames
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    reader = imageio.get_reader(video_path)
    
    for i, frame in enumerate(reader):
        frame_path = output_path / f"frame_{i:04d}.png"
        imageio.imwrite(frame_path, frame)
        print(f"Extracted frame {i} to {frame_path}")
    
    reader.close()


def main():
    parser = argparse.ArgumentParser(description='Postprocess videos')
    parser.add_argument('action', choices=['extract'], help='Action to perform')
    parser.add_argument('input', help='Input video file')
    parser.add_argument('output', help='Output directory')
    
    args = parser.parse_args()
    
    if args.action == 'extract':
        extract_frames(args.input, args.output)


if __name__ == '__main__':
    main()
