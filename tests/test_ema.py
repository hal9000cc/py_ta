"""Tests for EMA indicator."""
import numpy as np
import py_ta as ta
import pytest
import talib

from conftest import arrays_equal_with_nan


@pytest.mark.parametrize("period", [2, 5, 10, 20, 50, 100, 300, 500])
def test_ema_vs_talib(test_ohlcv_data, period):
    """Test EMA calculation against TA-Lib reference implementation.
    
    This test:
    1. Loads test OHLCV data
    2. Creates Quotes object
    3. Calculates EMA using py-ta
    4. Calculates EMA using TA-Lib
    5. Compares results with tolerance
    
    Args:
        test_ohlcv_data: Fixture providing OHLCV test data
        period: Period for EMA calculation
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
    ema_result = ta.ema(quotes, period=period, value='close')
    
    # Calculate with TA-Lib
    talib_ema = talib.EMA(close_data, timeperiod=period)
    
    # Compare results
    py_ta_ema = np.asarray(ema_result.ema)
    
    assert arrays_equal_with_nan(
        py_ta_ema,
        talib_ema
    ), f"EMA (period={period}) does not match TA-Lib"

