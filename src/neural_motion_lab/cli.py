"""
Command-line interface for Neural Motion Lab.
"""

import argparse
import sys
from pathlib import Path
import numpy as np
from PIL import Image
import imageio

from neural_motion_lab import VideoPipeline
from neural_motion_lab.utils import load_config, setup_logger


def generate_command(args):
    """Generate a single video."""
    logger = setup_logger("cli.generate")
    
    # Initialize pipeline
    logger.info("Initializing pipeline...")
    if args.config:
        config = load_config(args.config)
        pipeline = VideoPipeline(**config['pipeline'])
    else:
        pipeline = VideoPipeline(
            hunyuan_model_path=args.hunyuan_model,
            lora_model_path=args.lora_model,
            device=args.device
        )
    
    pipeline.setup()
    
    # Load image
    logger.info(f"Loading image: {args.image}")
    image = Image.open(args.image)
    image_array = np.array(image)
    
    # Generate video
    logger.info("Generating video...")
    video = pipeline.generate_video(
        input_image=image_array,
        prompt=args.prompt,
        num_frames=args.num_frames,
        fps=args.fps,
        seed=args.seed
    )
    
    # Save video
    logger.info(f"Saving video: {args.output}")
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    imageio.mimsave(args.output, video, fps=args.fps)
    
    logger.info("Done!")


def batch_command(args):
    """Generate multiple videos in batch."""
    logger = setup_logger("cli.batch")
    
    # Initialize pipeline
    logger.info("Initializing pipeline...")
    pipeline = VideoPipeline(
        hunyuan_model_path=args.hunyuan_model,
        lora_model_path=args.lora_model,
        device=args.device
    )
    pipeline.setup()
    
    # Load images
    input_dir = Path(args.input_dir)
    image_files = sorted(input_dir.glob("*.jpg")) + sorted(input_dir.glob("*.png"))
    
    # Load prompts
    if args.prompts_file:
        with open(args.prompts_file) as f:
            prompts = [line.strip() for line in f if line.strip()]
    else:
        prompts = [args.prompt] * len(image_files)
    
    # Generate videos
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for i, (img_file, prompt) in enumerate(zip(image_files, prompts)):
        logger.info(f"Processing {i+1}/{len(image_files)}: {img_file.name}")
        
        # Load image
        image = np.array(Image.open(img_file))
        
        # Generate
        video = pipeline.generate_video(
            input_image=image,
            prompt=prompt,
            num_frames=args.num_frames,
            fps=args.fps
        )
        
        # Save
        output_path = output_dir / f"{img_file.stem}.mp4"
        imageio.mimsave(str(output_path), video, fps=args.fps)
    
    logger.info("Batch generation complete!")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Neural Motion Lab - Video Generation CLI"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Generate command
    generate_parser = subparsers.add_parser("generate", help="Generate a single video")
    generate_parser.add_argument("--image", required=True, help="Input image path")
    generate_parser.add_argument("--prompt", required=True, help="Text prompt")
    generate_parser.add_argument("--output", required=True, help="Output video path")
    generate_parser.add_argument("--config", help="Configuration file")
    generate_parser.add_argument("--hunyuan-model", default="models/hunyuan", help="HunyuanVideo model path")
    generate_parser.add_argument("--lora-model", help="LoRA model path")
    generate_parser.add_argument("--device", default="cuda", choices=["cuda", "cpu"], help="Device to use")
    generate_parser.add_argument("--num-frames", type=int, default=16, help="Number of frames")
    generate_parser.add_argument("--fps", type=int, default=8, help="Frames per second")
    generate_parser.add_argument("--seed", type=int, help="Random seed")
    
    # Batch command
    batch_parser = subparsers.add_parser("batch", help="Generate multiple videos")
    batch_parser.add_argument("--input-dir", required=True, help="Input images directory")
    batch_parser.add_argument("--output-dir", required=True, help="Output videos directory")
    batch_parser.add_argument("--prompts-file", help="File with prompts (one per line)")
    batch_parser.add_argument("--prompt", default="", help="Default prompt for all videos")
    batch_parser.add_argument("--hunyuan-model", default="models/hunyuan", help="HunyuanVideo model path")
    batch_parser.add_argument("--lora-model", help="LoRA model path")
    batch_parser.add_argument("--device", default="cuda", choices=["cuda", "cpu"], help="Device to use")
    batch_parser.add_argument("--num-frames", type=int, default=16, help="Number of frames")
    batch_parser.add_argument("--fps", type=int, default=8, help="Frames per second")
    
    args = parser.parse_args()
    
    if args.command == "generate":
        generate_command(args)
    elif args.command == "batch":
        batch_command(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
