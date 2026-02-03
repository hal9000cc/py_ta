"""Tests for Stochastic Oscillator indicator."""
import numpy as np
import pytest
import py_ta as ta
import talib

from conftest import arrays_equal_with_nan


@pytest.mark.parametrize('period, period_d, smooth', [
    (1, 5, 1),
    (1, 5, 3),
    (1, 1, 1),
    (2, 5, 3),
    (14, 5, 3),
])
def test_stochastic_vs_talib(test_ohlcv_data, period, period_d, smooth):
    """Test Stochastic Oscillator calculation against TA-Lib reference implementation.
    
    This test:
    1. Loads test OHLCV data
    2. Creates Quotes object
    3. Calculates Stochastic using py-ta
    4. Calculates Stochastic using TA-Lib
    5. Compares results with tolerance
    
    Parameters are parametrized: period, period_d, smooth.
    ma_type='sma' is fixed (default).
    Note: TA-Lib STOCH uses fixed smoothing (smooth=3), so we use STOCHF for custom parameters.
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
    
    # Calculate with py-ta (using default ma_type='sma')
    stoch_result = ta.stochastic(quotes, period=period, period_d=period_d, smooth=smooth, ma_type='sma')
    
    # Calculate with TA-Lib
    # talib.STOCHF uses fast stochastic with custom smoothing
    talib_slowk, talib_slowd = talib.STOCHF(
        high_data,
        low_data,
        close_data,
        fastk_period=period,
        fastd_period=period_d,
        fastd_matype=0  # SMA
    )
    
    # Compare %K (value_k) results
    assert arrays_equal_with_nan(
        stoch_result.value_k,
        talib_slowk
    ), f"Stochastic %K (period={period}, smooth={smooth}) does not match TA-Lib"
    
    # Compare %D (value_d) results
    assert arrays_equal_with_nan(
        stoch_result.value_d,
        talib_slowd
    ), f"Stochastic %D (period_d={period_d}) does not match TA-Lib"

