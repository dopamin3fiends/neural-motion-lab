"""
Integration test for basic video generation.
"""

import pytest
import numpy as np
from neural_motion_lab.pipelines import VideoPipeline


@pytest.mark.integration
@pytest.mark.slow
class TestVideoGeneration:
    """Integration tests for video generation pipeline."""
    
    @pytest.fixture
    def dummy_image(self):
        """Create a dummy image for testing."""
        return np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)
    
    def test_pipeline_initialization(self):
        """Test that pipeline can be initialized."""
        pipeline = VideoPipeline(
            hunyuan_model_path="models/hunyuan",
            device="cpu"  # Use CPU for testing
        )
        assert pipeline is not None
