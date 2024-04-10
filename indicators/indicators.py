import numpy as np


def simple_moving_average(data: list, window_size: int) -> list:
    """
    Calculate Simple Moving Average (SMA) of given data.

    Args:
    - data (list): List of numeric values representing the data.
    - window_size (int): Size of the moving window.

    Returns:
    - List of Simple Moving Average values.
    """
    sma_values = []
    for i in range(len(data) - window_size + 1):
        window = data[i: i + window_size]
        sma = sum(window) / window_size
        sma_values.append(sma)
    return sma_values


def exponential_moving_average(data: list, alpha: float) -> list:
    """
    Calculate Exponential Moving Average (EMA) of given data.

    Args:
    - data (list): List of numeric values representing the data.
    - alpha (float): Smoothing factor (0 < alpha < 1).

    Returns:
    - List of Exponential Moving Average values.
    """
    ema_values = []
    ema_prev = data[0]
    ema_values.append(ema_prev)
    for i in range(1, len(data)):
        ema = alpha * data[i] + (1 - alpha) * ema_prev
        ema_values.append(ema)
        ema_prev = ema
    return ema_values


def relative_strength_index(data: list, window_size: int = 14) -> list:
    """
    Calculate Relative Strength Index (RSI) of given data.

    Args:
    - data (list): List of numeric values representing the data.
    - window_size (int): Size of the RSI window (default is 14).

    Returns:
    - List of Relative Strength Index values.
    """
    delta = [data[i + 1] - data[i] for i in range(len(data) - 1)]
    gain = [d if d > 0 else 0 for d in delta]
    loss = [abs(d) if d < 0 else 0 for d in delta]

    avg_gain = sum(gain[:window_size]) / window_size
    avg_loss = sum(loss[:window_size]) / window_size

    rsi_values = [100 - (100 / (1 + avg_gain / avg_loss))]

    for i in range(window_size, len(data) - 1):
        avg_gain = (avg_gain * (window_size - 1) + gain[i]) / window_size
        avg_loss = (avg_loss * (window_size - 1) + loss[i]) / window_size
        rsi = 100 - (100 / (1 + avg_gain / avg_loss))
        rsi_values.append(rsi)

    return rsi_values


def chandelier_exit(highs, lows, period=1, multiplier=1.85):
    """
    Applicability: Time window 4h and above
    The Chandelier Exit is a volatility-based indicator used primarily in trend-following strategies to set trailing
    stop-loss levels. Calculate Chandelier Exit Long and Chandelier Exit Short.

    Args:
    - highs (list): List of high prices.
    - lows (list): List of low prices.
    - closes (list): List of closing prices.
    - period (int): Lookback period for calculating the ATR (default is 22).
    - multiplier (int): Multiplier for ATR to calculate the Chandelier Exit (default is 3).

    Returns:
    - chandelier_exit_long (list): List of Chandelier Exit Long values.
    - chandelier_exit_short (list): List of Chandelier Exit Short values.
    """

    # Calculate Average True Range (ATR)
    tr_list = [high - low for high, low in zip(highs, lows)]
    atr_list = [
        sum(tr_list[i - period: i]) / period for i in range(period, len(tr_list) + 1)
    ]

    chandelier_exit_long = [
        high - multiplier * atr for high, atr in zip(highs[period - 1:], atr_list)
    ]
    chandelier_exit_short = [
        low + multiplier * atr for low, atr in zip(lows[period - 1:], atr_list)
    ]

    return chandelier_exit_long, chandelier_exit_short


def chandelier_exit_indicator(
        highs: list,
        lows: list,
        closes: list,
        period: int = 1,
        multiplier: float = 1.85,
        use_close: bool = True,
):
    """
    Calculate Chandelier Exit Long and Short levels, along with buy and sell signals.

    Args:
    - highs (list): List of high prices.
    - lows (list): List of low prices.
    - closes (list): List of closing prices.
    - period (int): Lookback period for calculating the ATR (default should be 22  but here is 1).
    - multiplier (float): Multiplier for ATR to calculate the Chandelier Exit (default should be 3.0  but here is 1.85).
    - use_close (bool): Flag to indicate whether to use the close price for extremums (default is True).

    Returns:
    - long_stop (list): List of Chandelier Exit Long values.
    - short_stop (list): List of Chandelier Exit Short values.
    - buy_signal (list): List of indices where buy signals occur.
    - sell_signal (list): List of indices where sell signals occur.
    """
    atr = multiplier * np.mean(np.abs(np.diff(np.column_stack((highs, closes)))))

    long_stop = (
                    np.max(closes[-period:]) if use_close else np.max(highs[-period:])
                ) - atr
    short_stop = (
                     np.min(closes[-period:]) if use_close else np.min(lows[-period:])
                 ) + atr

    # Buy signal: price crosses above Chandelier Exit Long
    buy_signal = [
        i
        for i in range(1, len(closes))
        if closes[i] > long_stop[i - 1] >= closes[i - 1]
    ]

    # Sell signal: price crosses below Chandelier Exit Short
    sell_signal = [
        i
        for i in range(1, len(closes))
        if closes[i] < short_stop[i - 1] <= closes[i - 1]
    ]

    return long_stop, short_stop, buy_signal, sell_signal
