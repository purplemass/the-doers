import openai


class LLMClient:
    def __init__(self, api_key="your_api_key_here"):
        openai.api_key = api_key

    def decide(self, task):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a task manager deciding worker assignments."},
                {"role": "user", "content": f"What worker should handle the task: {task}?"}
            ]
        )
        return response["choices"][0]["message"]["content"]
