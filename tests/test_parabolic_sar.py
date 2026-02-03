"""Tests for Parabolic SAR indicator."""
import numpy as np
import pytest
import py_ta as ta
import talib

from conftest import arrays_equal_with_nan


@pytest.mark.parametrize('start, maximum, increment', [
    (0.02, 0.2, 0.02),
    (0.01, 0.2, 0.02),
    (0.02, 0.3, 0.01),
])
def test_parabolic_sar_vs_talib(test_ohlcv_data, start, maximum, increment):
    """Test Parabolic SAR calculation against TA-Lib reference implementation.
    
    This test:
    1. Loads test OHLCV data
    2. Creates Quotes object
    3. Calculates Parabolic SAR using py-ta
    4. Calculates Parabolic SAR using TA-Lib
    5. Compares results with tolerance
    
    Parameters are parametrized: start, maximum, increment.
    Note: TA-Lib SAR uses fixed parameters (start=0.02, increment=0.02, maximum=0.2),
    so we can only test with default values or use SAREXT for custom parameters.
    """
    # Extract data
    open_data = test_ohlcv_data['open']
    high_data = test_ohlcv_data['high']
    low_data = test_ohlcv_data['low']
    close_data = test_ohlcv_data['close']
    volume_data = test_ohlcv_data['volume']
    
    # Check minimum data requirement
    data_length = len(close_data)
    assert data_length >= 3, f"Insufficient data: {data_length} bars, need at least 3"
    
    # Create Quotes
    quotes = ta.Quotes(open_data, high_data, low_data, close_data, volume_data)
    
    # Calculate with py-ta
    sar_result = ta.parabolic_sar(quotes, start=start, maximum=maximum, increment=increment)
    
    # Calculate with TA-Lib
    # talib.SAR uses fixed parameters, so we use SAREXT for custom parameters
    talib_sar = talib.SAREXT(
        high_data,
        low_data,
        startvalue=start,
        offsetonreverse=0.0,
        accelerationinitlong=start,
        accelerationlong=increment,
        accelerationmaxlong=maximum,
        accelerationinitshort=start,
        accelerationshort=increment,
        accelerationmaxshort=maximum
    )
    
    # Compare SAR results
    assert arrays_equal_with_nan(
        sar_result.sar,
        talib_sar
    ), f"Parabolic SAR (start={start}, maximum={maximum}, increment={increment}) does not match TA-Lib"

