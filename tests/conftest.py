from injector import Injector
from pytest import fixture

from src.application.messages.interfaces.percistence.chat import ChatRepo

# from src.infrastructure.ioc import AppModule, RepositoryModule
from src.infrastructure.mediator.mediator import MediatorImpl
from tests.fixtures import init_container


@fixture(scope="function")
def container() -> Injector:
    return init_container()
    # return Injector([AppModule])


@fixture()
def mediator(container: Injector) -> MediatorImpl:
    return container.get(MediatorImpl)


@fixture()
def chat_repository(container: Injector) -> ChatRepo:
    return container.get(ChatRepo)
