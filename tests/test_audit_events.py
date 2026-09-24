from opentaf.audit.events import (
    AuditEvent,
    AuditLogger,
    InMemoryAuditRepository,
)


def create_audit_logger():
    repository = InMemoryAuditRepository()
    return AuditLogger(repository)


def test_audit_event_can_be_recorded():
    audit = create_audit_logger()

    event = AuditEvent(
        event_id="EVT-001",
        event_type="POLICY_DECISION",
        agent_id="OTAF-KYC-001",
        decision="allowed",
    )

    audit.record(event)

    events = audit.list_events()

    assert len(events) == 1
    assert events[0].event_id == "EVT-001"


def test_events_can_be_filtered_by_agent():
    audit = create_audit_logger()

    audit.record(
        AuditEvent(
            event_id="EVT-001",
            event_type="POLICY_DECISION",
            agent_id="OTAF-KYC-001",
        )
    )

    audit.record(
        AuditEvent(
            event_id="EVT-002",
            event_type="POLICY_DECISION",
            agent_id="OTAF-RISK-001",
        )
    )

    events = audit.find_by_agent("OTAF-KYC-001")

    assert len(events) == 1
    assert events[0].agent_id == "OTAF-KYC-001"


def test_events_can_be_filtered_by_type():
    audit = create_audit_logger()

    audit.record(
        AuditEvent(
            event_id="EVT-001",
            event_type="POLICY_DECISION",
            agent_id="OTAF-KYC-001",
        )
    )

    audit.record(
        AuditEvent(
            event_id="EVT-002",
            event_type="HUMAN_APPROVAL",
            agent_id="OTAF-KYC-001",
        )
    )

    events = audit.find_by_event_type("HUMAN_APPROVAL")

    assert len(events) == 1
    assert events[0].event_type == "HUMAN_APPROVAL"
