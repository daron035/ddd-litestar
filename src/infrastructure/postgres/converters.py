from dataclasses import asdict
from datetime import datetime
from typing import Any, cast

import orjson

from src.application.common.exceptions import MappingError
from src.application.user import dto
from src.domain.common.events.event import Event
from src.domain.user import (
    entities,
    value_objects as vo,
)
from src.domain.user.value_objects import Username
from src.domain.user.value_objects.deleted_status import DeletionTime
from src.infrastructure.event_bus.event_bus import serialize_event
from src.infrastructure.postgres import models


def convert_user_entity_to_db_model(user: entities.User) -> models.User:
    return models.User(
        id=user.id.to_raw(),
        username=user.username.to_raw(),
        first_name=user.full_name.first_name,
        last_name=user.full_name.last_name,
        middle_name=user.full_name.middle_name,
        deleted_at=user.deleted_at.to_raw(),
    )


def convert_db_model_to_user_entity(user: models.User, existing_usernames: set[Username]) -> entities.User:
    full_name = vo.FullName(
        first_name=user.first_name,
        last_name=user.last_name,
        middle_name=user.middle_name,
    )
    return entities.User(
        id=vo.UserId(user.id),
        username=vo.Username(user.username),
        full_name=full_name,
        deleted_at=DeletionTime(user.deleted_at),
        existing_usernames=existing_usernames,
    )


def convert_db_model_to_active_user_dto(user: models.User) -> dto.User:
    if user.deleted_at is not None:
        raise MappingError(f"User {user} is deleted")

    return dto.User(
        id=user.id,
        username=cast(str, user.username),
        first_name=user.first_name,
        last_name=user.last_name,
        middle_name=user.middle_name,
    )


def convert_db_model_to_deleted_user_dto(user: models.User) -> dto.DeletedUser:
    if user.deleted_at is None:
        raise MappingError(f"User {user} isn't deleted")

    return dto.DeletedUser(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        middle_name=user.middle_name,
        deleted_at=cast(datetime, user.deleted_at),
    )


def convert_db_model_to_user_dto(user: models.User) -> dto.UserDTOs:
    match user:
        case models.User(deleted_at=None):
            return convert_db_model_to_active_user_dto(user)
        case models.User(deleted_at=True):
            return convert_db_model_to_deleted_user_dto(user)
        case _:
            raise MappingError(f"User {user} is invalid")


def convert_events_to_outbox_db_model(event: Event | list[Event]) -> list[models.Outbox]:
    if isinstance(event, list):
        ev = [convert_single_event(e) for e in event]
    else:
        ev = [convert_single_event(event)]
    return ev


def convert_single_event(event: Event) -> models.Outbox:
    return models.Outbox(
        id=event.event_id,
        occurred_on=event.event_timestamp,
        type=event.__class__.__name__,
        data=serialize_event_data_sql(event),
    )


def serialize_event_data_sql(event: Any) -> Any:
    event_dict = asdict(event)
    serialized_event = orjson.dumps({k: serialize_event(v) for k, v in event_dict.items()}).decode("utf-8")
    return serialized_event
