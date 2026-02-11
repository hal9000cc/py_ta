"""Tests for metadata functionality."""
import pytest

import pyita as ta
from pyita.metadata import create_metadata


class TestMetadata:
    """Tests for metadata functionality."""
    
    def test_metadata(self):
        """Test that metadata() can be called without errors."""
        create_metadata()
        result = ta.metadata()
        
        assert isinstance(result, dict)
        assert len(result) > 0
        
        for indicator_name, metadata in result.items():
            assert 'name' in metadata
            assert 'signature' in metadata
            assert 'parameters' in metadata
            assert 'output_series' in metadata
            assert 'description' in metadata
            assert metadata['name'] == indicator_name

