"""Tests for conversation history management."""

from __future__ import annotations

from AI_engineer.conversation import conversation_history, trim_conversation_history


class TestTrimConversationHistory:
    def _reset(self) -> None:
        """Reset conversation_history to just the system prompt."""
        conversation_history.clear()
        conversation_history.append({"role": "system", "content": "system prompt"})

    def test_no_trim_under_threshold(self) -> None:
        self._reset()
        for i in range(10):
            conversation_history.append({"role": "user", "content": f"msg {i}"})

        trim_conversation_history()
        # 1 system + 10 user = 11, under threshold of 20
        assert len(conversation_history) == 11

    def test_trims_over_threshold(self) -> None:
        self._reset()
        for i in range(25):
            conversation_history.append({"role": "user", "content": f"msg {i}"})

        trim_conversation_history()
        # Should keep system prompt + last 15
        assert len(conversation_history) == 16
        assert conversation_history[0]["role"] == "system"

    def test_preserves_system_prompt(self) -> None:
        self._reset()
        for i in range(30):
            conversation_history.append({"role": "user", "content": f"msg {i}"})

        trim_conversation_history()
        system_msgs = [m for m in conversation_history if m["role"] == "system"]
        assert len(system_msgs) == 1
        assert system_msgs[0]["content"] == "system prompt"

    def test_keeps_most_recent_messages(self) -> None:
        self._reset()
        for i in range(25):
            conversation_history.append({"role": "user", "content": f"msg {i}"})

        trim_conversation_history()
        non_system = [m for m in conversation_history if m["role"] != "system"]
        assert non_system[-1]["content"] == "msg 24"
        assert non_system[0]["content"] == "msg 10"
