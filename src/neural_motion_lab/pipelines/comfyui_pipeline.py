"""
ComfyUI integration pipeline.
"""

from typing import Dict, Any, Optional
import json


class ComfyUIPipeline:
    """
    Pipeline for ComfyUI integration.
    
    This pipeline provides integration with ComfyUI workflows for
    interactive video generation.
    """
    
    def __init__(self, workflow_path: Optional[str] = None):
        """
        Initialize ComfyUI pipeline.
        
        Args:
            workflow_path: Path to ComfyUI workflow JSON file
        """
        self.workflow_path = workflow_path
        self.workflow = None
        
    def load_workflow(self, path: Optional[str] = None) -> Dict[str, Any]:
        """
        Load a ComfyUI workflow from JSON.
        
        Args:
            path: Path to workflow file (uses default if not provided)
            
        Returns:
            Workflow configuration dictionary
        """
        workflow_file = path or self.workflow_path
        
        if not workflow_file:
            raise ValueError("No workflow path provided")
            
        with open(workflow_file, 'r') as f:
            self.workflow = json.load(f)
            
        return self.workflow
        
    def save_workflow(self, path: str, workflow: Optional[Dict[str, Any]] = None) -> None:
        """
        Save a ComfyUI workflow to JSON.
        
        Args:
            path: Path to save workflow file
            workflow: Workflow dictionary (uses current if not provided)
        """
        workflow_data = workflow or self.workflow
        
        if not workflow_data:
            raise ValueError("No workflow to save")
            
        with open(path, 'w') as f:
            json.dump(workflow_data, f, indent=2)
            
    def update_workflow_params(self, params: Dict[str, Any]) -> None:
        """
        Update workflow parameters.
        
        Args:
            params: Dictionary of parameters to update
        """
        if not self.workflow:
            raise ValueError("No workflow loaded")
            
        # Perform deep merge of parameters
        self._deep_merge(self.workflow, params)
        
    def _deep_merge(self, base: Dict[str, Any], update: Dict[str, Any]) -> None:
        """
        Recursively merge update dictionary into base dictionary.
        
        Args:
            base: Base dictionary to update
            update: Dictionary with updates to apply
        """
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value
        
    def execute(self, server_url: str = "http://127.0.0.1:8188") -> Dict[str, Any]:
        """
        Execute the workflow on a ComfyUI server.
        
        NOTE: This is a placeholder implementation. In production, this should:
        - Send the workflow to the ComfyUI server via its API
        - Monitor the execution progress
        - Handle errors and retries
        - Return the results including output paths
        
        Args:
            server_url: URL of the ComfyUI server
            
        Returns:
            Execution result
        """
        if not self.workflow:
            raise ValueError("No workflow loaded")
            
        # TODO: Implement actual ComfyUI API call using websockets/HTTP
        # Example: POST to /prompt endpoint with the workflow
        print(f"Executing workflow on {server_url}")
        return {"status": "success", "message": "Workflow executed"}
