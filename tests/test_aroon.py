"""Tests for Aroon indicator."""
import numpy as np
import pytest
import py_ta as ta
import talib

from conftest import arrays_equal_with_nan


@pytest.mark.parametrize('period', [2, 7, 14])
def test_aroon_vs_talib(test_ohlcv_data, period):
    """Test Aroon calculation against TA-Lib reference implementation.
    
    This test:
    1. Loads test OHLCV data
    2. Creates Quotes object
    3. Calculates Aroon using py-ta
    4. Calculates Aroon using TA-Lib
    5. Compares results with tolerance
    
    Parameters are parametrized: period.
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
    aroon_result = ta.aroon(quotes, period=period)
    
    # Calculate with TA-Lib
    talib_aroon_down, talib_aroon_up = talib.AROON(high_data, low_data, timeperiod=period)
    
    # Compare Aroon Up results
    assert arrays_equal_with_nan(
        aroon_result.up,
        talib_aroon_up
    ), f"Aroon Up (period={period}) does not match TA-Lib"
    
    # Compare Aroon Down results
    assert arrays_equal_with_nan(
        aroon_result.down,
        talib_aroon_down
    ), f"Aroon Down (period={period}) does not match TA-Lib"


@pytest.mark.parametrize('period', [2, 7, 14])
def test_aroon_oscillator_vs_talib(test_ohlcv_data, period):
    """Test Aroon Oscillator calculation against TA-Lib reference implementation."""
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
    aroon_result = ta.aroon(quotes, period=period)
    
    # Calculate with TA-Lib
    talib_aroonosc = talib.AROONOSC(high_data, low_data, timeperiod=period)
    
    # Compare Aroon Oscillator results
    assert arrays_equal_with_nan(
        aroon_result.oscillator,
        talib_aroonosc
    ), f"Aroon Oscillator (period={period}) does not match TA-Lib"

