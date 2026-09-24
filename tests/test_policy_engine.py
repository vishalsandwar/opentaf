from opentaf.agents.registry import AgentDefinition, AgentRegistry
from opentaf.governance.policy import PolicyEngine
from opentaf.tools.registry import ToolDefinition, ToolRegistry


def create_agent(registry):
    agent = AgentDefinition(
        agent_id="OTAF-KYC-001",
        name="KYC Validation Agent",
        purpose="Support customer KYC validation",
        owner="Customer Operations",
        risk_level="high",
        autonomy_level="L2",
    )

    registry.register(agent)

    return agent


def create_tool(registry, allowed_agents):
    tool = ToolDefinition(
        tool_id="TOOL-KYC-VALIDATE",
        name="KYC Validation Tool",
        purpose="Validate synthetic customer KYC information",
        risk_level="high",
        allowed_agents=allowed_agents,
        requires_human_approval=True,
    )

    registry.register(tool)

    return tool


def test_approved_agent_can_access_authorised_tool():
    agent_registry = AgentRegistry()
    tool_registry = ToolRegistry()

    agent = create_agent(agent_registry)

    agent_registry.approve(agent.agent_id)

    tool = create_tool(
        tool_registry,
        ["OTAF-KYC-001"],
    )

    engine = PolicyEngine()

    decision = engine.evaluate(agent, tool)

    assert decision.allowed is True
    assert decision.requires_human_approval is True


def test_unauthorised_agent_is_rejected():
    agent_registry = AgentRegistry()
    tool_registry = ToolRegistry()

    agent = create_agent(agent_registry)

    agent_registry.approve(agent.agent_id)

    tool = create_tool(
        tool_registry,
        ["OTAF-DOCUMENT-001"],
    )

    engine = PolicyEngine()

    decision = engine.evaluate(agent, tool)

    assert decision.allowed is False
    assert (
        decision.reason
        == "Agent is not authorised to use this tool."
    )


def test_unapproved_agent_is_rejected():
    agent_registry = AgentRegistry()
    tool_registry = ToolRegistry()

    agent = create_agent(agent_registry)

    tool = create_tool(
        tool_registry,
        ["OTAF-KYC-001"],
    )

    engine = PolicyEngine()

    decision = engine.evaluate(agent, tool)

    assert decision.allowed is False
    assert (
        decision.reason
        == "Agent is not approved for execution."
    )


def test_inactive_tool_is_rejected():
    agent_registry = AgentRegistry()
    tool_registry = ToolRegistry()

    agent = create_agent(agent_registry)

    agent_registry.approve(agent.agent_id)

    tool = create_tool(
        tool_registry,
        ["OTAF-KYC-001"],
    )

    tool.status = "inactive"

    engine = PolicyEngine()

    decision = engine.evaluate(agent, tool)

    assert decision.allowed is False
    assert decision.reason == "Tool is not active."
