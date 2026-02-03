"""Tests for OBV indicator."""
import numpy as np
import pytest
import py_ta as ta
import talib

from conftest import arrays_equal_with_nan


def test_obv_vs_talib(test_ohlcv_data):
    """Test OBV calculation against TA-Lib reference implementation.
    
    This test:
    1. Loads test OHLCV data
    2. Creates Quotes object
    3. Calculates OBV using py-ta
    4. Calculates OBV using TA-Lib
    5. Compares results with tolerance
    
    OBV doesn't have parameters, only requires OHLCV data.
    """
    # Extract data
    open_data = test_ohlcv_data['open']
    high_data = test_ohlcv_data['high']
    low_data = test_ohlcv_data['low']
    close_data = test_ohlcv_data['close']
    volume_data = test_ohlcv_data['volume']
    
    # OBV needs at least 1 bar
    data_length = len(close_data)
    assert data_length >= 1, f"Insufficient data: {data_length} bars, need at least 1"
    
    # Create Quotes
    quotes = ta.Quotes(open_data, high_data, low_data, close_data, volume_data)
    
    # Calculate with py-ta
    obv_result = ta.obv(quotes)
    
    # Calculate with TA-Lib
    talib_obv = talib.OBV(close_data, volume_data)
    
    # Compare OBV results
    assert arrays_equal_with_nan(
        obv_result.obv,
        talib_obv
    ), f"OBV does not match TA-Lib"

