"""Helpers for converting data between py_ta and stock-indicators formats."""
import pickle
from pathlib import Path

import numpy as np
from py_ta.indicator_result import IndicatorResult

TEST_DATA_DIR = Path(__file__).parent / 'test_data'


def quotes_to_si(quotes):
    """Convert py_ta Quotes object to list of stock-indicators Quote objects.

    Args:
        quotes: py_ta Quotes object with .open, .high, .low, .close,
                .time, .volume attributes (numpy arrays)

    Returns:
        list[Quote]: List of stock-indicators Quote objects
    """
    return _dict_to_si_quotes({
        'time': quotes.time,
        'open': quotes.open,
        'high': quotes.high,
        'low': quotes.low,
        'close': quotes.close,
        'volume': quotes.volume,
    })


def si_results_to_numpy(results, attrs):
    """Convert stock-indicators results to dict of numpy arrays.

    None values are converted to NaN.

    Args:
        results: stock-indicators IndicatorResults (list of result objects)
        attrs: list of attribute names to extract (e.g. ['atr', 'tr', 'atrp'])

    Returns:
        dict[str, np.ndarray]: Attribute names mapped to float64 numpy arrays.
    """
    n = len(results)
    output = {}

    for attr in attrs:
        arr = np.empty(n, dtype=np.float64)
        for i, r in enumerate(results):
            val = getattr(r, attr)
            arr[i] = np.nan if val is None else float(val)
        output[attr] = arr

    return output


def get_si_ref(quotes_filename, si_func_name, *args):
    """Get cached stock-indicators reference values.

    On first call computes indicator via stock-indicators and caches
    the result as a pickle file. Subsequent calls load from cache.

    Args:
        quotes_filename: Name of quotes pickle file (e.g. 'BINANCE_BTC_USDT_1h_2025.pkl')
        si_func_name: Name of stock-indicators function (e.g. 'get_adx')
        *args: Positional arguments to pass to the indicator function

    Returns:
        IndicatorResult: Object with attribute access to numpy arrays
    """
    cache_path = _build_cache_path(quotes_filename, si_func_name, args)

    if cache_path.exists():
        with open(cache_path, 'rb') as f:
            return IndicatorResult(pickle.load(f))

    with open(TEST_DATA_DIR / quotes_filename, 'rb') as f:
        quotes_data = pickle.load(f)

    from stock_indicators import indicators as si

    func = getattr(si, si_func_name)
    si_quotes = _dict_to_si_quotes(quotes_data)
    results = func(si_quotes, *args)
    data_dict = _extract_all_attrs(results)

    with open(cache_path, 'wb') as f:
        pickle.dump(data_dict, f)

    return IndicatorResult(data_dict)


def _build_cache_path(quotes_filename, si_func_name, args):
    quotes_base = quotes_filename.replace('.pkl', '')
    params_suffix = '-' + ','.join(str(a) for a in args) if args else ''
    cache_name = f'si_ref-{si_func_name}-{quotes_base}{params_suffix}.pkl'
    return TEST_DATA_DIR / cache_name


def _dict_to_si_quotes(data_dict):
    from stock_indicators import Quote

    time = data_dict['time']
    open_data = data_dict['open']
    high = data_dict['high']
    low = data_dict['low']
    close = data_dict['close']
    volume = data_dict['volume']

    result = []
    for i in range(len(close)):
        result.append(Quote(
            date=time[i].astype('datetime64[ms]').item(),
            open=float(open_data[i]),
            high=float(high[i]),
            low=float(low[i]),
            close=float(close[i]),
            volume=float(volume[i]),
        ))
    return result


def _extract_all_attrs(results):
    result_class = type(results[0])
    attrs = [
        name for name in dir(result_class)
        if isinstance(getattr(result_class, name, None), property)
        and name != 'date' and not name.startswith('_')
    ]

    n = len(results)
    data_dict = {}
    for attr in attrs:
        arr = np.empty(n, dtype=np.float64)
        for i, r in enumerate(results):
            val = getattr(r, attr)
            arr[i] = np.nan if val is None else float(val)
        data_dict[attr] = arr

    return data_dict
