from typing import NoReturn

from sqlalchemy.exc import DBAPIError, IntegrityError

from src.application.common.exceptions import RepoError
from src.application.user.exceptions import UserIdAlreadyExistsError
from src.application.user.intefraces.persistence.repo import UserRepo
from src.domain.user import entities
from src.domain.user.exceptions import UsernameAlreadyExistsError
from src.infrastructure.postgres.converters import convert_user_entity_to_db_model
from src.infrastructure.postgres.repositories.base import SQLAlchemyRepo
from src.infrastructure.postgres.utility_wrappers import exception_mapper


class UserRepoImpl(SQLAlchemyRepo, UserRepo):
    @exception_mapper
    async def add_user(self, user: entities.User) -> None:
        db_user = convert_user_entity_to_db_model(user)
        self._session.add(db_user)
        try:
            await self._session.flush((db_user,))
        except IntegrityError as err:
            self._parse_error(err, user)

    def _parse_error(self, err: DBAPIError, user: entities.User) -> NoReturn:
        match err.__cause__.__cause__.constraint_name:  # type: ignore
            case "pk_users":
                raise UserIdAlreadyExistsError(user.id.to_raw()) from err
            case "uq_users_username":
                raise UsernameAlreadyExistsError(str(user.username)) from err
            case _:
                raise RepoError from err
