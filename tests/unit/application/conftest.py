import pytest

from tests.mocks import EventMediatorMock, UserRepoMock
from tests.mocks.uow import UnitOfWorkMock


@pytest.fixture()
def user_repo() -> UserRepoMock:
    return UserRepoMock()


@pytest.fixture()
def event_mediator() -> EventMediatorMock:
    return EventMediatorMock()


@pytest.fixture()
def uow() -> UnitOfWorkMock:
    return UnitOfWorkMock()
