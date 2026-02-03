"""Tests for ADX indicator."""
import numpy as np
import pytest
import py_ta as ta
import talib

from conftest import arrays_equal_with_nan


@pytest.mark.parametrize('period', [14, 2])
def test_adx_vs_talib(test_ohlcv_data, period):
    """Test ADX calculation against TA-Lib reference implementation.
    
    This test:
    1. Loads test OHLCV data
    2. Creates Quotes object
    3. Calculates ADX using py-ta
    4. Calculates ADX using TA-Lib
    5. Compares results with tolerance
    
    Parameters are parametrized: period.
    smooth=period and ma_type='mma' are fixed (defaults).
    Note: TA-Lib ADX uses Wilder's smoothing (similar to MMA).
    """
    # Extract data
    open_data = test_ohlcv_data['open']
    high_data = test_ohlcv_data['high']
    low_data = test_ohlcv_data['low']
    close_data = test_ohlcv_data['close']
    volume_data = test_ohlcv_data['volume']
    
    # Check minimum data requirement
    # ADX needs at least period bars
    data_length = len(close_data)
    assert data_length >= period, f"Insufficient data: {data_length} bars, need at least {period}"
    
    # Create Quotes
    quotes = ta.Quotes(open_data, high_data, low_data, close_data, volume_data)
    
    # Calculate with py-ta (using default smooth=period, ma_type='mma')
    adx_result = ta.adx(quotes, period=period, smooth=period, ma_type='mmaw')
    
    # Calculate with TA-Lib
    # talib.ADX uses Wilder's smoothing (similar to MMA)
    talib_adx = talib.ADX(high_data, low_data, close_data, timeperiod=period)
    
    # Compare ADX results
    assert arrays_equal_with_nan(
        adx_result.adx,
        talib_adx
    ), f"ADX (period={period}) does not match TA-Lib"


@pytest.mark.parametrize('period', [14, 2])
def test_plus_di_vs_talib(test_ohlcv_data, period):
    """Test Plus DI calculation against TA-Lib reference implementation."""
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
    adx_result = ta.adx(quotes, period=period, smooth=period, ma_type='mmaw')
    
    # Calculate with TA-Lib
    talib_plus_di = talib.PLUS_DI(high_data, low_data, close_data, timeperiod=period)
    
    # Compare Plus DI results
    assert arrays_equal_with_nan(
        adx_result.p_di,
        talib_plus_di
    ), f"Plus DI (period={period}) does not match TA-Lib"


@pytest.mark.parametrize('period', [14, 2])
def test_minus_di_vs_talib(test_ohlcv_data, period):
    """Test Minus DI calculation against TA-Lib reference implementation."""
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
    adx_result = ta.adx(quotes, period=period, smooth=period, ma_type='mma')
    
    # Calculate with TA-Lib
    talib_minus_di = talib.MINUS_DI(high_data, low_data, close_data, timeperiod=period)
    
    # Compare Minus DI results
    assert arrays_equal_with_nan(
        adx_result.m_di,
        talib_minus_di
    ), f"Minus DI (period={period}) does not match TA-Lib"

