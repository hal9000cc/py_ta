"""py-ta: Technical analysis library for stock quotes.

This module provides technical indicators for analyzing stock market data.
Indicators are loaded lazily when first accessed.

Example:
    >>> import py_ta as ta
    >>> quotes = ta.Quotes(open, high, low, close)
    >>> bb = ta.bollinger_bands(quotes, period=20)
    >>> sma = ta.sma(quotes, period=20)
"""
import importlib

from .quotes import Quotes

__version__ = "0.1.0"
__all__ = ['Quotes']

# Cache for lazy-loaded indicators
_indicator_cache = {}


def __getattr__(name):
    """Lazy loading of indicators.
    
    When an indicator is accessed (e.g., ta.bollinger_bands), this function:
    1. Checks if it's already in the cache
    2. If not, tries to import from indicators/{name}.py
    3. Caches and returns the get_indicator_out function
    
    Args:
        name: Name of the indicator (e.g., 'bollinger_bands', 'sma', 'ema')
        
    Returns:
        The get_indicator_out function from the indicator module
        
    Raises:
        AttributeError: If the indicator module or function is not found
    """
    # Check cache first
    if name in _indicator_cache:
        return _indicator_cache[name]
    
    # Try to import the indicator module
    try:
        module = importlib.import_module(f'.indicators.{name}', __package__)
        func = module.get_indicator_out
        _indicator_cache[name] = func
        return func
    except (ImportError, AttributeError) as e:
        raise AttributeError(
            f"module '{__name__}' has no attribute '{name}'. "
            f"Make sure the indicator '{name}' exists in the indicators directory."
        ) from e


def __dir__():
    """List available attributes including cached indicators."""
    base_attrs = ['Quotes', '__version__']
    return sorted(base_attrs + list(_indicator_cache.keys()))

