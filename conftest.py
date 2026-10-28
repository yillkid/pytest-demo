# 讓 pytest 把 repo 根目錄加入 import 路徑，`from app.main import app` 才找得到。
import pytest

from app.main import EVENTS


@pytest.fixture(autouse=True)
def _clear_events():
    EVENTS.clear()
    yield
    EVENTS.clear()
