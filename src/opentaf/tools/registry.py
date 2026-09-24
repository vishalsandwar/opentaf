"""
OpenTAF Tool Registry

Defines the enterprise capabilities that agents are permitted
to invoke.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class ToolDefinition:
    """Definition of an OpenTAF enterprise tool."""

    tool_id: str
    name: str
    purpose: str
    risk_level: str
    allowed_agents: List[str] = field(default_factory=list)
    requires_human_approval: bool = False
    status: str = "active"


class ToolRegistry:
    """Registry for managing governed enterprise tools."""

    def __init__(self) -> None:
        self._tools: Dict[str, ToolDefinition] = {}

    def register(self, tool: ToolDefinition) -> None:
        """Register a new enterprise tool."""

        if tool.tool_id in self._tools:
            raise ValueError(
                f"Tool already registered: {tool.tool_id}"
            )

        self._tools[tool.tool_id] = tool

    def get(self, tool_id: str) -> Optional[ToolDefinition]:
        """Retrieve a tool by ID."""

        return self._tools.get(tool_id)

    def list_tools(self) -> List[ToolDefinition]:
        """Return all registered tools."""

        return list(self._tools.values())
