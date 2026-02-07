"""Tests for Supertrend indicator."""
import pytest
import py_ta as ta

from conftest import test_ohlcv_data


def test_supertrend_not_implemented(test_ohlcv_data):
    """Test for Supertrend is not implemented yet.
    
    Supertrend is not available in TA-Lib for comparison,
    so this test is not implemented.
    """
    pytest.skip("Supertrend test is not implemented: TA-Lib does not have this indicator")


def test_supertrend_basic(test_ohlcv_data):
    """Basic test for Supertrend (placeholder).
    
    This test verifies that the indicator can be called without errors.
    """
    # Extract data
    open_data = test_ohlcv_data['open']
    high_data = test_ohlcv_data['high']
    low_data = test_ohlcv_data['low']
    close_data = test_ohlcv_data['close']
    volume_data = test_ohlcv_data['volume']
    
    quotes = ta.Quotes(open_data, high_data, low_data, close_data, volume_data)
    
    supertrend_result = ta.supertrend(quotes, period=10, multipler=3, ma_type='mma')
    
    assert hasattr(supertrend_result, 'supertrend'), "Result should have 'supertrend' attribute"
    assert hasattr(supertrend_result, 'supertrend_mid'), "Result should have 'supertrend_mid' attribute"
    assert len(supertrend_result.supertrend) == len(close_data), "supertrend should have same length as input data"
    assert len(supertrend_result.supertrend_mid) == len(close_data), "supertrend_mid should have same length as input data"

