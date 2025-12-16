#!/usr/bin/env python3
"""
Neural Motion Lab - Workflow Loader
Utility to programmatically load workflows into ComfyUI
"""

import os
import sys
import json
import argparse
import shutil
from pathlib import Path


class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_success(message):
    print(f"{Colors.GREEN}✓ {message}{Colors.END}")


def print_warning(message):
    print(f"{Colors.YELLOW}⚠ {message}{Colors.END}")


def print_error(message):
    print(f"{Colors.RED}✗ {message}{Colors.END}")


def print_info(message):
    print(f"{Colors.CYAN}ℹ {message}{Colors.END}")


def find_comfyui_path():
    """Try to find ComfyUI installation path"""
    possible_paths = [
        Path.home() / "ComfyUI",
        Path.cwd().parent / "ComfyUI",
        Path("/opt/ComfyUI"),
    ]
    
    for path in possible_paths:
        if path.exists() and (path / "main.py").exists():
            return path
    
    return None


def validate_workflow(workflow_path):
    """Validate that the workflow file is valid JSON"""
    try:
        with open(workflow_path, 'r') as f:
            data = json.load(f)
        
        # Check for required fields
        if 'nodes' not in data:
            print_error("Invalid workflow: missing 'nodes' field")
            return False
        
        if 'links' not in data:
            print_error("Invalid workflow: missing 'links' field")
            return False
        
        print_success(f"Workflow validation passed: {len(data['nodes'])} nodes, {len(data['links'])} links")
        return True
        
    except json.JSONDecodeError as e:
        print_error(f"Invalid JSON in workflow file: {e}")
        return False
    except Exception as e:
        print_error(f"Error validating workflow: {e}")
        return False


def list_workflows():
    """List available workflows"""
    base_dir = Path(__file__).parent.parent
    workflow_dir = base_dir / "workflows"
    
    if not workflow_dir.exists():
        print_error("Workflows directory not found")
        return []
    
    workflows = list(workflow_dir.glob("*.json"))
    
    if not workflows:
        print_warning("No workflow files found")
        return []
    
    print(f"\n{Colors.BOLD}Available Workflows:{Colors.END}\n")
    
    for i, workflow in enumerate(workflows, 1):
        print(f"{i}. {Colors.CYAN}{workflow.stem}{Colors.END}")
        
        # Try to read description from workflow
        try:
            with open(workflow, 'r') as f:
                data = json.load(f)
                if 'extra' in data and 'description' in data['extra']:
                    print(f"   {data['extra']['description']}")
                print(f"   File: {workflow.name}")
        except:
            print(f"   File: {workflow.name}")
        
        print()
    
    return workflows


def copy_workflow_to_comfyui(workflow_path, comfyui_path, workflow_name=None):
    """Copy workflow to ComfyUI user directory"""
    if not comfyui_path:
        print_error("ComfyUI path not provided")
        return False
    
    # ComfyUI stores workflows in user/default/workflows or at root
    user_workflows = comfyui_path / "user" / "default" / "workflows"
    user_workflows.mkdir(parents=True, exist_ok=True)
    
    if workflow_name:
        dest_name = workflow_name if workflow_name.endswith('.json') else f"{workflow_name}.json"
    else:
        dest_name = workflow_path.name
    
    dest_path = user_workflows / dest_name
    
    try:
        shutil.copy(workflow_path, dest_path)
        print_success(f"Copied workflow to: {dest_path}")
        return True
    except Exception as e:
        print_error(f"Failed to copy workflow: {e}")
        return False


def create_api_workflow(workflow_path, output_path=None):
    """Convert workflow to API format"""
    try:
        with open(workflow_path, 'r') as f:
            workflow = json.load(f)
        
        # ComfyUI API format is similar but may need modifications
        # For now, just copy the workflow
        if output_path is None:
            output_path = workflow_path.parent / f"{workflow_path.stem}_api.json"
        
        with open(output_path, 'w') as f:
            json.dump(workflow, f, indent=2)
        
        print_success(f"Created API workflow: {output_path}")
        return True
        
    except Exception as e:
        print_error(f"Failed to create API workflow: {e}")
        return False


def get_workflow_info(workflow_path):
    """Get detailed information about a workflow"""
    try:
        with open(workflow_path, 'r') as f:
            data = json.load(f)
        
        print(f"\n{Colors.BOLD}Workflow: {workflow_path.name}{Colors.END}\n")
        print(f"Nodes: {len(data.get('nodes', []))}")
        print(f"Links: {len(data.get('links', []))}")
        
        # Count node types
        node_types = {}
        for node in data.get('nodes', []):
            node_type = node.get('type', 'Unknown')
            node_types[node_type] = node_types.get(node_type, 0) + 1
        
        print(f"\n{Colors.BOLD}Node Types:{Colors.END}")
        for node_type, count in sorted(node_types.items()):
            print(f"  {node_type}: {count}")
        
        return True
        
    except Exception as e:
        print_error(f"Error reading workflow: {e}")
        return False


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Load and manage Neural Motion Lab workflows"
    )
    
    parser.add_argument(
        'workflow',
        nargs='?',
        help="Workflow name or path to load"
    )
    
    parser.add_argument(
        '--list',
        action='store_true',
        help="List available workflows"
    )
    
    parser.add_argument(
        '--info',
        action='store_true',
        help="Show workflow information"
    )
    
    parser.add_argument(
        '--validate',
        action='store_true',
        help="Validate workflow file"
    )
    
    parser.add_argument(
        '--copy-to-comfyui',
        action='store_true',
        help="Copy workflow to ComfyUI directory"
    )
    
    parser.add_argument(
        '--comfyui-path',
        type=str,
        help="Path to ComfyUI installation"
    )
    
    parser.add_argument(
        '--api-format',
        action='store_true',
        help="Convert to API format"
    )
    
    args = parser.parse_args()
    
    base_dir = Path(__file__).parent.parent
    workflow_dir = base_dir / "workflows"
    
    # List workflows
    if args.list:
        list_workflows()
        return
    
    # Need a workflow for other operations
    if not args.workflow:
        print_error("No workflow specified")
        print_info("Use --list to see available workflows")
        sys.exit(1)
    
    # Find workflow file
    workflow_path = Path(args.workflow)
    if not workflow_path.exists():
        # Try in workflows directory
        workflow_path = workflow_dir / args.workflow
        if not workflow_path.suffix:
            workflow_path = workflow_path.with_suffix('.json')
    
    if not workflow_path.exists():
        print_error(f"Workflow not found: {args.workflow}")
        sys.exit(1)
    
    print_info(f"Using workflow: {workflow_path}")
    
    # Validate
    if args.validate or args.info or args.copy_to_comfyui or args.api_format:
        if not validate_workflow(workflow_path):
            sys.exit(1)
    
    # Show info
    if args.info:
        get_workflow_info(workflow_path)
    
    # Copy to ComfyUI
    if args.copy_to_comfyui:
        comfyui_path = args.comfyui_path
        if not comfyui_path:
            comfyui_path = find_comfyui_path()
        
        if not comfyui_path:
            print_error("ComfyUI path not found")
            print_info("Use --comfyui-path to specify location")
            sys.exit(1)
        
        copy_workflow_to_comfyui(workflow_path, Path(comfyui_path))
    
    # API format
    if args.api_format:
        create_api_workflow(workflow_path)
    
    print_success("Done!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Interrupted by user{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print_error(f"Error: {e}")
        sys.exit(1)
