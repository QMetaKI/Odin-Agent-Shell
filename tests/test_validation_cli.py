from odin.cli import validate_all

def test_validate_all_clean():
    assert validate_all() == []
