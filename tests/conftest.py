import pytest

from settings.containers import get_container


@pytest.fixture
def container():
    return get_container()


@pytest.fixture(scope="session")
def event_loop():
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()