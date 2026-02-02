"""Tests for SMA indicator."""
import numpy as np
import pytest
import py_ta as ta
import talib

from conftest import arrays_equal_with_nan


@pytest.mark.parametrize('period', [2, 5, 10, 20, 50, 100, 300, 500])
def test_sma_vs_talib(test_ohlcv_data, period):
    """Test SMA calculation against TA-Lib reference implementation.
    
    This test:
    1. Loads test OHLCV data
    2. Creates Quotes object
    3. Calculates SMA using py-ta
    4. Calculates SMA using TA-Lib
    5. Compares results with tolerance
    
    Parameters are parametrized: period.
    value='close' is fixed.
    """
    # Extract data
    open_data = test_ohlcv_data['open']
    high_data = test_ohlcv_data['high']
    low_data = test_ohlcv_data['low']
    close_data = test_ohlcv_data['close']
    volume_data = test_ohlcv_data['volume']
    
    # Check minimum data requirement
    data_length = len(close_data)
    assert data_length >= period, f"Insufficient data: {data_length} bars, need at least {period}"
    
    # Create Quotes
    quotes = ta.Quotes(open_data, high_data, low_data, close_data, volume_data)
    
    # Calculate with py-ta
    sma_result = ta.sma(quotes, period=period, value='close')
    
    # Calculate with TA-Lib
    talib_sma = talib.SMA(close_data, timeperiod=period)
    
    # Compare results
    py_ta_sma = np.asarray(sma_result.sma)
    
    assert arrays_equal_with_nan(
        py_ta_sma,
        talib_sma
    ), f"SMA (period={period}) does not match TA-Lib"

