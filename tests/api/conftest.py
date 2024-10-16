from fastapi import FastAPI
from fastapi.testclient import TestClient

import pytest

from src.presentation.api.main import init_api


@pytest.fixture
def app() -> FastAPI:
    app = init_api()
    return app


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app=app)
