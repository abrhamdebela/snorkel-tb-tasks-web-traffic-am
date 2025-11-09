import pytest


@pytest.fixture
def basic_obj():
    return type("BasicObj", (), {
        "bhagavad": None,
        "gita": ["True or false:", "This string is impure", "Answer: "],
        "fix me": [0, 2, 2, 3, 4, 5],
        "fixme": [0, 2, 2, 3, 4, 5]
    })()