from opentaf.tools.executor import InMemoryToolExecutor


class SyntheticTool:
    def execute(self, value):
        return f"processed:{value}"


def test_tool_can_be_registered_and_executed():
    executor = InMemoryToolExecutor()

    executor.register(
        "TOOL-SYNTHETIC",
        SyntheticTool(),
    )

    result = executor.execute(
        tool_id="TOOL-SYNTHETIC",
        action="execute",
        parameters={
            "value": "test",
        },
    )

    assert result == "processed:test"


def test_unknown_tool_is_rejected():
    executor = InMemoryToolExecutor()

    try:
        executor.execute(
            tool_id="TOOL-UNKNOWN",
            action="execute",
            parameters={},
        )
        assert False
    except ValueError:
        assert True


def test_unknown_action_is_rejected():
    executor = InMemoryToolExecutor()

    executor.register(
        "TOOL-SYNTHETIC",
        SyntheticTool(),
    )

    try:
        executor.execute(
            tool_id="TOOL-SYNTHETIC",
            action="unknown",
            parameters={},
        )
        assert False
    except ValueError:
        assert True
