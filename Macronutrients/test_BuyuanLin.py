# content of conftest.py
import pytest

dataset = 'Desktop/Food101'

def pytest_collect_file(parent, path):
    if path.ext == ".yaml" and path.basename.startswith("test"):
        return YamlFile.from_parent(parent, fspath=path)


class YamlFile(pytest.File):
    def collect(self):
        # We need a yaml parser, e.g. PyYAML.
        import yaml

        raw = yaml.safe_load(self.fspath.open())
        for name, spec in sorted(raw.items()):
            yield YamlItem.from_parent(self, name=name, spec=spec)


class YamlItem(pytest.Item):
    def __init__(self, name, parent, spec):
        super().__init__(name, parent)
        self.spec = spec

    def runtest(self):
        for name, value in sorted(self.spec.items()):
            # Some custom test execution (dumb example follows).
            if name != value:
                raise YamlException(self, name, value)

    def repr_failure(self, excinfo):
        """Called when self.runtest() raises an exception."""
        if isinstance(excinfo.value, YamlException):
            return "\n".join(
                [
                    "usecase execution failed",
                    "   spec failed: {1!r}: {2!r}".format(*excinfo.value.args),
                    "   no further details known at this point.",
                ]
            )

    def reportinfo(self):
        return self.fspath, 0, "usecase: {}".format(self.name)

    path_large_number_fixture = 'large_num_fixture.txt'


def test_add_ten():
    """ Tests the add_ten function """
    assert 15 == add_ten(5)


def test_add_ten_str_int():
    """ Tests the add_ten function for string input """
    assert add_ten('5') == '15'


def test_add_ten_none():
    """ Tests that add_ten throws a ValueError when None input given """
    assert add_ten(None) is None


def test_large_number():

    with open(path_large_number_fixture, 'r') as fh:
        expected = int(fh.readline())

    assert add_ten(90) == expected

class YamlException(Exception):
    """Custom exception for error reporting."""
