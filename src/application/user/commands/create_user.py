import logging

from dataclasses import dataclass
from uuid import UUID

from src.application.common.interfaces.uow import UnitOfWork
from src.application.user.intefraces.persistence.repo import UserRepo
from src.domain.user.entities import User
from src.domain.user.value_objects import FullName, UserId, Username
from src.infrastructure.mediator.interface.entities.command import Command
from src.infrastructure.mediator.interface.handlers.command import CommandHandler
from src.infrastructure.mediator.interface.mediator import EventMediator
from src.infrastructure.postgres.utility_wrappers import close_session


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class CreateUser(Command[UUID]):
    username: str
    first_name: str
    last_name: str
    middle_name: str | None


@dataclass(frozen=True)
class CreateUserHandler(CommandHandler[CreateUser, UUID]):
    user_repo: UserRepo
    uow: UnitOfWork
    mediator: EventMediator

    @close_session
    async def __call__(self, command: CreateUser) -> UUID:
        user_id = UserId()
        username = Username(command.username)
        full_name = FullName(command.first_name, command.last_name, command.middle_name)

        # TODO: existing_usernames = await self._user_repo.get_existing_usernames()
        existing_usernames = {Username("ioqwrue")}
        user = User.create(user_id, username, full_name, existing_usernames)
        await self.user_repo.add_user(user)
        await self.mediator.publish(user.pull_events())
        await self.uow.commit()

        logger.info("User created", extra={"user": user})

        return user_id.to_raw()
