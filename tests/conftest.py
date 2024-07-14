from injector import Injector
from pytest import fixture

from src.application.common.mediator.base import Mediator
from src.infrastructure.ioc import AppModule
from src.infrastructure.repositories.messages.base import BaseChatRepository


@fixture(scope="function")
def container() -> Injector:
    return Injector(AppModule)


@fixture()
def mediator(container: Injector) -> Mediator:
    return container.get(Mediator)


@fixture()
def chat_repository(container: Injector) -> BaseChatRepository:
    return container.get(BaseChatRepository)
