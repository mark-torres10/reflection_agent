import json

from prompts import get_defaults


def test_get_defaults_keys():
    defaults = get_defaults()
    assert set(defaults) == {
        "generic_system",
        "guide_system",
        "fewshot_user",
        "fewshot_assistant",
    }


def test_get_defaults_non_empty():
    defaults = get_defaults()
    for value in defaults.values():
        assert value.strip()


def test_fewshot_assistant_valid_json():
    defaults = get_defaults()
    data = json.loads(defaults["fewshot_assistant"])
    assert "reflection" in data
    assert data["reflection"].strip()
