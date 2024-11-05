"""Промпты для OpenAI."""

# Промпт для суммирования текста
SUMMARY_PROMPT = "Summarize the following text:"

# Промпт для ответа на вопрос
QUESTION_PROMPT = """Context: {context}

User question: {question}

Please answer the question based on the provided context.
If the answer cannot be found in the context, state this and provide a general answer.
"""
