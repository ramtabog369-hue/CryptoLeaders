# Временная заглушка вместо ChatOpenAI
class FakeLLM:
    def invoke(self, prompt):
        return "SELECT count() FROM crypto.daily_candles"
    def bind(self, **kwargs):
        return self

llm = FakeLLM()