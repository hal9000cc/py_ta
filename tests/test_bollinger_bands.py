"""Tests for Bollinger Bands indicator."""
import numpy as np
import pytest
import pyita as ta
import talib

from conftest import arrays_equal_with_nan


@pytest.mark.parametrize('period, deviation', [
    (200, 3),
    (2, 1),
    (2, 2),
    (20, 1),
    (20, 3),
    (4, 2),
])
def test_bollinger_bands_vs_talib(test_ohlcv_data, period, deviation):
    """Test Bollinger Bands calculation against TA-Lib reference implementation.
    
    This test:
    1. Loads test OHLCV data
    2. Creates Quotes object
    3. Calculates Bollinger Bands using pyita
    4. Calculates Bollinger Bands using TA-Lib
    5. Compares results with tolerance
    
    Parameters are parametrized: period and deviation.
    ma_type='sma' and value='close' are fixed.
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
    
    # Calculate with pyita
    bb = ta.bollinger_bands(quotes, period=period, deviation=deviation, ma_type='sma', value='close')
    
    # Calculate with TA-Lib
    # talib.BBANDS(close, timeperiod=period, nbdevup=deviation, nbdevdn=deviation, matype=0)
    # matype: 0=SMA, 1=EMA, 2=WMA, 3=DEMA, 4=TEMA, 5=TRIMA, 6=KAMA, 7=MAMA, 8=T3
    talib_upper, talib_middle, talib_lower = talib.BBANDS(
        close_data,
        timeperiod=period,
        nbdevup=deviation,
        nbdevdn=deviation,
        matype=0  # SMA
    )
    
    # Compare results
    # Compare middle line
    assert arrays_equal_with_nan(
        bb.mid_line,
        talib_middle
    ), f"Middle line (SMA, period={period}, deviation={deviation}) does not match TA-Lib"
    
    # Compare upper band
    assert arrays_equal_with_nan(
        bb.up_line,
        talib_upper
    ), f"Upper band (period={period}, deviation={deviation}) does not match TA-Lib"
    
    # Compare lower band
    assert arrays_equal_with_nan(
        bb.down_line,
        talib_lower
    ), f"Lower band (period={period}, deviation={deviation}) does not match TA-Lib"


@pytest.mark.parametrize('period, deviation_up, deviation_down', [
    (200, 3, 2),
    (2, 1, 0.5),
    (2, 2, 1),
    (20, 2.5, 1.5),
    (20, 3, 1),
    (4, 2, 1),
])
def test_bollinger_bands_different_deviations_vs_talib(test_ohlcv_data, period, deviation_up, deviation_down):
    """Test Bollinger Bands calculation with different deviations against TA-Lib reference implementation.
    
    This test:
    1. Loads test OHLCV data
    2. Creates Quotes object
    3. Calculates Bollinger Bands using pyita with different deviations for upper and lower bands
    4. Calculates Bollinger Bands using TA-Lib with corresponding parameters
    5. Compares results with tolerance
    
    Parameters are parametrized: period, deviation_up, and deviation_down.
    ma_type='sma' and value='close' are fixed.
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
    
    # Calculate with pyita
    bb = ta.bollinger_bands(quotes, period=period, deviation_up=deviation_up, deviation_down=deviation_down, ma_type='sma', value='close')
    
    # Calculate with TA-Lib
    # talib.BBANDS(close, timeperiod=period, nbdevup=deviation_up, nbdevdn=deviation_down, matype=0)
    # matype: 0=SMA, 1=EMA, 2=WMA, 3=DEMA, 4=TEMA, 5=TRIMA, 6=KAMA, 7=MAMA, 8=T3
    talib_upper, talib_middle, talib_lower = talib.BBANDS(
        close_data,
        timeperiod=period,
        nbdevup=deviation_up,
        nbdevdn=deviation_down,
        matype=0  # SMA
    )
    
    # Compare results
    # Compare middle line
    assert arrays_equal_with_nan(
        bb.mid_line,
        talib_middle
    ), f"Middle line (SMA, period={period}, deviation_up={deviation_up}, deviation_down={deviation_down}) does not match TA-Lib"
    
    # Compare upper band
    assert arrays_equal_with_nan(
        bb.up_line,
        talib_upper
    ), f"Upper band (period={period}, deviation_up={deviation_up}) does not match TA-Lib"
    
    # Compare lower band
    assert arrays_equal_with_nan(
        bb.down_line,
        talib_lower
    ), f"Lower band (period={period}, deviation_down={deviation_down}) does not match TA-Lib"

