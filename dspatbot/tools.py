import datetime
import dspy

def calculator_func(expression: str) -> str:
    """
    A simple calculator that evaluates a mathematical expression.
    """
    try:
        # A safer eval version
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception as e:
        return f"Error: {e}"

def get_date_func() -> str:
    """
    Returns the current date in ISO format.
    """
    return datetime.date.today().isoformat()

def get_weather_func(location: str) -> str:
    """
    A placeholder function to get weather information for a given location.
    """
    # This would normally call a weather API
    if "texas" in location.lower():
        return "The weather in Texas is sunny with a high of 30°C."
    elif "seattle" in location.lower():
        return "The weather in Seattle is rainy with a high of 20°C."
    else:
        # Default response for other locations
        return f"The weather in {location} is sunny with a high of 25°C."

# Define DSPy tools
calculator = dspy.Tool(calculator_func)
get_date = dspy.Tool(get_date_func)
get_weather = dspy.Tool(get_weather_func)

ALL_TOOLS = [calculator, get_date, get_weather]