from collections import defaultdict
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from typing import Any, Generic, TypeVar

from src.application.common.command import Command, CommandHandler, CRes_co
from src.application.common.event import EventHandler
from src.application.common.mediator.command import CommandMediator
from src.application.common.mediator.event import EventMediator
from src.application.common.mediator.exceptions import CommandHandlersNotRegisteredError
from src.application.common.mediator.query import QueryMediator
from src.application.common.query import Q_contra, QRes_co, Query, QueryHandler
from src.domain.common.events.event import Event


QRes = TypeVar("QRes", bound=Any)


@dataclass(eq=False)
class Mediator(CommandMediator, QueryMediator, EventMediator, Generic[CRes_co, QRes]):
    commands_map: dict[Command, list[CommandHandler]] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )
    queries_map: dict[Query, QueryHandler] = field(
        default_factory=dict,
        kw_only=True,
    )

    def register_command(
        self,
        command: Command,
        command_handlers: Iterable[CommandHandler],
    ) -> None:
        self.commands_map[command].extend(command_handlers)

    def register_query(
        self,
        query: Q_contra,
        query_handler: QueryHandler[Q_contra, QRes_co],
    ) -> None:
        self.queries_map[query] = query_handler

    def register_event(self, event: Any, event_handlers: Iterable[EventHandler]) -> None:
        pass

    async def send(self, command: Command) -> Iterable[CRes_co]:
        command_type = type(command)
        handlers: list | None = self.commands_map.get(command_type)

        if not handlers:
            raise CommandHandlersNotRegisteredError(command_type)

        return [await handler.handle(command) for handler in handlers]

    async def query(self, query: Query) -> QRes:
        return await self.queries_map[type(query)].handle(query=query)

    async def publish(self, events: Event | Sequence[Event]) -> None:
        pass
