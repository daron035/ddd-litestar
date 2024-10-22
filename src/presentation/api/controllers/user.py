import logging

from fastapi import APIRouter, Depends, status
from punq import Container

from src.application.user import dto
from src.application.user.commands.create_user import CreateUser
from src.application.user.exceptions import UserIdAlreadyExistsError
from src.application.user.queries.get_user_by_id import GetUserById
from src.domain.user.exceptions import UsernameAlreadyExistsError
from src.domain.user.value_objects.username import EmptyUsernameError, TooLongUsernameError, WrongUsernameFormatError
from src.infrastructure.containers import init_container
from src.infrastructure.mediator.mediator import MediatorImpl
from src.presentation.api.controllers.responses import ErrorResponse


logger = logging.getLogger(__name__)


user_router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@user_router.post(
    "/",
    description="Create new user",
    responses={
        status.HTTP_201_CREATED: {"model": dto.User},
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse[TooLongUsernameError | EmptyUsernameError | WrongUsernameFormatError],
        },
        status.HTTP_409_CONFLICT: {
            "model": ErrorResponse[UsernameAlreadyExistsError | UserIdAlreadyExistsError],
        },
    },
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    data: CreateUser,
    container: Container = Depends(init_container),
) -> dto.UserDTOs:
    mediator: MediatorImpl = container.resolve(MediatorImpl)
    user_id = await mediator.send(data)
    user = await mediator.query(GetUserById(user_id=user_id))
    return user
