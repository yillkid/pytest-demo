"""松年長照中心：跌倒事件紀錄 API（Git 與自動化 第 14 節的起點）。

需求（林護理長）：夜班偵測到跌倒時留一筆紀錄，隔天早上看得到「幾點、哪一台攝影機、哪裡」。
先不用 AI；有地方收、收進來的資料是對的就好。
"""
from datetime import datetime

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

VERSION = "v0.1.0"

app = FastAPI(title="events-api")


class Event(BaseModel):
    event_id: str = Field(pattern=r"^[A-Za-z0-9_-]{3,64}$")
    site: str = Field(min_length=1)
    camera_id: str = Field(min_length=1)
    event_time: datetime
    kind: str = "fall"
    score: float = Field(ge=0, le=1)


EVENTS: dict[str, Event] = {}   # 先存在記憶體；重開就沒了（API 課再換資料庫）


@app.get("/health")
def health():
    return {"status": "ok", "version": VERSION}


@app.post("/events", status_code=201)
def create_event(event: Event):
    if event.event_id in EVENTS:
        raise HTTPException(status_code=409, detail="event_id already exists")
    EVENTS[event.event_id] = event
    return event


@app.get("/events")
def list_events():
    return sorted(EVENTS.values(), key=lambda e: e.event_time)
