

from __future__ import annotations

import ollama

import config


class LLMService:

    def __init__(self):

        self.model = config.MODEL_NAME
        self.temperature = 0.3
        self.max_tokens = 512

    # ----------------------------------------------------

    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Generate a complete response.
        """

        try:

            response = ollama.chat(

                model=self.model,

                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],

                options={
                    "temperature": self.temperature,
                    "num_predict": self.max_tokens,
                },

            )

            return response["message"]["content"]

        except Exception as e:

            return f"LLM Error : {str(e)}"

    # ----------------------------------------------------

    def stream(
        self,
        prompt: str,
    ):
        """
        Stream response tokens.
        """

        try:

            stream = ollama.chat(

                model=self.model,

                stream=True,

                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],

                options={
                    "temperature": self.temperature,
                    "num_predict": self.max_tokens,
                },

            )

            for chunk in stream:

                if "message" in chunk:

                    yield chunk["message"]["content"]

        except Exception as e:

            yield f"\nLLM Error : {str(e)}"

    # ----------------------------------------------------

    def health_check(self):
        """
        Check whether the configured model is available.
        """

        try:

            models = ollama.list()

            available = []

            for model in models.get("models", []):

                name = model.get("model") or model.get("name")

                if name:
                    available.append(name)

            return {
                "status": self.model in available,
                "model": self.model,
                "available_models": available,
            }

        except Exception as e:

            return {
                "status": False,
                "error": str(e),
            }