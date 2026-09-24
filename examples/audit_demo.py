from opentaf.audit.events import AuditEvent, AuditLogger


audit = AuditLogger()


audit.record(
    AuditEvent(
        event_id="EVT-001",
        event_type="POLICY_DECISION",
        agent_id="OTAF-KYC-001",
        user_id="synthetic-user-001",
        tool_id="TOOL-KYC-VALIDATE",
        action="validate_kyc",
        decision="allowed",
        outcome="human_approval_required",
        details={
            "risk_level": "high",
            "autonomy_level": "L2",
        },
    )
)


audit.record(
    AuditEvent(
        event_id="EVT-002",
        event_type="HUMAN_APPROVAL",
        agent_id="OTAF-KYC-001",
        user_id="synthetic-user-001",
        tool_id="TOOL-KYC-VALIDATE",
        action="approve_kyc_validation",
        decision="approved",
        outcome="approved_for_execution",
    )
)


for event in audit.list_events():
    print(
        f"{event.event_id} | "
        f"{event.event_type} | "
        f"{event.agent_id} | "
        f"{event.action} | "
        f"{event.outcome}"
    )
