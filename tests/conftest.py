import pytest

def pytest_addoption(parser):
    """
    Custom command-line options for the pytest command.
    """
    parser.addoption(
        "--local",
        action="store_true",
        help="Run tests that require local resources and environment variables"
    )

def pytest_configure(config):
    """
    Register custom markers for the pytest command.
    """
    config.addinivalue_line("markers", "local: Mark test as local resource dependent")


def pytest_collection_modifyitems(config, items):
    """
    Skip tests specific markers.
    """

    # Skip local tests if not run with --local option
    if config.getoption("--local"):
        # --local given in cli: do not skip local tests
        return
    skip_local = pytest.mark.skip(
        reason="Need --local option to run local resource dependent tests"
    )
    for item in items:
        if "local" in item.keywords:
            item.add_marker(skip_local)
