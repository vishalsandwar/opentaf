
from opentaf.agents.registry import AgentDefinition, AgentRegistry
from opentaf.governance.policy import PolicyEngine
from opentaf.tools.registry import ToolDefinition, ToolRegistry


# -----------------------------
# Agent Registry
# -----------------------------

agent_registry = AgentRegistry()

kyc_agent = AgentDefinition(
    agent_id="OTAF-KYC-001",
    name="KYC Validation Agent",
    purpose="Support customer KYC validation",
    owner="Customer Operations",
    risk_level="high",
    autonomy_level="L2",
)

agent_registry.register(kyc_agent)
agent_registry.approve("OTAF-KYC-001")


# -----------------------------
# Tool Registry
# -----------------------------

tool_registry = ToolRegistry()

kyc_tool = ToolDefinition(
    tool_id="TOOL-KYC-VALIDATE",
    name="KYC Validation Tool",
    purpose="Validate synthetic customer KYC information",
    risk_level="high",
    allowed_agents=["OTAF-KYC-001"],
    requires_human_approval=True,
)

tool_registry.register(kyc_tool)


# -----------------------------
# Policy Evaluation
# -----------------------------

policy_engine = PolicyEngine()

agent = agent_registry.get("OTAF-KYC-001")
tool = tool_registry.get("TOOL-KYC-VALIDATE")

decision = policy_engine.evaluate(agent, tool)


print("Policy Decision")
print("----------------")
print(f"Allowed: {decision.allowed}")
print(f"Reason: {decision.reason}")
print(
    f"Human Approval Required: "
    f"{decision.requires_human_approval}"
)
