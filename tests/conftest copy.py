from injector import Injector
from pytest import fixture

from src.application.messages.interfaces.percistence.chat import ChatRepo
from src.infrastructure.ioc import AppModule, RepositoryModule
from src.infrastructure.mediator.mediator import MediatorImpl


@fixture(scope="function")
def container() -> Injector:
    return Injector([AppModule, RepositoryModule])


@fixture()
def mediator(container: Injector) -> MediatorImpl:
    return container.get(MediatorImpl)


@fixture()
def chat_repository(container: Injector) -> ChatRepo:
    return container.get(ChatRepo)
