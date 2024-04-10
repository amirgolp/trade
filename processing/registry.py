from pydantic import BaseModel, field_validator
from typing import Callable, Dict, Any, Optional
from indicators import (
    exponential_moving_average,
    simple_moving_average,
    relative_strength_index,
)


class TradingStrategyInput(BaseModel):
    trade_type: str
    strategy: str
    indicator: str

    @field_validator("trade_type")
    def validate_trade_type(cls, v):
        if v not in {"buy", "sell"}:
            raise ValueError("Trade type must be 'buy' or 'sell'")
        return v

    @field_validator("strategy")
    def validate_strategy(cls, v):
        if v not in {"moving_average", "rsi"}:
            raise ValueError("Strategy must be 'moving_average' or 'rsi'")
        return v

    @field_validator("indicator")
    def validate_indicator(cls, v, values):
        if values["strategy"] == "moving_average" and v not in {
            "simple",
            "exponential",
        }:
            raise ValueError(
                "Indicator for moving_average strategy must be 'simple' or 'exponential'"
            )
        return v


class TradingStrategy:
    def __init__(self, trade_type: str, strategy: str, indicator: str):
        self.trade_type = trade_type
        self.strategy = strategy
        self.indicator = indicator

    def execute_trade(self, data: list):
        # Your trade execution logic here
        print(
            f"Executing trade: {self.trade_type}, Strategy: {self.strategy}, Indicator: {self.indicator}"
        )


class Indicator(BaseModel):
    name: str
    function: Callable


class IndicatorRegistry:
    def __init__(self):
        self.registry: Dict[str, Indicator] = {}

    def register_indicator(self, name: str, indicator_function: Callable):
        if name not in self.registry:
            self.registry[name] = Indicator(name=name, function=indicator_function)
        else:
            print(f"Indicator '{name}' is already registered.")

    def get_indicator(self, name: str) -> Callable[..., Any] | None:
        if name in self.registry:
            return self.registry[name].function
        else:
            print(f"Indicator '{name}' is not registered.")
            return None


class TradingStrategyRegistry(BaseModel):
    registry: Dict[str, Indicator]

    @field_validator("registry")
    def check_registry(cls, v):
        if not isinstance(v, dict):
            raise ValueError("Registry must be a dictionary.")
        for name, indicator in v.items():
            if not isinstance(indicator, Indicator):
                raise ValueError(
                    f"Invalid entry in registry: {name}. Must be an Indicator instance."
                )
        return v

    def register_indicator(self, name: str, indicator_function: Callable):
        if name in self.registry:
            print(f"Indicator '{name}' is already registered.")
        else:
            self.registry[name] = Indicator(name=name, function=indicator_function)

    def get_indicator(self, name: str) -> Optional[Callable]:
        if name in self.registry:
            return self.registry[name].function
        else:
            print(f"Indicator '{name}' is not registered.")
            return None


indicator_registry = IndicatorRegistry()

# Register indicators
indicator_registry.register_indicator("SMA", simple_moving_average)
indicator_registry.register_indicator("EMA", exponential_moving_average)
indicator_registry.register_indicator("RSI", relative_strength_index)

# Example of getting an indicator function
sma_function = indicator_registry.get_indicator("SMA")
if sma_function:
    # Now you can use the obtained function to calculate SMA
    data = [...]  # Your data here
    sma_result = sma_function(data)
    print("Simple Moving Average:", sma_result)

trade_type = input("Enter trade type (buy/sell): ")
strategy = input("Enter trading strategy (moving_average/rsi): ")
indicator = input(
    "Enter indicator type (simple/exponential for moving average, none for RSI): "
)

# Create trading strategy object
my_strategy = TradingStrategy(trade_type, strategy, indicator)

# Simulated data (replace with actual data from forex or commodity market)
data = [...]  # Your data here

# Execute the trade
my_strategy.execute_trade(data)
