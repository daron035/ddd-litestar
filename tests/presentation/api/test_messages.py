from faker import Faker
from httpx import Response
from litestar import Litestar
from litestar.status_codes import HTTP_201_CREATED, HTTP_500_INTERNAL_SERVER_ERROR
from litestar.testing import AsyncTestClient


async def test_create_chat_success(
    test_client: AsyncTestClient[Litestar],
    faker: Faker,
):
    title = faker.text()[:100]
    response: Response = await test_client.post("/", json={"title": title})

    assert response.is_success
    assert response.status_code == HTTP_201_CREATED

    json_data = response.json()
    assert json_data["title"]["value"] == title


async def test_create_chat_fail_text_too_long(
    test_client: AsyncTestClient[Litestar],
    faker: Faker,
):
    title = faker.text(max_nb_chars=500)
    response: Response = await test_client.post("/", json={"title": title})

    assert response.status_code == HTTP_500_INTERNAL_SERVER_ERROR

    # json_data = response.json()
    # assert json_data["detail"] == "Bad Request"


async def test_create_chat_fail_text_empty(
    test_client: AsyncTestClient[Litestar],
):
    response: Response = await test_client.post("/", json={"title": ""})

    assert response.status_code == HTTP_500_INTERNAL_SERVER_ERROR

    # json_data = response.json()
    # assert json_data["detail"] == "Bad Request"
