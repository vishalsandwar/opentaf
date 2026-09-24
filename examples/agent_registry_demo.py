from opentaf.agents.registry import AgentDefinition, AgentRegistry


registry = AgentRegistry()


kyc_agent = AgentDefinition(
    agent_id="OTAF-KYC-001",
    name="KYC Validation Agent",
    purpose="Support customer KYC validation",
    owner="Customer Operations",
    risk_level="high",
    autonomy_level="L2",
    tools=[
        "document_retrieval",
        "kyc_validation"
    ],
)


registry.register(kyc_agent)

registry.approve("OTAF-KYC-001")


for agent in registry.list_agents():
    print(
        f"{agent.agent_id} | "
        f"{agent.name} | "
        f"Risk: {agent.risk_level} | "
        f"Autonomy: {agent.autonomy_level} | "
        f"Status: {agent.status}"
    )
