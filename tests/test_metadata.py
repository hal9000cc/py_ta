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
            
            # Check output_series structure and types
            for series in metadata['output_series']:
                assert 'name' in series
                assert 'type' in series
                assert isinstance(series['name'], str)
                assert isinstance(series['type'], str)
                assert series['type'] in ('price', 'as_source', 'none'), \
                    f"Invalid series type '{series['type']}' for {indicator_name}.{series['name']}"

    def test_version(self):
        """Test that __version__ is accessible and is a valid version string."""
        assert hasattr(ta, '__version__')
        version = ta.__version__
        assert isinstance(version, str)
        assert len(version) > 0
        # Version should be in format like "1.0.13" or similar
        assert '.' in version


