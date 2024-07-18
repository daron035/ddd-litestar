import abc

from src.infrastructure.mediator.interface.entities.request import Request

# from src.application.common.mediator.interface.entities.request import Request


class Event(Request[None], abc.ABC):
    pass
