from collections.abc import Iterable
from typing import NoReturn
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import DBAPIError, IntegrityError

from src.application.common.exceptions import RepoError
from src.application.user import dto
from src.application.user.exceptions import UserIdAlreadyExistsError, UserIdNotExistError
from src.application.user.interfaces.persistence import UserReader, UserRepo
from src.domain.user import entities
from src.domain.user.exceptions import UsernameAlreadyExistsError
from src.domain.user.value_objects import Username
from src.infrastructure.postgres.converters import (
    convert_db_model_to_user_dto,
    convert_user_entity_to_db_model,
)
from src.infrastructure.postgres.models import User
from src.infrastructure.postgres.repositories.base import SQLAlchemyRepo
from src.infrastructure.postgres.utility_wrappers import exception_mapper


class UserReaderImpl(SQLAlchemyRepo, UserReader):
    @exception_mapper
    async def get_user_by_id(self, user_id: UUID) -> dto.UserDTOs:
        user: User | None = await self._session.get(User, user_id)
        if user is None:
            raise UserIdNotExistError(user_id)

        return convert_db_model_to_user_dto(user)


class UserRepoImpl(SQLAlchemyRepo, UserRepo):
    @exception_mapper
    async def add_user(self, user: entities.User) -> None:
        db_user = convert_user_entity_to_db_model(user)
        self._session.add(db_user)
        try:
            await self._session.flush((db_user,))
        except IntegrityError as err:
            self._parse_error(err, user)

    @exception_mapper
    async def get_existing_usernames(self) -> set[Username]:
        stmt = select(User.username).where(User.username.is_not(None))
        result: Iterable[str] = await self._session.scalars(stmt)
        existing_usernames = {Username(username) for username in result}
        return existing_usernames

    def _parse_error(self, err: DBAPIError, user: entities.User) -> NoReturn:
        match err.__cause__.__cause__.constraint_name:  # type: ignore
            case "pk_users":
                raise UserIdAlreadyExistsError(user.id.to_raw()) from err
            case "uq_users_username":
                raise UsernameAlreadyExistsError(str(user.username)) from err
            case _:
                raise RepoError from err
