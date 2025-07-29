import dspy

DEFAULT_MODEL = "openrouter/google/gemini-2.5-flash-lite"

def configure_llm(model: str = DEFAULT_MODEL) -> None:
    # Configure the language model using OpenRouter
    llm = dspy.LM(model)
    dspy.settings.configure(lm=llm)
