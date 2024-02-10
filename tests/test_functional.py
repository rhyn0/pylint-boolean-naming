# Standard Library
from pathlib import Path
import sys
from typing import List
from typing import Union

# External Party
from pylint.testutils import UPDATE_FILE
from pylint.testutils import UPDATE_OPTION
from pylint.testutils import FunctionalTestFile
from pylint.testutils import LintModuleTest
from pylint.testutils.functional import LintModuleOutputUpdate
import pytest

TEST_DIR = Path(__file__).parent


sys.path += [
    str(p.absolute()) for p in (TEST_DIR, TEST_DIR / "../../", TEST_DIR / "input")
]


# Credit to pylint-django
# https://github.com/pylint-dev/pylint-django
class PylintBooleanModuleTest(LintModuleTest):
    """Only used so that we can load this checker into the linter!"""

    def __init__(self, test_file: FunctionalTestFile):
        """Force loading of our checker."""
        super().__init__(test_file)
        self._linter.load_plugin_modules(["pylint_boolean_naming"])
        self._linter.load_plugin_configuration()


class PylintBooleanOutputUpdate(LintModuleOutputUpdate):
    """Only used so that we can load this checker into the linter!"""

    def __init__(self, test_file: FunctionalTestFile):
        """Force loading of our checker."""
        super().__init__(test_file)
        self._linter.load_plugin_modules(["pylint_boolean_naming"])
        self._linter.load_plugin_configuration()


def get_tests(input_dir: str = "input", sort: bool = False) -> List[FunctionalTestFile]:
    """Crawl subdirectory from test directory to find test files."""

    def _file_name(test: FunctionalTestFile):
        return test.base

    test_subdir = TEST_DIR / input_dir

    suite = []
    for fname in test_subdir.iterdir():
        if fname.name != "__init__.py" and fname.name.endswith(".py"):
            suite.append(
                FunctionalTestFile(str(test_subdir.absolute()), str(fname.absolute()))
            )

    # when testing the migrations plugin we need to sort by input file name
    # because the plugin reports the errors in close() which appends them to the
    # report for the last file in the list
    if sort:
        suite.sort(key=_file_name)

    return suite


TESTS = get_tests()
TESTS_NAMES = [t.base for t in TESTS]


@pytest.mark.parametrize("test_file", TESTS, ids=TESTS_NAMES)
def test_everything(test_file: FunctionalTestFile):
    """Run tests collected from the input directory.

    Uses the above defined classes to force the loading of our checker.
    """
    # copied from pylint.tests.test_functional.test_functional
    lint_test: Union[PylintBooleanModuleTest, PylintBooleanOutputUpdate]
    lint_test = (
        PylintBooleanOutputUpdate(test_file)
        if UPDATE_FILE.exists()
        else PylintBooleanModuleTest(test_file)
    )
    lint_test.setUp()
    lint_test.runTest()


if __name__ == "__main__":
    # Helper function to update the expected output of the tests
    if UPDATE_OPTION in sys.argv:
        UPDATE_FILE.touch()
        sys.argv.remove(UPDATE_OPTION)
    try:
        pytest.main(sys.argv)
    finally:
        if UPDATE_FILE.exists():
            UPDATE_FILE.unlink()
