from opentaf.agents.registry import AgentDefinition, AgentRegistry


def create_agent():
    return AgentDefinition(
        agent_id="OTAF-KYC-001",
        name="KYC Validation Agent",
        purpose="Support customer KYC validation",
        owner="Customer Operations",
        risk_level="high",
        autonomy_level="L2",
        tools=[
            "document_retrieval",
            "kyc_validation",
        ],
    )


def test_agent_can_be_registered():
    registry = AgentRegistry()

    agent = create_agent()
    registry.register(agent)

    result = registry.get("OTAF-KYC-001")

    assert result is not None
    assert result.name == "KYC Validation Agent"


def test_agent_can_be_approved():
    registry = AgentRegistry()

    agent = create_agent()
    registry.register(agent)

    registry.approve("OTAF-KYC-001")

    result = registry.get("OTAF-KYC-001")

    assert result.status == "approved"


def test_duplicate_agent_registration_is_rejected():
    registry = AgentRegistry()

    agent = create_agent()

    registry.register(agent)

    try:
        registry.register(agent)
        assert False
    except ValueError:
        assert True
