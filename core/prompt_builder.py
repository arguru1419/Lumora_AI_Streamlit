

class PromptBuilder:

    def __init__(self):

        self.system_prompt = """
You are Lumora AI, a professional AI assistant.

Rules:
1. Answer accurately and concisely.
2. Use the provided context whenever relevant.
3. If the context does not contain the answer, say you don't know instead of making up facts.
4. Be polite, professional, and helpful.
5. Format long responses with headings and bullet points when appropriate.
""".strip()

    def _format_history(self, history):
        """
        Convert chat history into a readable conversation.
        """

        if not history:
            return ""

        lines = []

        for message in history:
            role = message.get("role", "user").capitalize()
            text = message.get("message", "").strip()

            if text:
                lines.append(f"{role}: {text}")

        return "\n".join(lines)

    def build(
        self,
        history,
        context,
        question,
    ):
        """
        Construct the final prompt for the LLM.
        """

        conversation = self._format_history(history)

        prompt = f"""
================ SYSTEM ================

{self.system_prompt}

================ CONTEXT ================

{context}

================ CHAT HISTORY ================

{conversation}

================ USER QUESTION ================

{question}

================ ASSISTANT ================
"""

        return prompt.strip()