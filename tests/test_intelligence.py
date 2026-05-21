from unittest.mock import MagicMock, patch

import pytest
from langchain_core.messages import AIMessage

from intelligence import (
    GenericRunError,
    GuideOutput,
    GuideRunError,
    run_generic,
    run_guide,
)
from prompts import get_defaults


@pytest.fixture
def prompts():
    return get_defaults()


def test_run_generic_returns_content(prompts):
    mock_chain = MagicMock()
    mock_chain.invoke.return_value = AIMessage(content="Try a short walk after work.")

    with patch("intelligence._build_generic_chain", return_value=mock_chain):
        out = run_generic("I am tired.", prompts)

    assert out == "Try a short walk after work."
    mock_chain.invoke.assert_called_once_with({"user_text": "I am tired."})


def test_run_guide_returns_guide_output(prompts):
    expected = GuideOutput(
        reflection="You sound worn down and still pushing.",
        follow_up_question="What would rest look like for five minutes?",
    )
    mock_chain = MagicMock()
    mock_chain.invoke.return_value = expected

    with patch("intelligence._build_guide_chain", return_value=mock_chain):
        out = run_guide("I am tired.", prompts)

    assert out.reflection == expected.reflection
    assert out.follow_up_question == expected.follow_up_question


def test_run_generic_raises_on_failure(prompts):
    mock_chain = MagicMock()
    mock_chain.invoke.side_effect = RuntimeError("API down")

    with patch("intelligence._build_generic_chain", return_value=mock_chain):
        with pytest.raises(GenericRunError):
            run_generic("I am tired.", prompts)


def test_run_guide_raises_on_failure(prompts):
    mock_chain = MagicMock()
    mock_chain.invoke.side_effect = RuntimeError("parse failed")

    with patch("intelligence._build_guide_chain", return_value=mock_chain):
        with pytest.raises(GuideRunError):
            run_guide("I am tired.", prompts)
