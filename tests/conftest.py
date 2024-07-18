from injector import Injector
from pytest import fixture

from src.infrastructure.ioc import AppModule
from src.infrastructure.mediator.mediator import MediatorImpl
from src.infrastructure.repositories.messages.base import BaseChatRepository


@fixture(scope="function")
def container() -> Injector:
    return Injector(AppModule)


@fixture()
def mediator(container: Injector) -> MediatorImpl:
    return container.get(MediatorImpl)


@fixture()
def chat_repository(container: Injector) -> BaseChatRepository:
    return container.get(BaseChatRepository)
