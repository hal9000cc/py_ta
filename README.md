# py-ta

A simple and efficient technical analysis library for stock market quotes.

## Features

- Simple API for working with OHLCV data
- Efficient calculations using NumPy and Numba
- Support for common technical indicators
- No external data sources required - bring your own data

## Installation

```bash
pip install py-ta
```

Or install from source:

```bash
git clone https://github.com/hal9000cc/py_ta.git
cd py_ta
pip install -e .
```

## Usage

### Creating Quotes

```python
import py_ta as ta
import numpy as np

# Create quotes with OHLC data
open_prices = np.array([100, 102, 101, 103])
high_prices = np.array([105, 106, 104, 107])
low_prices = np.array([99, 101, 100, 102])
close_prices = np.array([102, 103, 101, 105])

quotes = ta.Quotes(open_prices, high_prices, low_prices, close_prices)

# With volume
volume = np.array([1000, 1200, 900, 1500])
quotes = ta.Quotes(open_prices, high_prices, low_prices, close_prices, volume)

# With volume and time
time = np.array(['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04'], 
                dtype='datetime64[ms]')
quotes = ta.Quotes(open_prices, high_prices, low_prices, close_prices, volume, time)

# From pandas DataFrame
import pandas as pd
df = pd.DataFrame({
    'open': open_prices,
    'high': high_prices,
    'low': low_prices,
    'close': close_prices,
    'volume': volume
})
quotes = ta.Quotes(df)
```

### Bollinger Bands

```python
import py_ta as ta

quotes = ta.Quotes(open_data, high_data, low_data, close_data)

# Calculate Bollinger Bands
bb = ta.bollinger_bands(quotes, period=20, deviation=2, ma_type='sma', value='close')

# Access the bands
print(bb.mid_line)   # Middle line (moving average)
print(bb.up_line)    # Upper band
print(bb.down_line)  # Lower band
print(bb.z_score)    # Z-score
```

### Simple Moving Average (SMA)

```python
import py_ta as ta

quotes = ta.Quotes(open_data, high_data, low_data, close_data)

# Calculate SMA
sma = ta.sma(quotes, period=20, value='close')

print(sma.sma)  # SMA values
```

### Exponential Moving Average (EMA)

```python
import py_ta as ta

quotes = ta.Quotes(open_data, high_data, low_data, close_data)

# Calculate EMA
ema = ta.ema(quotes, period=12, value='close')

print(ema.ema)  # EMA values
```

## Available Indicators

- **bollinger_bands** - Bollinger Bands
- **sma** - Simple Moving Average
- **ema** - Exponential Moving Average

More indicators coming soon!

## Requirements

- Python 3.12+
- NumPy
- Numba

## License

MIT License. Copyright (c) 2022 Aleksandr Kuznetsov hal@hal9000.cc

## Related Projects

This library is inspired by [live_trading_indicators](https://github.com/hal9000cc/live_trading_indicators), 
a more feature-rich library that supports live data loading and incremental updates.

