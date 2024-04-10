from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, Label
import pandas as pd


def plot_chandelier_exit(long_stop, short_stop, closes, buy_signals, sell_signals, show_labels=True):
    x = range(len(closes))

    source = ColumnDataSource(data=dict(
        x=x,
        closes=closes,
        long_stop=long_stop,
        short_stop=short_stop,
        buy_signals=[long_stop[i] if i in buy_signals else None for i in range(len(closes))],
        sell_signals=[short_stop[i] if i in sell_signals else None for i in range(len(closes))]
    ))

    p = figure(title='Chandelier Exit Indicator', x_axis_label='Period', y_axis_label='Price', plot_width=800,
               plot_height=400)

    p.line('x', 'closes', source=source, line_width=2, legend_label='Close Price', color='black')
    p.line('x', 'long_stop', source=source, line_dash='dashed', line_width=2, legend_label='Chandelier Exit Long',
           color='green')
    p.line('x', 'short_stop', source=source, line_dash='dashed', line_width=2, legend_label='Chandelier Exit Short',
           color='red')

    p.circle('x', 'buy_signals', source=source, size=10, color='green', legend_label='Buy Signal')
    p.circle('x', 'sell_signals', source=source, size=10, color='red', legend_label='Sell Signal')

    if show_labels:
        for idx in buy_signals:
            p.add_layout(Label(x=idx, y=long_stop[idx], text='Buy', text_color='green', text_align='center'))
        for idx in sell_signals:
            p.add_layout(Label(x=idx, y=short_stop[idx], text='Sell', text_color='red', text_align='center'))

    p.legend.location = "top_left"
    p.grid.visible = True

    show(p)


def candlestick_chart(highs, lows, opens, closes, dates, title="Candlestick Chart"):
    # Determine color based on price change
    colors = ["green" if close > open_ else "red" for open_, close in zip(opens, closes)]

    # Create a ColumnDataSource
    source = ColumnDataSource(data=dict(
        highs=highs,
        lows=lows,
        opens=opens,
        closes=closes,
        dates=dates,
        colors=colors
    ))

    # Create a new plot with datetime axis type
    p = figure(x_axis_type="datetime", title=title, width=1000, height=500)

    # Draw candlesticks
    p.segment(x0='dates', y0='highs', x1='dates', y1='lows', source=source, line_color="black")
    p.vbar(x='dates', width=0.5, top='opens', bottom='closes', source=source, fill_color='colors', line_color="black")

    # Increase the width of the line representing the high and low
    p.segment(x0='dates', y0='opens', x1='dates', y1='closes', source=source, line_width=2, line_color="black")

    return p


# Example data (highs, lows, opens, closes, dates)
highs = [100, 110, 120, 115, 105]
lows = [90, 100, 110, 105, 95]
opens = [95, 105, 115, 110, 100]
closes = [105, 115, 110, 105, 100]
dates = ['2022-01-01', '2022-01-02', '2022-01-03', '2022-01-04', '2022-01-05']

# Convert dates to datetime objects
dates = pd.to_datetime(dates)

# Create the candlestick chart
candlestick_chart = candlestick_chart(highs, lows, opens, closes, dates)

# Show the plot
show(candlestick_chart)
