"""
OpenTAF Tool Executor

Provides a provider-independent execution interface for
governed enterprise tools.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict


class ToolExecutor(ABC):
    """Abstract interface for enterprise tool execution."""

    @abstractmethod
    def execute(
        self,
        tool_id: str,
        action: str,
        parameters: Dict[str, Any],
    ) -> Any:
        """Execute a registered enterprise tool."""


class InMemoryToolExecutor(ToolExecutor):
    """Tool executor for the OpenTAF reference implementation."""

    def __init__(self) -> None:
        self._tools: Dict[str, Any] = {}

    def register(
        self,
        tool_id: str,
        tool: Any,
    ) -> None:
        """Register an executable tool."""

        if tool_id in self._tools:
            raise ValueError(
                f"Tool already registered: {tool_id}"
            )

        self._tools[tool_id] = tool

    def execute(
        self,
        tool_id: str,
        action: str,
        parameters: Dict[str, Any],
    ) -> Any:
        """Execute a registered tool action."""

        tool = self._tools.get(tool_id)

        if tool is None:
            raise ValueError(
                f"Executable tool not found: {tool_id}"
            )

        method = getattr(tool, action, None)

        if method is None:
            raise ValueError(
                f"Tool action not found: {action}"
            )

        return method(**parameters)
