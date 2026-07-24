"""
core/orchestrator.py

Central AI Orchestrator
"""

import re

from core.guardrails import GuardRails
from core.rate_limiter import RateLimiter
from core.prompt_builder import PromptBuilder

from services.llm_service import LLMService
from services.rag_service import RAGService
from services.chat_history import ChatHistory

from tools.tool_registry import ToolRegistry


class AIOrchestrator:

    def __init__(self):

        self.guardrails = GuardRails()
        self.rate_limiter = RateLimiter()
        self.prompt_builder = PromptBuilder()

        self.llm = LLMService()
        self.rag = RAGService()

        self.history = ChatHistory()

        self.tools = ToolRegistry()

    # -----------------------------------------------------

    def _detect_tool(self, prompt: str):

        text = prompt.lower().strip()

        # Calculator

        if re.fullmatch(r"[0-9\+\-\*/\(\)\.\s%]+", text):
            return "calculator"

        if any(word in text for word in [
            "sqrt",
            "sin",
            "cos",
            "tan",
            "factorial",
            "log",
            "calculate",
        ]):
            return "calculator"

        # Summary

        if text.startswith("summarize"):
            return "summary"

        if text.startswith("summary"):
            return "summary"

        # Statistics

        if text.startswith("statistics"):
            return "statistics"

        if text.startswith("mean"):
            return "statistics"

        return None

    # -----------------------------------------------------

    def chat(
        self,
        session_id,
        user_prompt,
    ):

        # Rate Limiting

        if not self.rate_limiter.allow(session_id):
            return "Rate limit exceeded."

        # Guardrails

        if not self.guardrails.validate(user_prompt):
            return "Prompt rejected."

        # Save User Message

        self.history.append(
            session_id,
            "user",
            user_prompt,
        )

        # --------------------------
        # Tool Detection
        # --------------------------

        tool = self._detect_tool(user_prompt)

        if tool == "calculator":

            expression = (
                user_prompt
                .replace("calculate", "")
                .strip()
            )

            response = self.tools.execute(
                "calculator",
                expression,
            )

        elif tool == "summary":

            text = (
                user_prompt
                .replace("summarize", "")
                .replace("summary", "")
                .strip()
            )

            response = self.tools.execute(
                "summary",
                text,
            )

        else:

            history = self.history.load(session_id)

            context = self.rag.retrieve(user_prompt)

            prompt = self.prompt_builder.build(
                history,
                context,
                user_prompt,
            )

            response = self.llm.generate(prompt)

        self.history.append(
            session_id,
            "assistant",
            str(response),
        )

        return str(response)

    # -----------------------------------------------------

    def available_tools(self):
        return self.tools.list_tools()