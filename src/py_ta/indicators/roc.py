"""roc(quotes, period=14, ma_period=14, ma_type='sma', value='close')
Rate of Change."""
import numpy as np

from ..indicator_result import IndicatorResult
from ..move_average import ma_calculate, MA_Type
from ..exceptions import PyTAExceptionBadParameterValue, PyTAExceptionTooLittleData
from ..constants import PRICE_TYPE


def get_indicator_out(quotes, period=14, ma_period=14, ma_type='sma', value='close'):
    """Calculate Rate of Change (ROC).
    
    ROC is a momentum oscillator that measures the percentage change in price
    over a specified period. It shows the speed at which price is changing.
    
    Args:
        quotes: Quotes object containing OHLCV data
        period: Period for ROC calculation (default: 14)
        ma_period: Period for smoothing ROC (default: 14)
        ma_type: Type of moving average for smoothing - 'sma', 'ema', 'mma', 'ema0', 'mma0' (default: 'sma')
        value: Price field to use - 'open', 'high', 'low', or 'close' (default: 'close')
        
    Returns:
        IndicatorResult object with attributes:
            - roc: Rate of Change values (first period elements are NaN)
            - smooth_roc: Smoothed ROC values (first period elements are NaN)
            
    Raises:
        PyTAExceptionBadParameterValue: If period <= 0, ma_period <= 0, value is invalid, or ma_type is invalid
        PyTAExceptionDataSeriesNonFound: If the specified value series is not found
        PyTAExceptionTooLittleData: If data length is insufficient
        
    Example:
        >>> roc_result = roc(quotes, period=14, ma_period=14)
        >>> print(roc_result.roc)
        >>> print(roc_result.smooth_roc)
    """
    # Validate period
    if period <= 0:
        raise PyTAExceptionBadParameterValue(f'period must be greater than 0, got {period}')
    
    # Validate ma_period
    if ma_period <= 0:
        raise PyTAExceptionBadParameterValue(f'ma_period must be greater than 0, got {ma_period}')
    
    # Validate value
    valid_values = ['open', 'high', 'low', 'close']
    if value not in valid_values:
        raise PyTAExceptionBadParameterValue(f'value must be one of {valid_values}, got {value}')
    
    # Convert ma_type string to MA_Type enum (will raise ValueError if invalid)
    try:
        ma_type_enum = MA_Type.cast(ma_type)
    except ValueError as e:
        raise PyTAExceptionBadParameterValue(str(e))
    
    # Get source values from quotes
    source_values = quotes[value]
    
    # Check minimum data requirement
    data_len = len(source_values)
    if data_len < period:
        raise PyTAExceptionTooLittleData(f'data length {data_len} < {period}')
    
    # Calculate ROC
    # ROC = (current - previous) / previous
    # source_values[period:] - current values starting from index 'period'
    # source_values[:-period] - previous values (period bars ago)
    roc = (source_values[period:] - source_values[:-period]) / source_values[:-period]
    
    # Handle division by zero
    np.seterr(divide='ignore', invalid='ignore')
    roc[source_values[:-period] == 0] = 0
    
    # Smooth ROC
    smooth_roc = ma_calculate(roc, ma_period, ma_type_enum)
    
    # Create beginning array with NaN values
    begin = np.array([np.nan] * period, dtype=PRICE_TYPE)
    
    return IndicatorResult({
        'roc': np.hstack((begin, roc)),
        'smooth_roc': np.hstack((begin, smooth_roc))
    })

