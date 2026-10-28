"""事件 API 的測試：每一條都對應林護理長的一個需求。"""
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def make_event(**kw):
    e = {
        "event_id": "s1cam2-20260112-021503-0",
        "site": "松年長照中心",
        "camera_id": "cam2",
        "event_time": "2026-01-12T02:15:03+08:00",
        "kind": "fall",
        "score": 0.97,
    }
    e.update(kw)
    return e


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_create_and_list():
    # 需求：送進來的事件，早上查得到
    assert client.post("/events", json=make_event()).status_code == 201
    r = client.get("/events")
    assert r.status_code == 200
    assert [e["event_id"] for e in r.json()] == ["s1cam2-20260112-021503-0"]


def test_duplicate_rejected():
    # 需求：同一件事不要記兩次（攝影機重送）
    client.post("/events", json=make_event())
    assert client.post("/events", json=make_event()).status_code == 409


def test_score_out_of_range_rejected():
    # 需求：分數是 0～1；有人送 97（百分比）要擋下來
    assert client.post("/events", json=make_event(score=97)).status_code == 422


def test_event_time_without_timezone_rejected():
    # 需求：時間不能錯。沒寫 +08:00 的時間，存起來不知道是台灣幾點 → 要擋下來
    r = client.post("/events", json=make_event(event_time="2026-01-12T02:15:03"))
    assert r.status_code == 422
